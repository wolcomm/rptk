import yaml
from rptk.modules.format import BaseFormat


class YamlFormat(BaseFormat):
    def format(self, result=None, name=None):
        name = super(YamlFormat, self).format(result=result, name=name)
        output = yaml.dump(
            {name: result},
            indent=4,
            explicit_start=True,
            explicit_end=True,
            default_flow_style=False,
        )
        return output
