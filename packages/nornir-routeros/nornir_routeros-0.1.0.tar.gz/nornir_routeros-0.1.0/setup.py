# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nornir_routeros',
 'nornir_routeros.plugins',
 'nornir_routeros.plugins.connections',
 'nornir_routeros.plugins.tasks']

package_data = \
{'': ['*']}

install_requires = \
['Jinja2>=2.11.2,<3.0.0', 'RouterOS-api>=0.17.0,<0.18.0']

entry_points = \
{'nornir.plugins.inventory': ['routerosapi = '
                              'nornir_routeros.plugins.connections:RouterOsApi']}

setup_kwargs = {
    'name': 'nornir-routeros',
    'version': '0.1.0',
    'description': 'RouterOS API plugins for nornir',
    'long_description': None,
    'author': 'Devon Mar',
    'author_email': 'devonm@mdmm.ca',
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
