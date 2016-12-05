from rptk.modules.format import JinjaFormat


class IosFormat(JinjaFormat):
    """ renders result object as a Cisco IOS prefix-list """
    description = "Cisco IOS Classic / XE prefix-list"
    template_name = 'ios.j2'
