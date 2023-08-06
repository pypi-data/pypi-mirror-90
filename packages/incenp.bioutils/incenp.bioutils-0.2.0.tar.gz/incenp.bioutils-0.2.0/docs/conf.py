# -*- coding: utf-8 -*-

# -- Project information -----------------------------------------------------

project = 'Incenp.Bioutils'
copyright = '2021 Damien Goutte-Gattat'
author = 'Damien Goutte-Gattat <dgouttegattat@incenp.org>'

# -- General configuration ---------------------------------------------------

source_suffix = '.rst'
master_doc = 'index'

language = 'en'

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = 'sphinx'

extensions = [
        'sphinx.ext.autodoc'
]

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
