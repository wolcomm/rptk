import json
from rptk.modules.format import BaseFormat


class JsonFormat(BaseFormat):
    def format(self, result=None, name=None):
        self.log_method_enter(method=self.current_method)
        name = super(JsonFormat, self).format(result=result, name=name)
        self.log.debug(msg="creating json output")
        try:
            output = json.dumps(
                {name: result.dict()},
                indent=4
            )
            self.log_method_exit(method=self.current_method)
            return output
        except Exception as e:
            self.log.error(msg=e.message)
            raise

    def validate(self, output=None):
        self.log_method_enter(method=self.current_method)
        super(JsonFormat, self).validate(output=output)
        try:
            json.loads(output)
        except Exception as e:
            self.log.error(msg=e.message)
            raise
        self.log_method_exit(method=self.current_method)
        return True
