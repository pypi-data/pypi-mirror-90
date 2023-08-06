from revli.lib.plugins.plugin import Plugin
from os.path import join


class Chart(Plugin):
    def add(self):
        self.add_script(join("chart", "chart_plugin.js"))
        self.add_script(join("chart", "Chart.min.js"))
        self.add_plugin_def("RevealChart")
