from importlib import import_module

from django.conf import settings


class ModuleImport:
    module = None

    def __init__(self, module):
        self.module = module

    def execute(self):

        modules = {}
        for app in settings.INSTALLED_APPS:
            try:
                module = ".".join([app, self.module])
                modules[app] = import_module(module)
            except ImportError:
                pass
        return modules
