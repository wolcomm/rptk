from rptk.modules.format import BaseFormat


class JunosFormat(BaseFormat):
    def format(self, result=None, name=None):
        super(JunosFormat, self).format(result=result, name=name)
        output = str()
        output += \
            "policy-options {" \
            "replace:" \
            "  prefix-list %s {" % name
        for af in result:
            for entry in result[af]:
                output += "    %s;\n" % entry['prefix']
        output += "  }" \
                  "}"
        return output
