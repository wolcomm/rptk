import radix
from rptk.base import BaseObject


class PrefixSet(BaseObject):
    def __init__(self, results=None):
        super(PrefixSet, self).__init__()
        self.log_init()
        if not isinstance(results, dict):
            self.raise_type_error(arg=results, cls=dict)
        self.log.debug(msg="creating radix trees")
        self._trees = {'ipv4': radix.Radix(), 'ipv6': radix.Radix()}
        for af in results:
            self.log.debug(msg="adding %s prefixes to tree" % af)
            for entry in results[af]:
                prefix = entry[u"prefix"]
                self.log.debug(msg="adding prefix: %s" % prefix)
                node = self._trees[af].add(prefix)
                self.log.debug(msg="adding data to radix node")
                try:
                    node.data[u"greater-equal"] = entry[u"greater-equal"]
                except KeyError as e:
                    self.log.debug(msg="no key '%s' found" % e.message)
                try:
                    node.data[u"less-equal"] = entry[u"less-equal"]
                except KeyError as e:
                    self.log.debug(msg="no key '%s' found" % e.message)
                node.data[u"active"] = True
        self.log_init_done()

    def dict(self):
        self.log_method_enter(method=self.current_method)
        result = dict()
        for af in self._trees:
            result[af] = list()
            tree = self._trees[af]
            for node in tree.nodes():
                if node.data["active"]:
                    entry = {
                        u'prefix': node.prefix,
                        u'exact': self.exact(node.data),
                    }
                    if u"greater-equal" in node.data:
                        entry[u"greater-equal"] = node.data[u"greater-equal"]
                    if u"less-equal" in node.data:
                        entry[u"less-equal"] = node.data[u"less-equal"]
                    result[af].append(entry)
        return result

    @staticmethod
    def exact(data=None):
        if "greater-equal" in data:
            return True
        if "less-equal" in data:
            return True
        return False
