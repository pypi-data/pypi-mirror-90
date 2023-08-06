# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['frog_lib']

package_data = \
{'': ['*']}

install_requires = \
['PyGithub>=1.53,<2.0']

setup_kwargs = {
    'name': 'frog-lib',
    'version': '0.6.0',
    'description': '',
    'long_description': None,
    'author': 'Frog Dev',
    'author_email': 'dev@frog-mining.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
