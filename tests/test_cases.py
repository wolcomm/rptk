import os
from rptk import RptkAPI
from unittest import TestCase


class TestRptk(TestCase):
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                               'tests.conf')
    if os.name == 'posix':
        posix = True
    else:
        posix = False

    def test_api(self):
        rptk = RptkAPI(config_file=self.config_file)
        for q in rptk.query_class_loader.class_names:
            query_class = rptk.query_class_loader.get_class(name=q)
            if query_class.posix_only and not self.posix:
                continue
            for f in rptk.format_class_loader.class_names:
                opts = {'query': q, 'format': f}
                rptk.update_opts(**opts)
                result = rptk.query(test=True)
                self.assertTrue(result)
                if result:
                    print "api query with query=%s format=%s passed" % (q, f)
