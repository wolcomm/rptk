from rptk.modules.format import JinjaFormat


class BirdFormat(JinjaFormat):
    """ renders result object as a BIRD prefix-list """
    template_name = 'bird.j2'
