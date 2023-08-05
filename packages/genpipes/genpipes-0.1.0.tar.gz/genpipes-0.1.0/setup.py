# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['genpipes']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'genpipes',
    'version': '0.1.0',
    'description': 'Simple library to compose pipelinein the sklearn way thanks to generators',
    'long_description': None,
    'author': 'Matt G.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
