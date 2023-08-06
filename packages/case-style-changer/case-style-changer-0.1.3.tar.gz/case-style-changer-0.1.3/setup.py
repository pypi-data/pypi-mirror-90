# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['case_style_changer']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['case_style_changer = case_style_changer.cli:main',
                     'csc = case_style_changer.cli:main']}

setup_kwargs = {
    'name': 'case-style-changer',
    'version': '0.1.3',
    'description': 'Case Style Changer - a CLI tool that guesses the case of the input string and converts it to another case.',
    'long_description': '# Case Style Changer\n\n[![PyPi][pypi-version]][pypi] [![Python Version][python-version]][pypi] [![GitHub Workflow Status][actions-status]][actions] [![codecov][codecov-status]][codecov] [![Code Climate][codeclimate-status]][codeclimate] [![License][license]][license-file]\n\nCase Style Changer is a CLI tool that guesses the case of the input string and converts it to another case.\n\n## Installation\n\nInstall and update using [pip](https://pip.pypa.io/en/stable/quickstart/):\n\n``` sh\npip install case-style-changer\n```\n\nFor macOS user, you can install and update using [brew](https://brew.sh/):\n\n``` sh\nbrew tap xkumiyu/homebrew-case-style-changer\nbrew install case-style-changer\n```\n\n## Usage\n\n``` sh\n$ csc [--text TEXT] CASE_NAME\n```\n\n`CASE_NAME` is the name of the case you want to convert.\n\n### Examples\n\nYou can use standard input or arguments.\n\n``` sh\n$ echo "case-style-changer" | csc camel\ncaseStyleChanger\n```\n\n``` sh\n$ csc snake --text "caseStyleChanger"\ncase_style_changer\n```\n\n### Available case style\n\nThe available case styles are:\n\n| Case Name | Case Name Alias | Example |\n|:--|:--|:--|\n| `camel_case` | `camel`, `lower_camel_case`, `lcc` | caseStyleChanger |\n| `pascal_case` | `pascal`, `pascal_case`, `upper_camel_case`, `ucc` | CaseStyleChanger |\n| `snake_case` | `snake`, `lower_snake_case`, `lsc` | case_style_changer |\n| `constant_case` | `constant`, `constant_case`, `screaming`, `screaming_snake_case`, `upper_snake_case`, `upper_case`, `usc`, `ssc` | CASE_STYLE_CHANGER |\n| `kebab_case` | `kebab`, `kebab_case`, `chain`, `chain_case` | case-style-changer |\n| `sentence_case` | `sentence` | Case style changer |\n| `capital_case` | `capital`,`train`, `train_case` | Case Style Changer |\n\n## Change Log\n\nSee [Change Log](CHANGELOG.md).\n\n## Licence\n\nMIT: [LICENCE](LICENSE)\n\n[pypi]: https://pypi.org/project/case-style-changer\n[pypi-version]: https://img.shields.io/pypi/v/case-style-changer\n[python-version]: https://img.shields.io/pypi/pyversions/case-style-changer\n[actions]: https://github.com/xkumiyu/case-style-changer/actions\n[actions-status]: https://img.shields.io/github/workflow/status/xkumiyu/case-style-changer/Python%20package\n[codecov]: https://codecov.io/gh/xkumiyu/case-style-changer\n[codecov-status]: https://img.shields.io/codecov/c/github/xkumiyu/case-style-changer\n[codeclimate]: https://img.shields.io/codeclimate/maintainability/xkumiyu/case-style-changer\n[codeclimate-status]: https://img.shields.io/codeclimate/maintainability/xkumiyu/case-style-changer\n[license]: https://img.shields.io/github/license/xkumiyu/case-style-changer\n[license-file]: https://github.com/xkumiyu/case-style-changer/blob/master/LICENSE\n',
    'author': 'xkumiyu',
    'author_email': 'xkumiyu@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/xkumiyu/case-style-changer',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
