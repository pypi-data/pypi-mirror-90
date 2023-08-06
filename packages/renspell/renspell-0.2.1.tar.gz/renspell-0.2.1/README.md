renspell is a utility for performing spelling and grammatical checking
on [Ren'Py](https://www.renpy.org/) scripts.

# Installation

renspell can be installed by running `pip install renspell`. It requires
Python 3.5+ and Java JRE 8.0+.

LanguageTool will be automatically downloaded and installed upon the
first run.

# Usage

renspell is a command line utility. To use it, run `renspell
PATH_TO_FILE_OR_DIR_TO_CHECK`. For example, if I wanted to check a
script called 'script.rpy', I would do:

``` shell
renspell game/script.rpy
```

A full list of options can be found by running `renspell --help`.

renspell supports all languages which
[LanguageTool](https://languagetool.org/) does. An abbreviated list is:

| Language                  | Language Code |
| ------------------------- | ------------- |
| English (USA) \[DEFAULT\] | en-US         |
| English (Australia)       | en-AU         |
| English (United Kingdom)  | en-GB         |
| English (Canada)          | en-CA         |
| English (New Zealand)     | en-NZ         |
| Arabic                    | ar            |
| Belarusian                | be            |
| Catalan                   | ca            |
| Chinese                   | zh            |
| Danish                    | da            |
| Dutch (Belgium)           | nl-BE         |
| Dutch (Netherlands)       | nl-NL         |
| French                    | fr            |
| Galician                  | gl            |
| German                    | de            |
| Greek                     | el            |
| Icelandic                 | is            |
| Irish                     | ga            |
| Italian                   | it            |
| Japanese                  | ja            |
| Khmer                     | km            |
| Lithuanian                | lt            |
| Malayalam                 | ml            |
| Persian                   | fa            |
| Polish                    | pl            |
| Portuguese (Angola)       | pt-AO         |
| Portuguese (Brazil)       | pt-BR         |
| Portuguese (Mozambique)   | pt-MZ         |
| Portuguese (Portugal)     | pt-PT         |
| Romanian                  | ro            |
| Russian                   | ru            |
| Serbian                   | sr            |
| Slovak                    | sk            |
| Slovenian                 | sl            |
| Spanish                   | es            |
| Swedish                   | sv            |
| Tagalog                   | tl            |
| Tamil                     | ta            |
| Ukranian                  | uk            |

# Getting Help

If one of your scripts is causing renspell to have errors, please open
[an issue](https://gitlab.com/hlieberman/renspell/-/issues). If
possible, please include the script file that is causing the errors. If
you don't feel comfortable doing that, open the issue and tag
@hlieberman in the issue to get information necessary for submitting it
privately.

For more interactive, you may join the [Ren'Py
Discord](https://discord.gg/6ckxWYm) and ask for help there.

# Contributing

renspell is free and open source software, and we happily accept
contributions of all sorts, including code, design help, and
documentation. [Issues tagged
'newcomer'](https://gitlab.com/hlieberman/renspell/-/issues?label_name%5B%5D=newcomer)
are good places to start. Before starting anything that requires
significant architecture, please open an issue or check in with
@hlieberman on the [Ren'Py Discord](https://discord.gg/6ckxWYm).

Please sign-off on your commits (`git commit -s`). By doing so, you
certify that you have the right to submit the work under the license of
renspell (GPLv3), and that you agree to a [Developer Certificate of
Origin](https://developercertificate.org/).

# License and Copyright

renspell is copyright 2020-2021, Harlan Lieberman-Berg
\<hlieberman@setec.io\> and renspell contributors.

renspell is free software, licensed under the terms of the [GNU General
Public License](./LICENSE), version 3.0.
