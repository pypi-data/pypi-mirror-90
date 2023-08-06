import os
import re
import sys

sys.path.insert(0, os.path.abspath(".."))


def get_version():
    scriptdir = os.path.dirname(os.path.abspath(__file__))
    init_py_path = os.path.join(scriptdir, "..", "hspatial", "__init__.py")
    with open(init_py_path) as f:
        return re.search(r'^__version__ = "(.*?)"$', f.read(), re.MULTILINE).group(1)


extensions = ["sphinx.ext.autodoc", "sphinx.ext.viewcode"]
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"
project = "hspatial"
copyright = "2019, Antonis Christofides"
author = "Antonis Christofides"
version = get_version()
release = version
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
html_theme = "alabaster"
html_static_path = ["_static"]
htmlhelp_basename = "hspatial"
latex_elements = {}
latex_documents = [
    (
        master_doc,
        "hspatial.tex",
        "hspatial Documentation",
        "Antonis Christofides",
        "manual",
    )
]
texinfo_documents = [
    (
        master_doc,
        "hspatial",
        "hspatial Documentation",
        author,
        "hspatial",
        "One line description of project.",
        "Miscellaneous",
    )
]


def setup(app):
    app.add_object_type(
        "confval",
        "confval",
        objname="configuration value",
        indextemplate="pair: %s; configuration value",
    )
