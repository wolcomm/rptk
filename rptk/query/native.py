# Copyright (c) 2018 Workonline Communications (Pty) Ltd. All rights reserved.
#
# The contents of this file are licensed under the Apache License version 2.0
# (the "License"); you may not use this file except in compliance with the
# License.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations under
# the License.
"""rptk module.query.native module."""

from __future__ import print_function
from __future__ import unicode_literals

import ipaddress
import re
import socket

from rptk.__meta__ import __version__ as version
from rptk.query import BaseQuery


try:
    unicode
except NameError:
    unicode = str


class NativeQuery(BaseQuery):
    """Performs queries directly over python sockets."""

    def __init__(self, **opts):
        """Initialise new object."""
        super(NativeQuery, self).__init__(**opts)
        self._regexp = re.compile(
            r'(?P<state>[ACDEF])(?P<len>\d*)(?P<msg>[\w\s]*)$'
        )
        self._keepalive = True
        self.log_init_done()

    def __enter__(self):
        """Set up a TCP connection."""
        self.log_ready_start()
        self._connect()
        self.log_ready_done()
        return self

    def __exit__(self, typ, value, traceback):
        """Tear down the connection."""
        self.log_exit_start()
        self._disconnect()
        self.log_exit_done()

    def query(self, obj=None):
        """Execute a query."""
        obj = super(NativeQuery, self).query(obj=obj)
        tmp = dict()
        sets = {u'ipv4': set(), u'ipv6': set()}
        self.log.debug(msg="trying to get members of {}".format(obj))
        members = self._members(obj=obj)
        for member in members:
            self.log.debug(msg="trying to get routes for {}".format(member))
            routes = self._routes(obj=member)
            for af in routes:
                sets[af].update(routes[af])
        for af in sets:
            prefixes = sorted(list(sets[af]))
            tmp[af] = [{u'prefix': p.with_prefixlen, u'exact': True}
                       for p in prefixes]
            self.log.debug(msg="found {} {} prefixes for object {}"
                               .format(len(tmp[af]), af, obj))
        result = tmp
        self.log_method_exit(method=self.current_method)
        return result

    def _connect(self):
        """Establish a TCP connection to the IRR server."""
        self.log.debug(msg="creating socket")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log.debug(msg="trying to connect to {}".format(self.target))
        try:
            self._socket.connect((self.host, self.port))
        except socket.error as e:
            self.log.error(msg="{}".format(e))
            raise
        self.log.debug(msg="socket connected")
        if self._keepalive:
            self._socket.send(b'!!\n')
        self._query('!nRPTK-{}'.format(version))

    def _disconnect(self):
        """Tear the TCP connection down."""
        self.log.debug(msg="disconnecting socket")
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        self.log.debug(msg="socket closed")

    def _query(self, q, skip_errors=None):
        q += '\n'
        q = q.encode()
        total_sent = 0
        query_length = len(q)
        while total_sent < query_length:
            sent = self._socket.send(q[total_sent:])
            if not sent:
                self.raise_runtime_error(msg="socket connection broken")
            total_sent += sent
        self.log.debug(msg="sent query {} (length {} bytes)"
                           .format(q.rstrip(), total_sent))
        chunks = []
        chunk_size = 4096
        chunk = self._socket.recv(chunk_size)
        response, chunk = chunk.split(b'\n', 1)
        try:
            response_length = self._parse_response(response)
        except IRRQueryError as e:
            if type(e) in skip_errors:
                self.log.debug(msg="{}".format(e))
                response_length = False
            else:
                self.log.error(msg="{}".format(e))
                raise
        if not response_length:
            return
        total_rcvd = len(chunk) or 0
        chunks.append(chunk)
        while total_rcvd <= response_length:
            self.log.debug(msg="received {} of {} bytes"
                               .format(total_rcvd, response_length))
            chunk = self._socket.recv(chunk_size)
            if chunk == b'':
                self.raise_runtime_error(msg="socket connection broken")
            chunks.append(chunk)
            total_rcvd += len(chunk)
        self.log.debug(msg="received {} of {} bytes"
                           .format(total_rcvd, response_length))
        suffix = chunks[-1][-(total_rcvd - response_length):]
        chunks[-1] = chunks[-1][:-len(suffix)]
        self.log.debug("suffix length: {}".format(len(suffix)))
        return ''.join(c.decode() for c in chunks)

    def _parse_response(self, response):
        """Check response code and return response data length."""
        self.log.debug("received response {}".format(response))
        response = response.decode()
        match = self._regexp.match(response)
        if not match:
            self.raise_runtime_error("invalid response '{}'".format(response))
        state = match.group('state')
        if state == 'A':
            length = int(match.group('len'))
            self.log.debug(msg="query successful: {} bytes of data"
                               .format(length))
            return length
        elif state == 'C':
            self.log.debug(msg="query successful. no data.")
            return False
        elif state == 'D':
            raise KeyNotFoundError()
        elif state == 'E':
            raise KeyNotUniqueError()
        elif state == 'F':
            if match.group('msg'):
                msg = match.group('msg').strip()
            else:
                msg = 'unknown error'
            raise OtherError(msg)
        raise RuntimeError("invalid response '{}'".format(response))

    def _members(self, obj=None):
        """Resolve an as-set to its members."""
        q = "!i{},1".format(obj)
        members = self._query(q, skip_errors=(KeyNotFoundError,))
        if members:
            members = members.split()
            self.log.debug("found {} members of {}".format(len(members), obj))
            return members
        else:
            self.log.debug("no members of {} found. treating as autnum."
                           .format(obj))
            return [obj]

    def _routes(self, obj=None):
        """Get routes for specified object."""
        proto = {
            u'ipv4': {'cmd': '!g', 'class': ipaddress.IPv4Network},
            u'ipv6': {'cmd': '!6', 'class': ipaddress.IPv6Network}
        }
        routes = dict()
        for af in proto:
            cmd = proto[af]['cmd']
            cls = proto[af]['class']
            q = "{}{}".format(cmd, obj)
            routes[af] = list()
            resp = self._query(q, skip_errors=(KeyNotFoundError,))
            if resp:
                for each in resp.split():
                    try:
                        routes[af].append(cls(unicode(each)))
                    except (ipaddress.AddressValueError,
                            ipaddress.NetmaskValueError):
                        self.log.warning(msg="converting {} to {} failed"
                                             .format(each, cls))
            self.log.debug(msg="found {} {} prefixes for object {}"
                               .format(len(routes[af]), af, obj))
        return routes


class IRRQueryError(RuntimeError):
    """Exception raised during query execution."""

    proto_msg = ''

    def __init__(self, *args, **kwargs):
        """Initialise the Exception instance."""
        super(IRRQueryError, self).__init__(self.proto_msg, *args, **kwargs)


class KeyNotFoundError(IRRQueryError):
    """The RPSL key was not found."""

    proto_msg = "Key not found. (D)"


class KeyNotUniqueError(IRRQueryError):
    """There are multiple copies of the key in one database. (E)."""

    proto_msg = "There are multiple copies of the key in one database. (E)"


class OtherError(IRRQueryError):
    """An unknown error occured during query execution."""

    proto_msg = "Some other error, see the <optional message> for details."
