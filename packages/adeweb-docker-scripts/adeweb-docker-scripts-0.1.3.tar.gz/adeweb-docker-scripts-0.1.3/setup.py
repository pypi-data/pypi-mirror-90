# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['adeweb_docker_scripts']

package_data = \
{'': ['*']}

install_requires = \
['docker>=4.4.1,<5.0.0',
 'humanize>=3.2.0,<4.0.0',
 'rich>=9.5.1,<10.0.0',
 'typer>=0.3.2,<0.4.0']

entry_points = \
{'console_scripts': ['hdock = adeweb_docker_scripts.main:app']}

setup_kwargs = {
    'name': 'adeweb-docker-scripts',
    'version': '0.1.3',
    'description': 'Various Docker scripts to facilitate server management and apps debugging',
    'long_description': "Adeweb's docker scripts\n==============================\n\nVarious Docker scripts to facilitate server management and apps debugging.\n\n*Disclaimer: this is intented for internal use and may not be generic enough for you.*\n",
    'author': 'Antoine Duchene',
    'author_email': 'antoineduchene@icloud.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/adeweb-be/adeweb-docker-scripts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
