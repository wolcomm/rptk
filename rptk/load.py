import importlib


class ClassLoader(object):
    def __init__(self, items=None):
        if not isinstance(items, list):
            raise TypeError("%s not of type %s" % (items, list))
        self._classes = dict()
        for item in items:
            name = item[0]
            mod_path, cls_path = item[1].rsplit(".", 1)
            cls = getattr(importlib.import_module(mod_path), cls_path)
            self._classes.update({name: cls})

    def get_class(self, name=None):
        return self._classes[name]

    @property
    def class_names(self):
        return [name for name in self._classes]

    @property
    def classes(self):
        return [self.get_class(name) for name in self.class_names]
