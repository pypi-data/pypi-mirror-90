# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fxparser']

package_data = \
{'': ['*']}

install_requires = \
['spacy>=2.3.5,<3.0.0']

setup_kwargs = {
    'name': 'fxparser',
    'version': '0.1.0',
    'description': 'A forex message parser to extract information such as symbols, tps, and sls',
    'long_description': None,
    'author': 'Danny',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
