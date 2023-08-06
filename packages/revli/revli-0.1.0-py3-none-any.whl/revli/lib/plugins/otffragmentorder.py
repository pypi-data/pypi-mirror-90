from os.path import join

from revli.lib.plugins.plugin import Plugin


class OTFFragmentOrder(Plugin):
    def add(self):
        self.add_attr_to_initialize("otfFragmentOrder", True)
        self.add_dependency(join("otf-fragment-order", "otf-fragment-order.js"))
