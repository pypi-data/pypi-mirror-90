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
    'version': '0.2.1',
    'description': "A spell-checker for Ren'Py scripts",
    'long_description': "renspell is a utility for performing spelling and grammatical checking\non [Ren'Py](https://www.renpy.org/) scripts.\n\n# Installation\n\nrenspell can be installed by running `pip install renspell`. It requires\nPython 3.5+ and Java JRE 8.0+.\n\nLanguageTool will be automatically downloaded and installed upon the\nfirst run.\n\n# Usage\n\nrenspell is a command line utility. To use it, run `renspell\nPATH_TO_FILE_OR_DIR_TO_CHECK`. For example, if I wanted to check a\nscript called 'script.rpy', I would do:\n\n``` shell\nrenspell game/script.rpy\n```\n\nA full list of options can be found by running `renspell --help`.\n\nrenspell supports all languages which\n[LanguageTool](https://languagetool.org/) does. An abbreviated list is:\n\n| Language                  | Language Code |\n| ------------------------- | ------------- |\n| English (USA) \\[DEFAULT\\] | en-US         |\n| English (Australia)       | en-AU         |\n| English (United Kingdom)  | en-GB         |\n| English (Canada)          | en-CA         |\n| English (New Zealand)     | en-NZ         |\n| Arabic                    | ar            |\n| Belarusian                | be            |\n| Catalan                   | ca            |\n| Chinese                   | zh            |\n| Danish                    | da            |\n| Dutch (Belgium)           | nl-BE         |\n| Dutch (Netherlands)       | nl-NL         |\n| French                    | fr            |\n| Galician                  | gl            |\n| German                    | de            |\n| Greek                     | el            |\n| Icelandic                 | is            |\n| Irish                     | ga            |\n| Italian                   | it            |\n| Japanese                  | ja            |\n| Khmer                     | km            |\n| Lithuanian                | lt            |\n| Malayalam                 | ml            |\n| Persian                   | fa            |\n| Polish                    | pl            |\n| Portuguese (Angola)       | pt-AO         |\n| Portuguese (Brazil)       | pt-BR         |\n| Portuguese (Mozambique)   | pt-MZ         |\n| Portuguese (Portugal)     | pt-PT         |\n| Romanian                  | ro            |\n| Russian                   | ru            |\n| Serbian                   | sr            |\n| Slovak                    | sk            |\n| Slovenian                 | sl            |\n| Spanish                   | es            |\n| Swedish                   | sv            |\n| Tagalog                   | tl            |\n| Tamil                     | ta            |\n| Ukranian                  | uk            |\n\n# Getting Help\n\nIf one of your scripts is causing renspell to have errors, please open\n[an issue](https://gitlab.com/hlieberman/renspell/-/issues). If\npossible, please include the script file that is causing the errors. If\nyou don't feel comfortable doing that, open the issue and tag\n@hlieberman in the issue to get information necessary for submitting it\nprivately.\n\nFor more interactive, you may join the [Ren'Py\nDiscord](https://discord.gg/6ckxWYm) and ask for help there.\n\n# Contributing\n\nrenspell is free and open source software, and we happily accept\ncontributions of all sorts, including code, design help, and\ndocumentation. [Issues tagged\n'newcomer'](https://gitlab.com/hlieberman/renspell/-/issues?label_name%5B%5D=newcomer)\nare good places to start. Before starting anything that requires\nsignificant architecture, please open an issue or check in with\n@hlieberman on the [Ren'Py Discord](https://discord.gg/6ckxWYm).\n\nPlease sign-off on your commits (`git commit -s`). By doing so, you\ncertify that you have the right to submit the work under the license of\nrenspell (GPLv3), and that you agree to a [Developer Certificate of\nOrigin](https://developercertificate.org/).\n\n# License and Copyright\n\nrenspell is copyright 2020-2021, Harlan Lieberman-Berg\n\\<hlieberman@setec.io\\> and renspell contributors.\n\nrenspell is free software, licensed under the terms of the [GNU General\nPublic License](./LICENSE), version 3.0.\n",
    'author': 'Harlan Lieberman-Berg',
    'author_email': 'hlieberman@setec.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/hlieberman/renspell',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
