# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['py_apple_signin']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3.7,<4',
 'cryptography>=3.0,<4.0',
 'dataclasses-json>=0.5,<0.6',
 'pyjwt>=2.0,<3',
 'requests>=2.24,<3']

setup_kwargs = {
    'name': 'py-apple-signin',
    'version': '0.3.0',
    'description': 'Apple Sign In Python Server Side impl',
    'long_description': '# Apple SignIn SDK for Python\nApple SignIn Server Side in Python (with: sync & async API)\n\n[Pypi](https://pypi.org/project/py-apple-signin/)\n[Github](https://github.com/QiYuTechDev/py_apple_signin)\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/QiYuTechDev/py_apple_signin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
