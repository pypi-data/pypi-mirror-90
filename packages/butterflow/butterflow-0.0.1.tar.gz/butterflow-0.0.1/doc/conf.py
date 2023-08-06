# butterflow documentation build configuration file.
import butterflow as root


# -- General configuration ------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
]

templates_path = ["_templates"]
source_suffix = [".rst"]
master_doc = "index"

# General information about the project.
project = "butterflow"
author = "Kristian Boda"
copyright = f"2020, {author}"

# The short X.Y version.
version = root.__version__
# The full version, including alpha/beta/rc tags.
release = root.__release__

language = None
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = True


# -- Options for HTML output ----------------------------------------------

html_theme = "alabaster"

html_theme_options = {
    # Alabaster theme configuration.
    "page_width": "75%",
}

html_static_path = ["_static"]
html_show_copyright = True


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "10pt",
    "figure_align": "htbp",
}

latex_documents = [
    (master_doc, "butterflow.tex", "butterflow documentation", author, "manual")
]
