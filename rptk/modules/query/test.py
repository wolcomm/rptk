from rptk.modules.query import BaseQuery


class TestQuery(BaseQuery):
    def query(self, obj=None):
        obj = super(TestQuery, self).query(obj=obj)
        result = {
            u'object': obj
        }
        return result
