import json
from rptk.modules.format import BaseFormat


class JsonFormat(BaseFormat):
    def format(self, result=None, name=None):
        super(JsonFormat, self).format(result=result, name=name)
        output = json.dumps({name: result}, indent=4)
        return output
