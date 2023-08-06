from os.path import join, exists
from os import mkdir
from shutil import copy2, copytree


def create(location, data_dir, name="reveal.js"):
    """
    create a reveal.js presentation

    :param location: The location the presentation should be created
    :param data_dir: The directory of the data of reveal.js and the plugins
    :param name: The name of the folder
    """
    if not exists(location):
        raise OSError("Path does not exist")
    dst = join(location, name)
    if not exists(dst):
        mkdir(dst)
    else:
        raise RuntimeError("destination already exists")

    # copy the HTML page
    copy2(join(data_dir, "reveal.js", "index.html"), dst)

    # copy its dependencies
    copytree(join(data_dir, "reveal.js", "dist"), join(dst, "dist"))

    # copy the standard plugins
    mkdir(join(dst, "plugin"))
    for plugin in ["notes", "markdown", "highlight"]:
        src = join(data_dir, "reveal.js", "plugin", plugin)
        copytree(src, join(dst, "plugin", plugin))
