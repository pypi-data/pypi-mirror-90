# revli
revli is a cli tool to create reveal.js presentations and manage their plugins

This tool is still in development. Everything can change!

# Installation:
`pip install revli`

# Usage:
- create a new presentation:
`revli create [--path path] [--name name]`
    - `name` is the name of the presentation
    - `path` is the path where the folder `name` containing the presentation should be created

- cd in the new directory
`cd reveal.js` or `cd <name>` if a custom name was used in the creation

- get all available plugins:
`revli plugin list`

- add a plugin to the presentation:
`revli plugin add <plugin_name>`
    - `plugin_name` is the name of the plugin

- open `index.html`

# Plugins
* [Multiplex](https://github.com/reveal/multiplex)
* [Chart](https://github.com/rajgoel/reveal.js-plugins/tree/master/chart)
* [ChalkBoard](https://github.com/rajgoel/reveal.js-plugins/tree/master/chalkboard)
* [Mapbox](https://github.com/lipov3cz3k/reveal.js-mapbox-gl-plugin)
* [OnTheFly Fragment Order](https://github.com/Sonaryr/reveal.js-otf-fragment-order)
* [d3](https://github.com/gcalmettes/reveal.js-d3)
* [TagCloud](https://github.com/sebhildebrandt/reveal.js-tagcloud-plugin)

# License
MIT licensed
Copyright (C) 2020 Akida31