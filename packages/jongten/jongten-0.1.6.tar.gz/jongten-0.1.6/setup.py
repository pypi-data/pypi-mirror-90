# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['jongten']
install_requires = \
['mahjong>=1.1.11,<2.0.0']

entry_points = \
{'console_scripts': ['jongten = jongten:main']}

setup_kwargs = {
    'name': 'jongten',
    'version': '0.1.6',
    'description': 'CLI trainer for calculating riichi-mahjong points',
    'long_description': '🧮🀄️jongten🀄️🧮\n=========\n\nCLI trainer for calculating riichi-mahjong points🀄️\n\n[![PyPI version](https://badge.fury.io/py/jongten.svg)](https://badge.fury.io/py/jongten)\n[![Python Versions](https://img.shields.io/pypi/pyversions/jongten.svg)](https://pypi.org/project/jongten/)\n\n<!-- toc -->\n- [🧮🀄️jongten🀄️🧮](#️jongten️)\n- [Usage](#usage)\n<!-- tocstop -->\n\n# Usage\n<!-- usage -->\n```sh-session\n🐑🌙 jongten\n🀚 🀚 🀇 🀈 🀉 🀉 🀊 🀋 🀝 🀞 🀟 🀒 🀓 🀔\n\nツモ:🀔 リーチ無 場風: 東 自風: 南\n親の支払う点数: 700\n子の支払う点数: 400\n\n正解!!\n```\n<!-- usagestop -->\n',
    'author': 'odmishien',
    'author_email': 'tmtm.yagi.007@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'http://github.com/odmishien/jongten',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
