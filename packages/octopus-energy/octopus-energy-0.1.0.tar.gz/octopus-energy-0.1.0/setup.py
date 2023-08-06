# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopus_energy']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8.1,<3.0.0', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'octopus-energy',
    'version': '0.1.0',
    'description': 'Python client for the Octopus Energy RESTful API',
    'long_description': None,
    'author': 'Mark Allanson',
    'author_email': 'mark@allanson.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
