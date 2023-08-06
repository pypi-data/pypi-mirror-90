# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rygforms']

package_data = \
{'': ['*']}

install_requires = \
['authlib>=0.15.2,<0.16.0',
 'flask>=1.1.2,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'rygforms',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
