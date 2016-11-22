from rptk.modules.format import BaseFormat


class IosFormat(BaseFormat):
    def format(self, result=None, name=None):
        super(IosFormat, self).format(result=result, name=name)
        output = str()
        for af in result:
            if result[af]:
                output += "no %s %s\n" % (self.af(af=af), name)
                i = 0
                for entry in result[af]:
                    i += 10
                    output += self.line(name=name, af=af, entry=entry, i=i)
        return output

    def line(self, name='Prefix-List', af=None, entry=None, i=None):
        if not isinstance(entry, dict):
            raise ValueError("%s not of type %s" % (entry, dict))
        if not isinstance(i, int):
            raise ValueError("%s not of type %s" % (i, int))
        output = "%s %s seq %s permit %s" % (self.af(af=af), name, i, entry['prefix'])
        if not entry['exact']:
            if 'greater-equal' in entry:
                output += " ge %s" % entry['greater-equal']
            if 'less-equal' in entry:
                output += " le %s" % entry['less-equal']
        output += "\n"
        return output

    def af(self, af=None):
        if af == 'ipv4':
            return 'ip prefix-list'
        elif af == 'ipv6':
            return 'ipv6 prefix-list'
        else:
            raise ValueError("%s is not a valid address-family name" % af)
