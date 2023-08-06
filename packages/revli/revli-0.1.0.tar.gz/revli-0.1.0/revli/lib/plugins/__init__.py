from os.path import exists

from revli.lib.plugins.chalkboard import ChalkBoard
from revli.lib.plugins.chart import Chart
from revli.lib.plugins.d3 import D3
from revli.lib.plugins.mapbox import Mapbox
from revli.lib.plugins.math import Math
from revli.lib.plugins.multiplex import Multiplex
from revli.lib.plugins.otffragmentorder import OTFFragmentOrder
from revli.lib.plugins.search import Search
from revli.lib.plugins.tagcloud import Tagcloud
from revli.lib.plugins.zoom import Zoom

PLUGINS = {"chalkboard": ChalkBoard, "chart": Chart, "d3": D3, "mapbox": Mapbox, "math": Math,
           "multiplex": Multiplex, "otf-fragment": OTFFragmentOrder, "search": Search,
           "tagcloud": Tagcloud, "zoom": Zoom}


def add(plugin, file, data_dir):
    """
    add a plugin to a file

    :param plugin: the plugin which should be added
    :param file: the file to which the plugin should be added
    :param data_dir: the directory where the program data is stored
    """
    if not exists(file):
        raise OSError
    if plugin == "all":
        for plugin in PLUGINS:
            add(plugin, file, data_dir)
        return
    if plugin not in PLUGINS:
        raise ValueError("no valid plugin")
    print(f"adding plugin {plugin}...", end="\t")
    plugin = PLUGINS[plugin](file, data_dir)
    plugin.add()
    plugin.write()
    print("success")


def command(plugin, file, data_dir):
    """
    run a command of a plugin

    The Plugin will get its parameters through a cli
    :param plugin: the plugin which should be added
    :param file: the file to which the plugin should be added
    :param data_dir: the directory where the program data is stored
    """
    if plugin not in PLUGINS:
        raise ValueError("no valid plugin")
    print(f"running command for plugin {plugin}")
    plugin = PLUGINS[plugin](file, data_dir)
    plugin.command()


def plugin_help(plugin):
    """
    get the help of a certain plugin
    :param plugin: the name of the plugin
    """
    if plugin not in PLUGINS:
        raise ValueError("no valid plugin")
    PLUGINS[plugin].help()
