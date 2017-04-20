from __future__ import unicode_literals
import re
import ipaddress
from collections import Set
from rptk.base import BaseObject


class PrefixSet(BaseObject, Set):
    def __init__(self, data=None, **kwargs):
        super(PrefixSet, self).__init__()
        self.log_init()
        if not isinstance(data, dict):
            try:
                data = self.parse_prefix_range(expr=data)
            except ValueError as e:
                self.log.error(msg=e.message)
                raise e
        self._meta = kwargs
        self.log.debug(msg="creating prefix sets")
        self._sets = {'ipv4': set(), 'ipv6': set()}
        for af in data:
            try:
                version = int(re.match(r'^ipv(\d)', af).group(1))
            except ValueError:
                self.log.warning(msg="invalid address-family %s" % af)
            self.log.debug(msg="adding %s prefixes to set" % af)
            s = self._sets[af]
            for entry in data[af]:
                try:
                    prefix, root = self.index_of(entry["prefix"])
                except ValueError as e:
                    self.log.warning(msg=e.message)
                if prefix.version != version:
                    self.log.warning(msg="prefix %s not of version %d" % (prefix, version))
                    continue
                l = prefix.prefixlen
                h = prefix.max_prefixlen
                self.log.debug(msg="setting base index of prefix: %s = %d" % (prefix, root))
                try:
                    m = max(int(entry["greater-equal"]), l)
                except (KeyError, ValueError):
                    m = l
                self.log.debug(msg="min-length set to %d" % m)
                try:
                    n = min(int(entry["less-equal"]), h)
                except (KeyError, ValueError):
                    n = m
                self.log.debug(msg="max-length set to %d" % n)
                self.log.debug(msg="traversing subtree from index %d" % root)
                depth = n - l
                left = right = root
                for d in range(0, depth + 1):
                    if d >= m - l:
                        s.add((left, right + 1))
                        self.log.debug(msg="added %d indices at depth %d" % (left - right + 1, d))
                    left *= 2
                    right = 2*right + 1
                self.log.debug(msg="indexing %s^%d-%d complete" % (prefix, m, n))
        self.log_init_done()

    def __contains__(self, item):
        if isinstance(item, tuple):
            version = item[0]
            index = item[1]
        else:
            try:
                prefix, index = self.index_of(prefix=item)
            except ValueError as e:
                self.log.error(msg=e.message)
                raise e
            version = prefix.version
        for lower, upper in self.sets(version):
            if lower <= index < upper:
                return True
        return False

    def __iter__(self):
        for version in (4, 6):
            for lower, upper in self.sets(version):
                index = lower
                while index < upper:
                    yield (version, index)
                    index += 1

    def __len__(self):
        count = 0
        for version in (4, 6):
            for lower, upper in self.sets(version):
                count += upper - lower
        return count

    def _iter_ranges(self):
        for version in (4, 6):
            for lower, upper in self.sets(version):
                yield (version, lower, upper)

    def __and__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        it = list()
        for i_version, i_lower, i_upper in other._iter_ranges():
            for j_version, j_lower, j_upper in self._iter_ranges():
                if i_version == j_version:
                    v = i_version
                    l = max(i_lower, j_lower)
                    u = min(i_upper, j_upper)
                    if l <= u:
                        it.append((v, l, u))
        return self._from_iterable(it)

    @classmethod
    def _from_iterable(cls, it):
        self = cls({})
        for item in it:
            af = "ipv%d" % item[0]
            lower = item[1]
            try:
                upper = item[2]
            except IndexError:
                upper = lower + 1
            try:
                self._sets[af].add((lower, upper))
            except KeyError as e:
                self.log.error(msg=e.message)
                raise e
        return self

    def sets(self, af=None):
        try:
            return self._sets[af]
        except KeyError as e:
            try:
                return self._sets["ipv%d" % af]
            except KeyError as f:
                self.log.warning(msg=e.message)
                self.log.error(msg=f.message)
                raise f

    def prefixes(self):
        for af in ("ipv4", "ipv6"):
            for lower, upper in self.sets(af):
                for index in range(lower, upper):
                    yield self.indexed_by(index=index, af=af)

    @staticmethod
    def index_of(prefix=None):
        prefix = ipaddress.ip_network(prefix)
        p = int(prefix.network_address)
        l = prefix.prefixlen
        h = prefix.max_prefixlen
        index = 2**l + p/2**(h - l)
        return prefix, index

    @staticmethod
    def indexed_by(index=None, af=None):
        address_families = {
            'ipv4': {'size': 32, 'cls': ipaddress.IPv4Network},
            'ipv6': {'size': 128, 'cls': ipaddress.IPv6Network}
        }
        assert isinstance(index, (int, long))
        assert af in address_families
        h = int(address_families[af]['size'])
        cls = address_families[af]['cls']
        l = index.bit_length() - 1
        p = index * 2**(h - l) - 2**h
        return cls((p, l))

    @staticmethod
    def parse_prefix_range(expr=None):
        pattern = r'^(?P<prefix>((\d+(\.\d+){3})|([0-9a-fA-F:]{2,40}))/\d+)' \
                  r'(\^(?P<ge>\d+)-(?P<le>\d+))?$'
        match = re.match(pattern, expr)
        if match:
            prefix = ipaddress.ip_network(unicode(match.group("prefix")))
            afi = "ipv%d" % prefix.version
            entry = {"prefix": prefix}
            try:
                entry["greater-equal"] = int(match.group("ge"))
                entry["less-equal"] = int(match.group("le"))
            except (IndexError, TypeError):
                pass
        else:
            raise ValueError("no match found")
        return {afi: [entry]}
