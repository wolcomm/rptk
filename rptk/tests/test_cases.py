import os
import ConfigParser
from unittest import TestCase
from rptk import load, api


class TestRptk(TestCase):
    config_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'tests.conf')
    # argv = ['--config_path', config_path]
    if os.name == 'posix':
        posix = True
    else:
        posix = False

    def test_api(self):
        # cfg = ConfigParser.SafeConfigParser()
        # cfg.read(self.config_path)
        # query_class_loader = load.ClassLoader(items=cfg.items("query-classes"))
        # format_class_loader = load.ClassLoader(items=cfg.items("format-classes"))
        # obj = cfg.get(section="defaults", option="object")
        # name = cfg.get(section="defaults", option="name")
        rptk = api.Rptk(config_file=self.config_file)
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

    # def test_api(self):
    #     cfg = ConfigParser.SafeConfigParser()
    #     cfg.read(self.config_path)
    #     query_class_loader = load.ClassLoader(items=cfg.items("query-classes"))
    #     format_class_loader = load.ClassLoader(items=cfg.items("format-classes"))
    #     obj = cfg.get(section="defaults", option="object")
    #     name = cfg.get(section="defaults", option="name")
    #     for q in query_class_loader.class_names:
    #         query_class = query_class_loader.get_class(name=q)
    #         if query_class.posix_only and not self.posix:
    #             continue
    #         for f in format_class_loader.class_names:
    #             opts = {'query': q, 'format': f}
    #             rptk = api.Rptk(**opts)
    #             result = rptk.query(obj=obj, name=name, test=True)
    #             self.assertTrue(result)
    #             if result:
    #                 print "api query with query=%s format=%s passed" % (q, f)
