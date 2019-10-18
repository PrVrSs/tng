from app.manager import PluginManager


def main():
    plugin_manager = PluginManager()
    plugin_manager.call_method('process', keywords=['plug'], args={'plug': 1})
    plugin_manager.call_method('report')
    print(plugin_manager.get_plugins_description())


if __name__ == "__main__":
    main()
