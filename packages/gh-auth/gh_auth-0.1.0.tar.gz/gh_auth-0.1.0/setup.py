# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gh_auth']

package_data = \
{'': ['*']}

install_requires = \
['halo>=0.0.31,<0.0.32', 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'gh-auth',
    'version': '0.1.0',
    'description': 'A simple Python library for web-based GitHub authentication.',
    'long_description': None,
    'author': 'Jason Tolbert',
    'author_email': 'jasonalantolbert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
