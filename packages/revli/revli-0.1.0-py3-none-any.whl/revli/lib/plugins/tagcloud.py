from revli.lib.plugins.plugin import Plugin


class Tagcloud(Plugin):
    def add(self):
        self.add_dependency("tagcloud.js")
