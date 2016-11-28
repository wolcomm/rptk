import socket
import re
import ipaddress
from pkg_resources import get_distribution
from rptk.modules.query import BaseQuery


class NativeQuery(BaseQuery):
    def __init__(self, config=None):
        super(NativeQuery, self).__init__(config=config)
        self._regexp = re.compile('(?P<state>[ACDEF])(?P<len>\d*)(?P<msg>[\w\s]*)$')
        self._keepalive = True
        self.log_init_done()

    def __enter__(self):
        self.log_ready_start()
        self._connect()
        self.log_ready_done()
        return self

    def __exit__(self, typ, value, traceback):
        self.log_exit_start()
        self._disconnect()
        self.log_exit_done()

    def query(self, obj=None):
        obj = super(NativeQuery, self).query(obj=obj)
        result = dict()
        sets = {u'ipv4': set(), u'ipv6': set()}
        self.log.debug(msg="trying to get members of %s" % obj)
        members = self._members(obj=obj)
        for member in members:
            self.log.debug(msg="trying to get routes for %s" % member)
            routes = self._routes(obj=member)
            for af in routes:
                sets[af].update(routes[af])
        for af in sets:
            prefixes = sorted(list(sets[af]))
            result[af] = [{u'prefix': p.with_prefixlen, u'exact': True} for p in prefixes]
            self.log.debug(msg="found %s %s prefixes for object %s" % (len(result[af]), af, obj))
        self.log_method_exit(method=self.current_method)
        return result

    def _connect(self):
        self.log.debug(msg="creating socket")
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.log.debug(msg="trying to connect to %s:%s" % (
            self.config.args.host, self.config.args.port)
            )
        try:
            self._socket.connect((self.config.args.host, self.config.args.port))
        except socket.error as e:
            self.log.error(msg=e.message)
            raise
        self.log.debug(msg="socket connected")
        if self._keepalive:
            self._socket.send('!!\n')
        self._query('!nRPTK-%s' % get_distribution('rptk').version)

    def _disconnect(self):
        self.log.debug(msg="disconnecting socket")
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()
        self.log.debug(msg="socket closed")

    def _query(self, q, skip_errors=None):
        q += '\n'
        total_sent = 0
        query_length = len(q)
        while total_sent < query_length:
            sent = self._socket.send(q[total_sent:])
            if not sent:
                self.raise_runtime_error(msg="socket connection broken")
            total_sent += sent
        self.log.debug("sent query %s (length %d bytes)", q.rstrip(), total_sent)
        chunks = []
        chunk_size = 4096
        chunk = self._socket.recv(chunk_size)
        response, chunk = chunk.split('\n', 1)
        try:
            response_length = self._parse_response(response)
        except IRRQueryError as e:
            if type(e) in skip_errors:
                self.log.debug(msg=e.message)
                response_length = False
            else:
                self.log.error(msg=e.message)
                raise
        if not response_length:
            return
        total_rcvd = len(chunk) or 0
        chunks.append(chunk)
        while total_rcvd <= response_length:
            self.log.debug("received %d of %d bytes", total_rcvd, response_length)
            chunk = self._socket.recv(chunk_size)
            if chunk == '':
                self.raise_runtime_error(msg="socket connection broken")
            chunks.append(chunk)
            total_rcvd += len(chunk)
        self.log.debug("received %d of %d bytes", total_rcvd, response_length)
        suffix = chunks[-1][-(total_rcvd - response_length):]
        chunks[-1] = chunks[-1][:-len(suffix)]
        self.log.debug("suffix length: %d", len(suffix))
        return ''.join(chunks)

    def _parse_response(self, response):
        """ check response code and return response data length """
        self.log.debug("received response %s", response)
        match = self._regexp.match(response)
        if not match:
            self.raise_runtime_error("invalid response '%s'" % (response,))
        state = match.group('state')
        if state == 'A':
            length = int(match.group('len'))
            self.log.debug(msg="query successful: %d bytes of data" % length)
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
        raise RuntimeError("invalid response '%s'" % (response,))

    def _members(self, obj=None):
        """ resolve an as-set to its members """
        q = "!i%s,1" % obj
        members = self._query(q, skip_errors=(KeyNotFoundError,))
        if members:
            members = members.split()
            self.log.debug("found %d members of %s" % (len(members), obj))
            return members
        else:
            self.log.debug("no members of %s found. treating as autnum." % obj)
            return [obj]

    def _routes(self, obj=None):
        """ get routes for specified object """
        proto = {
            u'ipv4': {'cmd': '!g', 'class': ipaddress.IPv4Network},
            u'ipv6': {'cmd': '!6', 'class': ipaddress.IPv6Network}
        }
        routes = dict()
        for af in proto:
            cmd = proto[af]['cmd']
            cls = proto[af]['class']
            q = "%s%s" % (cmd, obj)
            routes[af] = list()
            resp = self._query(q, skip_errors=(KeyNotFoundError,))
            if resp:
                for each in resp.split():
                    try:
                        routes[af].append(cls(unicode(each)))
                    except ipaddress.AddressValueError, ipaddress.NetmaskValueError:
                        self.log.warning("converting %s to %s failed" % (each, cls))
            self.log.debug("found %d %s prefixes for object %s" % (len(routes[af]), af, obj))
        return routes


class IRRQueryError(RuntimeError):
    proto_msg = ''

    def __init__(self, *args, **kwargs):
        super(IRRQueryError, self).__init__(self.proto_msg, *args, **kwargs)


class KeyNotFoundError(IRRQueryError):
    proto_msg = "Key not found. (D)"


class KeyNotUniqueError(IRRQueryError):
    proto_msg = "There are multiple copies of the key in one database. (E)"


class OtherError(IRRQueryError):
    proto_msg = "Some other error, see the <optional message> for details."
