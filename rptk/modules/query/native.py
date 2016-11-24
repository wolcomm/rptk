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

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, typ, value, traceback):
        self._disconnect()

    def query(self, obj=None):
        obj = super(NativeQuery, self).query(obj=obj)
        result = dict()
        sets = {u'ipv4': set(), u'ipv6': set()}
        members = self._members(obj=obj)
        for member in members:
            routes = self._routes(obj=member)
            for af in routes:
                sets[af].update(routes[af])
        for af in sets:
            prefixes = sorted(list(sets[af]))
            result[af] = [{u'prefix': p.with_prefixlen, u'exact': True} for p in prefixes]
        return result

    def _connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((self.config.args.host, self.config.args.port))
        if self._keepalive:
            self._socket.send('!!\n')
        self._query('!nRPTK-%s' % get_distribution('rptk').version)

    def _disconnect(self):
        self._socket.shutdown(socket.SHUT_RDWR)
        self._socket.close()

    def _query(self, q):
        q += '\n'
        ttl = 0
        sz = len(q)
        while ttl < sz:
            sent = self._socket.send(q[ttl:])
            if not sent:
                raise RuntimeError("socket connection broken")
            ttl = ttl + sent
        self.log.debug("sent %s %d", q.rstrip(), ttl)
        chunks = []
        chunk_size = 4096
        chunk = self._socket.recv(chunk_size)
        response, chunk = chunk.split('\n', 1)
        sz = self._parse_response(response)
        if not sz:
            return
        ttl = len(chunk) or 0
        chunks.append(chunk)
        while ttl <= sz:
            self.log.debug("ttl %d, sz %d", ttl, sz)
            chunk = self._socket.recv(chunk_size)
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            ttl += len(chunk)
        self.log.debug("ttl %d, sz %d", ttl, sz)
        suffix = chunks[-1][-(ttl - sz):]
        chunks[-1] = chunks[-1][:-(ttl - sz)]
        self.log.debug("suffix %d '%s'", ttl - sz, suffix)
        return ''.join(chunks)

    def _parse_response(self, response):
        self.log.debug("response %s", response)
        match = self._regexp.match(response)
        if not match:
            raise RuntimeError("invalid response '%s'" % (response,))
        state = match.group('state')
        if state == 'A':
            return int(match.group('len'))
        elif state == 'C':
            return False
        elif state == 'D':
            self.log.warning("skipping key not found")
            return False
        elif state == 'E':
            raise KeyError("multiple copies of key in database")
        elif state == 'F':
            if match.group('msg'):
                msg = match.group('msg').strip()
            else:
                msg = 'unknown error'
            raise RuntimeError(msg)
        raise RuntimeError("invalid response '%s'" % (response,))

    def _members(self, obj=None):
        """ resolve an as-set to its members """
        q = "!i%s,1" % obj
        members = self._query(q)
        if members:
            return members.split()
        else:
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
            resp = self._query(q)
            if resp:
                for each in resp.split():
                    try:
                        routes[af].append(cls(unicode(each)))
                    except ipaddress.AddressValueError, ipaddress.NetmaskValueError:
                        self.log.warning("converting %s to %s failed" % (each, cls))
        return routes
