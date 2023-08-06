# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['__init__']
install_requires = \
['numpy>=1.17.0,<2.0.0']

setup_kwargs = {
    'name': 'polyagamma',
    'version': '0.1.0a2',
    'description': "Efficiently sample from the Polya-Gamma distribution using NumPy's Generator interface",
    'long_description': None,
    'author': 'Zolisa Bleki',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
