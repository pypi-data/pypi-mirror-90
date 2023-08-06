# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['kkpyutil']
setup_kwargs = {
    'name': 'kkpyutil',
    'version': '0.1.0',
    'description': 'Personal utility functions and classes frequently used by myself for daily Python work.',
    'long_description': '# kkpyutil\nPersonal utility functions and classes frequently used by myself for daily Python work.\n\nIt does not necessarily benefit everybody, but I hope it may occasionally shed light on some issues you may have in your own work.\n',
    'author': 'Beinan Li',
    'author_email': 'li.beinan@gmail.com',
    'maintainer': 'Todd Birchard',
    'maintainer_email': 'toddbirchard@gmail.com',
    'url': 'https://github.com/kakyoism/kkpyutil/',
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
