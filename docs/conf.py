# -*- coding: utf-8 -*-
"""django-downloadview documentation build configuration file."""

import re

import importlib.metadata

# Minimal Django settings. Required to use sphinx.ext.autodoc, because
# django-downloadview depends on Django...
from django.conf import settings

settings.configure(
    DATABASES={},  # Required to load ``django.views.generic``.
)


# -- General configuration ----------------------------------------------------

# Extensions.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.coverage",
    "sphinx.ext.intersphinx",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix of source filenames.
source_suffix = ".txt"

# The encoding of source files.
source_encoding = "utf-8"

# The master toctree document.
master_doc = "index"

# General information about the project.
project = "django-downloadview"
project_slug = re.sub(r"([\w_.-]+)", "-", project)
copyright = "2012-2015, Benoît Bryon"
author = "Benoît Bryon"
author_slug = re.sub(r"([\w_.-]+)", "-", author)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The full version, including alpha/beta/rc tags.
release = importlib.metadata.version("django-downloadview")
# The short X.Y version.
version = ".".join(release.split(".")[:2])

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
language = "en"

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ["_build"]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output --------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# Custom sidebar templates, maps document names to template names.
html_sidebars = {
    "**": ["globaltoc.html", "relations.html", "sourcelink.html", "searchbox.html"],
}

# Output file base name for HTML help builder.
htmlhelp_basename = "{project}doc".format(project=project_slug)


# -- Options for sphinx.ext.intersphinx ---------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "django": (
        "https://docs.djangoproject.com/en/3.1/",
        "https://docs.djangoproject.com/en/3.1/_objects/",
    ),
    "requests": ("https://requests.readthedocs.io/en/master/", None),
}


# -- Options for LaTeX output -------------------------------------------------

latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass
# [howto/manual]).
latex_documents = [
    (
        "index",
        "{project}.tex".format(project=project_slug),
        "{project} Documentation".format(project=project),
        author,
        "manual",
    ),
]


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    ("index", project, "{project} Documentation".format(project=project), [author], 1)
]


# -- Options for Texinfo output -----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        "index",
        project_slug,
        "{project} Documentation".format(project=project),
        author,
        project,
        "One line description of project.",
        "Miscellaneous",
    ),
]
