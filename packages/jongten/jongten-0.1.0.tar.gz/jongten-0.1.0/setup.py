# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['jongten']
install_requires = \
['mahjong>=1.1.11,<2.0.0']

entry_points = \
{'console_scripts': ['jongten = jongten:main']}

setup_kwargs = {
    'name': 'jongten',
    'version': '0.1.0',
    'description': 'CLI trainer for calculating riichi-mahjong points',
    'long_description': None,
    'author': 'odmishien',
    'author_email': 'tmtm.yagi.007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
