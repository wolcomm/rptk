from rptk.modules.format import BaseFormat


class TestFormat(BaseFormat):
    def format(self, result=None, name=None):
        super(TestFormat, self).format(result=result, name=name)
        output = {
            unicode(name): result
        }
        return output
