from rptk.modules.format import JinjaFormat


class IosNullFormat(JinjaFormat):
    """
    renders result object as a Cisco IOS prefix-list with an explicit deny
    all for empty lists
    """
    description = "Cisco IOS Classic / XE null prefix-list"
    template_name = 'ios_null.j2'
