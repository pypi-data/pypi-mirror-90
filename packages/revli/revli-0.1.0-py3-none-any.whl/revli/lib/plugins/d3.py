from revli.lib.plugins.plugin import Plugin


class D3(Plugin):
    def add(self):
        self.add_dependency("reveald3.js")
