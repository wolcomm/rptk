from rptk.modules.format import BaseFormat


class BirdFormat(BaseFormat):
    def format(self, result=None, name=None):
        super(BirdFormat, self).format(result=result, name=name)
        output = str()
        output += "%s = [\n" % name
        for af in result:
            for entry in result[af]:
                output += "  %s,\n" % entry['prefix']
        output += "];\n"
        return output
