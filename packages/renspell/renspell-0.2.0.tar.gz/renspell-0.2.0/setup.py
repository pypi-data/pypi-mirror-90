# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['renspell']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'colorama>=0.4.4,<0.5.0',
 'language-tool-python>=2.4.7,<3.0.0']

entry_points = \
{'console_scripts': ['renspell = renspell.main:main']}

setup_kwargs = {
    'name': 'renspell',
    'version': '0.2.0',
    'description': "A spell-checker for Ren'Py scripts",
    'long_description': None,
    'author': 'Harlan Lieberman-Berg',
    'author_email': 'hlieberman@setec.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
