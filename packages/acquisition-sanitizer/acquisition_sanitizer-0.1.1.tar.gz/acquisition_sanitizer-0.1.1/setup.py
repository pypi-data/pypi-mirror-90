# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['acquisition_sanitizer']

package_data = \
{'': ['*']}

install_requires = \
['html-sanitizer>=1.9.1,<2.0.0']

setup_kwargs = {
    'name': 'acquisition-sanitizer',
    'version': '0.1.1',
    'description': 'Helper function for pattern matching functions',
    'long_description': None,
    'author': 'Mars Veloso',
    'author_email': 'testmarcelino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
