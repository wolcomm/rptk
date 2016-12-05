from rptk.modules.format import JinjaFormat


class JunosFormat(JinjaFormat):
    """ renders result object as a Juniper JunOS prefix-list """
    description = "Juniper JunOS prefix-list"
    template_name = 'junos.j2'
