# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['azureipcheck']

package_data = \
{'': ['*']}

install_requires = \
['click-help-colors>=0.9,<0.10',
 'clumper>=0.2.7,<0.3.0',
 'gazpacho>=1.1,<2.0',
 'rich>=9.3.0,<10.0.0',
 'typer[all]>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['azureipcheck = azureipcheck.main:app']}

setup_kwargs = {
    'name': 'azureipcheck',
    'version': '1.0.0',
    'description': 'A Python CLI tool to check service tags for Azure IPs',
    'long_description': '# azureipcheck\n\n<div align="center">\n    <img src="https://img.shields.io/pypi/v/azureipcheck"/>\n    <img src="https://img.shields.io/pypi/pyversions/azureipcheck"/>\n    <img src="https://img.shields.io/pypi/l/azureipcheck"/>\n    <a href="https://twitter.com/mcohmi"><img src="https://img.shields.io/twitter/follow/mcohmi.svg?style=plastic"/></a><br>\n</div>\n\nA Python [Typer-based](https://github.com/tiangolo/typer) CLI tool to check IP addresses against Azure services. It also uses [Rich](https://github.com/willmcgugan/rich) for some dope console output. Additionally, it makes use of [Clumper](https://github.com/koaning/clumper) for parsing through the Azure Service Tag JSON files.\n\n\n## Installation\n\nThe recommended method of installation is with [pipx](https://github.com/pipxproject/pipx). \n\n```\npipx install azureipcheck\n```\n\nHowever, you can install the normal way from PyPi with `python3 -m pip install azureipcheck`.\n\n## Usage\n\nYou should first run `azureipcheck update` to download the latest Service Tag JSON files. After downloading the files locally, you can run `azureipcheck check <ip>`, where `ip` can be a single address or CIDR (i.e., `51.8.227.233` or `51.8.227.233/24`). \n\nChecking a CIDR does not check every IP in the network provided. It simply checks to see if the network is in a subnet of any of the Azure network ranges. Therefore `51.8.227.233/24` may return matches but `51.8.227.233/8` would not. \n\n\n### Built With\n- Typer: https://github.com/tiangolo/typer\n- Rich: https://github.com/willmcgugan/rich\n- Clumper: https://github.com/koaning/clumper\n- Gazpacho: https://github.com/maxhumber/gazpacho\n- Cookiecutter-RichTyper: https://github.com/daddycocoaman/cookiecutter-richtyper\n\nInspired by https://github.com/deanobalino/azureip\n\n\n',
    'author': 'Leron Gray',
    'author_email': None,
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
