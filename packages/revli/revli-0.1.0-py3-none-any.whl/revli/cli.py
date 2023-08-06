import argparse
from os.path import exists, join, abspath, dirname

from revli.lib import plugins
from revli.lib.create import create

# the directory in which all the data files are stored
DATA_DIR = join(abspath(dirname(__file__)), "data")


def main():
    parser = argparse.ArgumentParser(description="A cli for reveal.js presentations")
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    create_parser = subparsers.add_parser("create", help="create a presentation", aliases=["c"])
    create_parser.add_argument("--path", type=str, help="the path where the presentation should be created",
                               default=".")
    create_parser.add_argument("--name", type=str, help="the name of the presentation", default="reveal.js")

    plugin_parser = subparsers.add_parser("plugin", help="manage the plugins of your presentation", aliases=["p"])
    plugin_subparsers = plugin_parser.add_subparsers(title="subcommands", dest="plugin_subcommand")

    plugin_add_parser = plugin_subparsers.add_parser("add", help="add a plugin to your presentation", aliases=["a"])
    plugin_add_parser.add_argument("name", type=str, help="the name of the plugin")
    plugin_add_parser.add_argument("--path", type=str, help="the path where the presentation is", default=".")

    plugin_command_parser = plugin_subparsers.add_parser("command", help="execute a custom command of the plugin",
                                                         aliases=["c"])
    plugin_command_parser.add_argument("name", type=str, help="the name of the plugin")
    plugin_command_parser.add_argument("--path", type=str, help="the path where the presentation is",
                                       default=".")

    plugin_help_parser = plugin_subparsers.add_parser("help", help="get the help of a plugin", aliases=["h"])
    plugin_help_parser.add_argument("name", type=str, help="the name of the plugin")

    _plugin_list_parser = plugin_subparsers.add_parser("list", help="list all plugins", aliases=["l", "ls"])

    _help_parser = subparsers.add_parser("help", aliases=["h"])

    args = parser.parse_args()
    if args.subcommand in ["create", "c"]:
        create(args.path, DATA_DIR, args.name)
    elif args.subcommand in ["plugin", "p"]:
        if args.plugin_subcommand in ["add", "a"]:
            plugin = args.name.lower()
            check_plugin(plugin, custom="all")
            file = join(args.path, "index.html")
            if not exists(file):
                print(f"file {file} not found")
                exit(1)
            plugins.add(plugin, file, DATA_DIR)
        elif args.plugin_subcommand in ["help", "h"]:
            plugin = args.name.lower()
            check_plugin(plugin)
            plugins.plugin_help(plugin)
        elif args.plugin_subcommand in ["command", "c"]:
            plugin = args.name.lower()
            check_plugin(plugin)
            file = join(args.path, "index.html")
            if not exists(file):
                print(f"file {file} not found")
                exit(1)
            plugins.command(plugin, file, DATA_DIR)
        elif args.plugin_subcommand in ["list", "ls", "l"]:
            all_plugins = " ".join(plugins.PLUGINS.keys())
            print(f"Available plugins: \n{all_plugins}")
        else:
            # no valid subcommand recognized
            parser.print_help()
    else:
        # no valid subcommand recognized or help subcommand was used
        parser.print_help()


def check_plugin(plugin, *, custom=None):
    """
    check if plugin is a valid plugin and exits if not
    :param plugin: the name of the plugin
    :param custom: a additional plugin name
    """
    if custom and plugin == custom:
        return
    if plugin not in plugins.PLUGINS:
        all_plugins = " ".join(plugins.PLUGINS.keys())
        print(f"Plugin {plugin} not found. Try one of these:\n{all_plugins}")
        exit(1)


if __name__ == "__main__":
    main()
