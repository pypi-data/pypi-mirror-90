# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['zc']
setup_kwargs = {
    'name': 'zc',
    'version': '0.1.1',
    'description': 'Zencity opensourced utilities',
    'long_description': None,
    'author': 'Yehuda Deutsch',
    'author_email': 'yeh@uda.co.il',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
