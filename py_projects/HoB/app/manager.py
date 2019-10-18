import sys
import os
from app.interfaces import Plugin, Manager


class PluginManager(Manager):
    def __init__(self, path: str = None, plugin_init_args: dict = None):
        self.plugin_dir = path if path is not None else os.path.dirname(__file__) + '/plugins/'
        plugin_init_args = plugin_init_args or {}
        self.plugins: dict = {}
        self._load_plugins()
        self._register_plugins(**plugin_init_args)

    def _load_plugins(self):
        sys.path.append(self.plugin_dir)
        plugin_files = [fn for fn in os.listdir(self.plugin_dir) if fn.find('plug') != -1 and fn.endswith('.py')]
        plugin_modules = [m.split('.')[0] for m in plugin_files]
        for module in plugin_modules:
            _ = __import__(module)

    def _register_plugins(self, **kwargs):
        """
        :param kwargs:
        :return:
        """
        for plugin in Plugin.__subclasses__():
            obj = plugin(**kwargs)
            self.plugins[obj] = obj.keywords if hasattr(obj, 'keywords') else []

    def call_method(self, method, args: dict = None, keywords: list = None):
        args = args or {}
        keywords = keywords or []
        result: dict = {}
        for plugin in self.plugins:
            if not keywords or (set(keywords) & set(self.plugins[plugin])):
                try:
                    name_space = plugin.__class__.__name__
                    result[name_space] = getattr(plugin, method)(**args)
                except AttributeError:
                    pass

        return result

    def get_plugins_description(self, args: dict = None, keywords: list = None):
        args = args or {}
        keywords = keywords or []

        result = []
        for plugin in self.plugins:
            if not keywords or (set(keywords) & set(self.plugins[plugin])):
                result.append((self.plugins[plugin], plugin.description))

        return result

    def find_plugin(self):
        pass
