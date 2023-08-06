# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['evo_ingress', 'evo_ingress.src']

package_data = \
{'': ['*'], 'evo_ingress.src': ['queue/*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0', 'argh>=0.26.2,<0.27.0', 'watchdog>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'evo-ingress',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Moishe Keselman',
    'author_email': 'shimoshik@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
