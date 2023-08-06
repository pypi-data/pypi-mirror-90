from revli.lib.plugins.plugin import Plugin
from os.path import join


class Math(Plugin):
    def add(self):
        self.add_script(join("reveal.js", "plugin", "math", "math.js"))
        self.add_plugin_def("RevealMath")
