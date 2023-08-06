# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['octopus_energy']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7.1,<4.0.0', 'furl>=2.1.0,<3.0.0', 'python-dateutil>=2.8.1,<3.0.0']

setup_kwargs = {
    'name': 'octopus-energy',
    'version': '0.1.4',
    'description': 'Python client for the Octopus Energy RESTful API',
    'long_description': '# Octopus Energy Python API Client Library\nA Client library for accessing the Octopus Energy APIs\n\n***Warning: The API is currently undergoing active development and should be considered unstable,\neven volatile until it reaches version 1.0.0***\n\n[![PyPI version](https://badge.fury.io/py/octopus-energy.svg)](https://badge.fury.io/py/octopus-energy)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/octopus-energy)\n\n[![Build Status](https://travis-ci.com/markallanson/octopus-energy.svg?branch=main)](https://travis-ci.com/markallanson/octopus-energy)\n[![Coverage Status](https://coveralls.io/repos/github/markallanson/octopus-energy/badge.svg?branch=main)](https://coveralls.io/github/markallanson/octopus-energy?branch=main)\n\n## Installation\n`octopus-energy` can be installed from PyPI using pip:\n\n```shell\npip install octopus-energy\n```\n\n## Code\nThe code is available in the [octopus-energy repository on GitHub][github]\n\n## Features\n\n* Get energy consumption from SMETS1 and SMETS2 electricity and gas meters.\n\n## Quickstart\nYou can obtain your API token and meter information from the [Octopus Energy Developer \nDashboard][octo dashboard].\n\n### REST Client Wrapper\nThe REST client wrapper is a slim shim over the REST API that returns dictionaries as responses. This is perfect if you\nwant something quick and dirty.\n\n```python\nfrom octopus_energy import OctopusEnergyRestClient\n\napi_token="sk_live_your-token"\nmprn = "your-mprn"\nserial_number = "your-meter-serial-number"\n\nclient = OctopusEnergyClient(api_token)\nconsumption = await client.get_gas_consumption_v1(mprn, serial_number)\n```\n\n[github]: https://github.com/markallanson/octopus-energy\n[octo dashboard]: https://octopus.energy/dashboard/developer/\n',
    'author': 'Mark Allanson',
    'author_email': 'mark@allanson.org',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/markallanson/octopus-energy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
