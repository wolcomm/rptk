import yaml
from rptk.modules.format import BaseFormat


class YamlFormat(BaseFormat):
    description = "YAML object representation"

    def format(self, result=None, name=None):
        self.log_method_enter(method=self.current_method)
        name = super(YamlFormat, self).format(result=result, name=name)
        self.log.debug(msg="creating json output")
        try:
            output = yaml.dump(
                {name: result.dict()},
                indent=4,
                explicit_start=True,
                explicit_end=True,
                default_flow_style=False,
            )
            self.log_method_exit(method=self.current_method)
            return output
        except Exception as e:
            self.log.error(msg=e.message)
            raise

    def validate(self, output=None):
        self.log_method_enter(method=self.current_method)
        super(YamlFormat, self).validate(output=output)
        try:
            yaml.load(output)
        except Exception as e:
            self.log.error(msg=e.message)
            raise
        self.log_method_exit(method=self.current_method)
        return True
