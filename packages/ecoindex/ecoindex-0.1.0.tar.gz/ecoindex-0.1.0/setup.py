# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ecoindex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ecoindex',
    'version': '0.1.0',
    'description': 'Ecoindex module provides a simple way to measure the Ecoindex (http://www.ecoindex.fr/) score based on the 3 parameters : The DOM elements of the page, the size of the page and the number of external requests of the page',
    'long_description': None,
    'author': 'Vincent Vatelot',
    'author_email': 'vincent.vatelot@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
