from rptk.modules import PrefixSet
from rptk.modules.query.native import NativeQuery


class AggNativeQuery(NativeQuery):
    def query(self, obj=None):
        self.log_method_enter(method=self.current_method)
        tmp = super(AggNativeQuery, self).query(obj=obj)
        ps = PrefixSet(results=tmp)
        result = ps.dict()
        self.log_method_exit(method=self.current_method)
        return result
