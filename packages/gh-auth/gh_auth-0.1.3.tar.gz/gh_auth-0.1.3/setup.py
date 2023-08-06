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
    'version': '0.1.3',
    'description': 'A simple Python library for web-based GitHub authentication.',
    'long_description': '# gh-auth\n\nA simple Python library for web-based GitHub authentication using the [device flow](https://docs.github.com/en/free-pro-team@latest/developers/apps/authorizing-oauth-apps#device-flow).\n\n## Installation\n```\npip install gh-auth\n```\n\n## Usage\n\n1. On GitHub, [create a GitHub or OAuth app](https://github.com/settings/apps).\n\n2. In your code, import the `authenticate_with_github()` function and pass it your app\'s client ID.\n\n```python\nfrom gh_auth import authenticate_with_github\n\nauthenticate_with_github(client_id)\n```\nThat\'s it.\n\nWhen called, the function will prompt users to visit https://github.com/login/device and enter an eight-character code, \nthen continously ping GitHub for a response. Upon sucessful authentication, the function will return a token you can use\nto interact with the GitHub API via libraries such as [PyGithub](https://github.com/PyGithub/PyGithub).\n\n### Scopes\n\nIf you\'re using an OAuth app, you\'ll probably also want to define what scopes you want your app to be granted. Simply pass\na list of scopes into the ``authenticate_with_github()`` function alongside your client ID, like so:\n\n```python\nauthenticate_with_github(client_id, scopes=["example_scope", "another_scope"])\n```\nSee a full list of available OAuth scopes [here](https://docs.github.com/en/free-pro-team@latest/developers/apps/scopes-for-oauth-apps).\n\nIf you\'re using an OAuth app and don\'t define any scopes, GitHub will default to granting it read-only access to the\npublic data associated with the account being authenticated and nothing more. (For GitHub apps, [scopes are defined\non GitHub](https://docs.github.com/en/free-pro-team@latest/developers/apps/editing-a-github-apps-permissions) \nand can\'t be changed from this module.)\n\n## License\n\ngh-auth\'s source code is released under the MIT License.',
    'author': 'Jason Tolbert',
    'author_email': 'jasonalantolbert@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jasonalantolbert/gh-auth',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.0,<4.0.0',
}


setup(**setup_kwargs)
