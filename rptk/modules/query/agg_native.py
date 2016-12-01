from radix import Radix
from rptk.base import BaseObject
from rptk.modules.query.native import NativeQuery


class AggNativeQuery(NativeQuery):
    def query(self, obj=None):
        self.log_method_enter(method=self.current_method)
        tmp = super(AggNativeQuery, self).query(obj=obj)
        ps = PrefixSet(results=tmp)
        result = ps.prefixes()
        self.log_method_exit(method=self.current_method)
        return result


class PrefixSet(BaseObject):
    def __init__(self, results=None):
        super(PrefixSet, self).__init__()
        self.log_init()
        self.log.debug(msg="creating radix trees")
        self._trees = {'ipv4': Radix(), 'ipv6': Radix()}
        for af in results:
            self.log.debug(msg="adding %s prefixes to tree" % af)
            for entry in results[af]:
                prefix = entry[u"prefix"]
                self.log.debug(msg="adding prefix: %s" % prefix)
                node = self._trees[af].add(prefix)
                self.log.debug(msg="adding data to radix node %s" % node)
                node.data["data"] = PrefixData(data=entry)
        self.log_init_done()

    def prefixes(self):
        self.log_method_enter(method=self.current_method)
        result = dict()
        for af in self._trees:
            result[af] = list()
            tree = self._trees[af]
            for node in tree.nodes():
                data = node.data["data"]
                if data.active:
                    entry = {
                        u'prefix': node.prefix,
                        u'exact': data.aggregate,
                    }
                    result[af].append(entry)
        return result


class PrefixData(BaseObject):
    def __init__(self, data=None, active=True):
        super(PrefixData, self).__init__()
        self.log_init()
        if not isinstance(data, dict):
            self.raise_type_error(arg=data, cls=dict)
        self._active = active
        self._minlen = None
        self._maxlen = None
        try:
            self.log.debug(msg="setting min/max lengths")
            self.minlen = data[u"greater-equal"]
            self.maxlen = data[u"less-equal"]
        except KeyError as e:
            self.log.debug(msg="no key '%s' found" % e.message)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self.log_init_done()

    @property
    def active(self):
        return self._active

    @active.setter
    def active(self, val=None):
        self._active = bool(val)

    @property
    def minlen(self):
        return self._minlen

    @minlen.setter
    def minlen(self, val=None):
        try:
            val = int(val)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self._minlen = val

    @property
    def maxlen(self):
        return self._maxlen

    @maxlen.setter
    def maxlen(self, val=None):
        try:
            val = int(val)
        except Exception as e:
            self.log.error(msg=e.message)
            raise e
        self._maxlen = val

    @property
    def aggregate(self):
        if self.minlen or self.maxlen:
            return True
        else:
            return False

