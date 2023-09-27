# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys, os
from pathlib import Path

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT))

project = 'django_advanced_wallet'
copyright = '2023, Henrique da Silva Santos'
author = 'Henrique da Silva Santos'
release = '0.0.2'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    "sphinxcontrib_django",
]

autodoc_mock_imports = ['django']

templates_path = ['_templates']
exclude_patterns = [
    "*.migrations.rst"
]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']

django_settings = "example_app.app.settings"
django_show_db_tables = True
django_show_db_tables_abstract = True
django_choices_to_show = 10
