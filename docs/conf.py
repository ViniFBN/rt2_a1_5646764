# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
sys.path.insert(0, os.path.abspath('../vinicius_assignment_2_rt1/scripts/'))
sys.path.insert(1, os.path.abspath('../../devel/lib/python3/dist-packages/'))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'S5646764_rt2_a1'
copyright = '2023, Vinícius Ferreira'
author = 'Vinícius Ferreira'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
    "sphinx.ext.napoleon",
    'sphinx.ext.inheritance_diagram',
    'breathe'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for intersphinx extension ---------------------------------------
# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

highlight_language = 'py'
source_suffix = '.rst'
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
master_doc = 'index'

# -- Options for breathe
breathe_projects = {
"S5646764_rt2_a1": "../docs/xml/"
}
breathe_default_project = "S5646764_rt2_a1"
breathe_default_members = ('members', 'undoc-members')

intersphinx_mapping = {'https://docs.python.org/': None}
