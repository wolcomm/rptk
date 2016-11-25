from rptk.modules.format import BaseFormat


class TestFormat(BaseFormat):
    def format(self, result=None, name=None):
        name = super(TestFormat, self).format(result=result, name=name)
        output = {
            name: result
        }
        return output

    def validate(self, output=None):
        if not isinstance(output, dict):
            raise TypeError("%s not of type %s" % (output, dict))
        return True
