import json
from os.path import join, dirname, basename, relpath
from shutil import copy2, copytree

from _chompjs import parse
from bs4 import BeautifulSoup


def _parse_initialize(initialize):
    """
    parse the initialization of Reveal.js
    :param initialize: the params given in the HTML-Doc
    :return: the parsed initialization
    """
    lines = []
    # parse the input
    for line in initialize.strip().rstrip(");").splitlines():
        line = line.strip()
        # remove all comments in a new line
        if not line.startswith("//"):
            lines.append(line)
    return "".join(lines)


def _dump_json(text):
    """
    dump a dict to JS Object
    :param text: the dict
    :return: string of the JS Object
    """
    text = json.dumps(text)
    ret_text = ""
    last_char = ""
    for char in text:
        if char != '"' and last_char != "\\":
            ret_text += char
        last_char = char
    return ret_text


def _loads_json(text):
    """
    load a dict from a JS Object string
    :param text: the string which should be loaded
    :return: the dict
    """
    # Double all Quotes because the should stay in the String
    new_text = ""
    open_single_quotes = False
    open_double_quotes = False
    for char in text:
        if char == "'":
            if open_single_quotes:
                char = "\\''"
            else:
                char = "'\\'"
            open_single_quotes = not open_single_quotes
        elif char == '"':
            if open_double_quotes:
                char = '\\""'
            else:
                char = '"\\"'
            open_double_quotes = not open_double_quotes
        new_text += char
    # remove commas in the end of arrays
    new_text = new_text.replace(",]", "]")
    new_text = parse(new_text)
    new_text = json.loads(new_text)
    return new_text


def quote_js_str(text, *, quotes="'"):
    """
    quote a string so that it will be later formatted correctly
    :param text: the string which should be formatted
    :param quotes: the type of quotes which should be used
    :return: the formatted text
    """
    return f"{quotes}{text}{quotes}"


class Plugin:
    """
    the baseclass for all plugins.
    All plugins must implement the add method and can use all the methods of this class for it
    """

    def __init__(self, file, data_dir):
        self.file = file
        self.data_dir = data_dir
        with open(self.file, "r") as f:
            self.soup = BeautifulSoup(f, "html.parser")

    def add_script(self, src, copy_script=True):
        """
        add a plugin script at the end of the body
        :param src: the path of the plugin
        :param copy_script: if true the script will be copied to the new location
        """
        name = basename(src)
        src = join(self.data_dir, src)
        if not copy_script:
            self.soup.body.append(f'<script src="{src}"></script>')
            return
        path = join(dirname(self.file), "plugin")
        dst = join(path, name)
        copy2(src, dst)

        # use relative import
        dst = relpath(dst, dirname(self.file))
        dst = dst.replace("\\", "/")  # don't use windows pathing in HTML
        new_tag = self.soup.new_tag("script", src=dst)
        self.get_initialize_tag().insert_before(new_tag)

    def add_stylesheet(self, src):
        """
        add a stylesheet at the end of the head
        :param src: the src address of the stylesheet
        """
        new_tag = self.soup.new_tag("link", rel="stylesheet", href=src)
        self.soup.head.append(new_tag)

    def add_plugin_def(self, name):
        """
        add a plugin name to the list of plugins
        :param name: the name of the plugin
        """
        ini = self.get_initialize()
        ini["plugins"].append(name)
        self.write_initialize(ini)

    def add_dependency(self, src, *, is_async=True, external=False):
        """
        add a dependency to the list of dependencies in the initialization of reveal.js
        :param src: the src of the dependency
        :param is_async: the loading method of the plugin later in reveal.js
        :param external: if external the dependency won't be copied
        """
        # TODO dependencies are deprecated, use normal scripts instead
        if not external:
            name = basename(src)
            src = join(self.data_dir, src)
            path = join(dirname(self.file), "plugin")
            dst = join(path, name)
            copy2(src, dst)
            # use relative import
            dst = relpath(dst, dirname(self.file))
            dst = dst.replace("\\", "/")  # don't use windows pathing in HTML
        else:
            dst = src

        ini = self.get_initialize()
        if "dependencies" not in ini:
            ini["dependencies"] = []
        if is_async:
            async_text = ", async: true"
        else:
            async_text = ""
        text = f"{{ src: '{dst}'{async_text} }},"
        ini["dependencies"].append(text)
        self.write_initialize(ini)

    def add_attr_to_initialize(self, key, value):
        """
        add an attribute to the Reveal.initialize config

        WARNING: all strings must be formatted using quote_js_str
        :param key: the key of the attribute
        :param value: the value of the attribute, should be a dict
        """
        ini = self.get_initialize()
        ini[key] = value
        self.write_initialize(ini)

    def get_initialize_tag(self):
        """
        get the initialization tag
        """
        for script in self.soup.find_all("script"):
            text = script.string
            if text is not None and "Reveal.initialize" in text:
                return script
        raise ValueError("Reveal.initialize not found")

    def get_initialize(self):
        """
        get the initialize of the presentation
        :return: a dict of all attrs
        """
        text = self.get_initialize_tag().string
        texts = text.split("Reveal.initialize(")
        for text in texts:
            # TODO: use better way to determine the right text
            if "plugins" in text:
                lines = _parse_initialize(text)
                lines = _loads_json(lines)
                return lines

    def write_initialize(self, initialize):
        """
        write the initialize of the presentation
        :param initialize: a dict of all attrs
        """
        initialize = _dump_json(initialize)
        self.get_initialize_tag().string = f"Reveal.initialize({initialize});"

    def copy_dir(self, src, dst):
        """
        copy a directory to the presentation
        :param src: the src path of the directory in the DATA_DIR
        :param dst: the destination path in the presentation/plugin directory
        """
        path = join(dirname(self.file), "plugin")
        copytree(join(self.data_dir, src), join(path, dst))

    def add(self):
        """
        add the plugin to the file
        """
        raise NotImplementedError

    def write(self):
        """
        write the changes to the file
        """
        with open(self.file, "w") as f:
            f.write(self.soup.prettify())

    @staticmethod
    def help():
        """
        show the help of the plugin
        """
        print("no additional help for this plugin available")
        exit(1)

    def command(self):
        """
        execute a command gotten of a cli
        """
        print("no command for this plugin available")
        exit(1)
