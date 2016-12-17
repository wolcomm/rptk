from rptk.modules.format import JinjaFormat


class PlainFormat(JinjaFormat):
    """ renders result object as a Plaintext LOA prefix-list """
    description = "Plaintext (LOA) prefix-list"
    template_name = 'plain.j2'
