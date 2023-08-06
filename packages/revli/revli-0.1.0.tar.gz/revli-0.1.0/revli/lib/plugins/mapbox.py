from revli.lib.plugins.plugin import Plugin, quote_js_str


class Mapbox(Plugin):
    def add(self):
        self.add_dependency("https://api.tiles.mapbox.com/mapbox-gl-js/v0.46.0/mapbox-gl.js",
                            external=True)
        self.add_dependency("mapbox-gl.js")
        token = input("Mapbox AccessToken: ")
        self.add_attr_to_initialize("mapbox", {"accessToken": quote_js_str(token)})
