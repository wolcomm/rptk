from rptk.modules.format import BaseFormat


class JunosFormat(BaseFormat):
    def format(self, result=None, name=None):
        super(JunosFormat, self).format(result=result, name=name)
        output = str()
        output += \
            "policy-options {\n" \
            "replace:\n" \
            "  prefix-list %s {\n" % name
        for af in result:
            for entry in result[af]:
                output += "    %s;\n" % entry['prefix']
        output += "  }\n" \
                  "}\n"
        return output
