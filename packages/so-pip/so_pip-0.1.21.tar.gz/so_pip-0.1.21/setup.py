# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['so_pip',
 'so_pip._cache',
 'so_pip._vendor',
 'so_pip._vendor.find_imports',
 'so_pip._vendor.find_imports_cruft',
 'so_pip.api_clients',
 'so_pip.cli_clients',
 'so_pip.commands',
 'so_pip.language_guessing',
 'so_pip.models',
 'so_pip.parse_code',
 'so_pip.parse_python',
 'so_pip.pypi_query',
 'so_pip.random_names',
 'so_pip.random_names.etl',
 'so_pip.support_files',
 'so_pip.update_any',
 'so_pip.utils']

package_data = \
{'': ['*'],
 'so_pip': ['licenses/*', 'templates/*'],
 'so_pip._vendor': ['find_imports_cruft/LICENSE/*']}

install_requires = \
['2to3',
 'beautifulsoup4',
 'black',
 'html2text',
 'jinja2',
 'nbformat',
 'pip-upgrader',
 'pipreqs',
 'pur',
 'py-stackexchange',
 'pyflakes',
 'pypinfo',
 'pypistats',
 'pyrankvote',
 'python-dotenv',
 'pyupgrade',
 'requests',
 'stackapi',
 'stdlib-list']

entry_points = \
{'console_scripts': ['so_pip = so_pip.__main__:main']}

setup_kwargs = {
    'name': 'so-pip',
    'version': '0.1.21',
    'description': 'Generate packages from Stackoverflow answers',
    'long_description': "so_pip\n======\nEveryone copies code from StackOverflow, but no one is formalizing it.\n\nThis will vendorize the source code of question or answer into a folder and\ngenerate the accessory files to make it look like a python package.\n\nThe feature-set overlaps a bit with [cookie cutter, vendorizing libraries and\nstackoverflow search cli's](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md).\n\nInstallation\n------------\nRequires Python 3.7+, tested with 3.7, 3.8, 3.9\n```\ngit clone https://github.com/matthewdeanmartin/so_pip.git\npython -m venv venv\n. venv/Scripts/activate\npip install -r .config/requirements.txt\n# some tools can't co-exist in the same virtual environment\npipx install pylint\npipx install isort\npython -m so_pip --version\n```\nDocker support 1/2 implemented.\n```\ndocker build -t so_pip:latest .\n```\nUsage\n--------------\nConsider getting a [key](https://stackapps.com/apps/oauth/register) and adding a [.so_pip.ini file](https://github.com/matthewdeanmartin/so_pip/blob/main/.so_pip.ini) The app will make best efforts if you don't.\n```\n# Turn posts into nicely formated packages\n> so_pip vendorize my_name --question=31049648 | --answer=31049648\n> so_pip search --answer=31049648 --tags=python\n\n# Pip-like commands\n> so_pip uninstall | upgrade {package_name}\n> so_pip list | freeze\n```\n\nDocs\n-----\n* [Examples](https://github.com/matthewdeanmartin/so_pip/tree/main/examples)\n* [CLI](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/cli.md)\n* [Code reuse scanarios you see on StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/scenarios.md)\n* [Features](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/features.md)\n* [Security Considerations](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/security.md)\n* [Prior Art](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/prior_art.md) Similar and overlapping tools.\n* [Contributing *answers* to StackOverflow](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/contributing.md) AKA, fixing answers you found.\n* [Attribution Compliance](https://github.com/matthewdeanmartin/so_pip/blob/main/docs/comply_with_cc_sa.md)\n* [Contributing to so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CONTRIBUTING.md)\n* [Code of Conduct for so_pip](https://github.com/matthewdeanmartin/so_pip/blob/main/CODE_OF_CONDUCT.md)\n",
    'author': 'Matthew Martin',
    'author_email': 'matthewdeanmartin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/matthewdeanmartin/so_pip',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
