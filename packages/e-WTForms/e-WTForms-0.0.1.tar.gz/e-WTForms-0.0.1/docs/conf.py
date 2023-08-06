from pallets_sphinx_themes import get_version
from pallets_sphinx_themes import ProjectLink

# Project --------------------------------------------------------------

project = "e-WTForms"
copyright = "2021 e-WTForms"
author = "ennkua"
release, version = get_version("e-WTForms")

# General --------------------------------------------------------------

master_doc = "index"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "pallets_sphinx_themes",
    "sphinx_issues",
    "sphinxcontrib.log_cabinet",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
}
issues_github_path = "ennkua/e-wtforms"

# HTML -----------------------------------------------------------------

html_theme = "werkzeug"
html_context = {
    "project_links": [
        ProjectLink("PyPI Releases", "https://pypi.org/project/e-WTForms/"),
        ProjectLink("Source Code", "https://github.com/ennkua/e-wtforms/"),
        ProjectLink("Issue Tracker", "https://github.com/ennkua/e-wtforms/issues/"),
    ]
}
html_sidebars = {
    "index": ["project.html", "localtoc.html", "searchbox.html"],
    "**": ["localtoc.html", "relations.html", "searchbox.html"],
}
singlehtml_sidebars = {"index": ["project.html", "localtoc.html"]}
html_static_path = ["_static"]
html_logo = "_static/e-wtforms.png"
html_title = f"e-WTForms Documentation ({version})"
html_show_sourcelink = False

# LaTeX ----------------------------------------------------------------

latex_documents = [
    ("index", f"e-WTForms-{version}.tex", html_title, author, "manual"),
]
