from rptk.modules.format import BaseFormat


class IosFormat(BaseFormat):
    def format(self, result=None, name=None):
        super(IosFormat, self).format(result=result, name=name)
        output = str()
        for af in result:
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
        ge, le = '', ''
        if entry['exact']:
            return "%s %s seq %s permit %s\n" % (self.af(af=af), name, i, entry['prefix'])
        else:
            if 'greater-equal' in entry:
                ge = " %s" % entry['greater-equal']
            if 'less-equal' in entry:
                le = " %s" % entry['less-equal']
            return "%s %s seq %s permit %s%s%s\n" % (
                self.af(af=af), name, i, entry['prefix'], ge, le
            )

    def af(self, af=None):
        if af == 'ipv4':
            return 'ip prefix-list'
        elif af == 'ipv6':
            return 'ipv6 prefix-list'
        else:
            raise ValueError("%s is not a valid address-family name" % af)
