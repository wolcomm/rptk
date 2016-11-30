import importlib
from rptk.base import BaseObject


class ClassLoader(BaseObject):
    def __init__(self, items=None):
        super(ClassLoader, self).__init__()
        self.log_init()
        if not isinstance(items, list):
            raise TypeError("%s not of type %s" % (items, list))
        self._classes = dict()
        count = 0
        self.log.debug(msg="trying to load classes")
        for item in items:
            name = item[0]
            mod_path, cls_path = item[1].rsplit(".", 1)
            self.log.debug(msg="loading class %s" % cls_path)
            try:
                cls = getattr(importlib.import_module(mod_path), cls_path)
                self._classes.update({name: cls})
                count += 1
            except Exception as e:
                self.log.warning(msg=e.message)
        self.log.debug(msg="loaded %s classes" % count)
        self.log_init_done()

    def get_class(self, name=None):
        return self._classes[name]

    @property
    def class_names(self):
        return [name for name in self._classes]

    @property
    def classes(self):
        return [self.get_class(name) for name in self.class_names]

    @property
    def log(self):
        return self._log
