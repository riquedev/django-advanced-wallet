# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import sys, os
from pathlib import Path
import django

ROOT = Path(__file__).parent.parent.parent
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example_app.app.settings')
django.setup()
sys.path.insert(0, str(ROOT / 'django_advanced_wallet'))

project = 'django_advanced_wallet'
copyright = '2023, Henrique da Silva Santos'
author = 'Henrique da Silva Santos'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
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