# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['itstepweather']
setup_kwargs = {
    'name': 'itstepweather',
    'version': '0.1.0',
    'description': 'Simple weather module for ITStep students',
    'long_description': None,
    'author': 'Eugene',
    'author_email': 'coulderapid@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
