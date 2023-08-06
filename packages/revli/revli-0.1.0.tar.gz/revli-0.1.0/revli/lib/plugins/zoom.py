from revli.lib.plugins.plugin import Plugin
from os.path import join


class Zoom(Plugin):
    def add(self):
        self.add_script(join("reveal.js", "plugin", "zoom", "zoom.js"))
        self.add_plugin_def("RevealZoom")
