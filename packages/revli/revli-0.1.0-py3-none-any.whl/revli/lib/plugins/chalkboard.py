from os.path import join

from revli.lib.plugins.plugin import Plugin


class ChalkBoard(Plugin):
    def add(self):
        self.add_script(join("chalkboard", "chalkboard.js"))
        self.copy_dir(join("chalkboard", "img"), "img")
        self.add_stylesheet("https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css")
        self.add_plugin_def("RevealChalkboard")
