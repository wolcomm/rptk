from rptk.modules.format import BaseFormat


class TestFormat(BaseFormat):
    description = "Test output format"

    def format(self, result=None, name=None):
        self.log_method_enter(method=self.current_method)
        name = super(TestFormat, self).format(result=result, name=name)
        output = {
            name: result.dict()
        }
        self.log_method_exit(method=self.current_method)
        return output

    def validate(self, output=None):
        self.log_method_enter(method=self.current_method)
        if not isinstance(output, dict):
            self.raise_type_error(arg=output, cls=dict)
        self.log_method_exit(method=self.current_method)
        return True
