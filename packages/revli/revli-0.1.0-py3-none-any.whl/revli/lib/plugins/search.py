from revli.lib.plugins.plugin import Plugin
from os.path import join


class Search(Plugin):
    def add(self):
        self.add_script(join("reveal.js", "plugin", "search", "search.js"))
        self.add_plugin_def("RevealSearch")
