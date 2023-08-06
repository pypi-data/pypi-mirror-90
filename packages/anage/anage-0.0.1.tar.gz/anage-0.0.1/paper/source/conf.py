# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options.
# For a full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from anage import __version__

# Project information
project = 'anage'
copyright = '2021  Group 4'  # noqa
author = 'Group 4'
release = __version__

# Options for HTML output
html_theme = 'furo'

# Options for LaTeX
latex_elements = {
    'papersize': 'a4paper', 'pointsize': '12pt',
    'fontpkg': r'\usepackage{lmodern}',
    'babel': r'\usepackage[english,vietnamese]{babel}',
    'tableofcontents': r'\selectlanguage{english}\sphinxtableofcontents'}
