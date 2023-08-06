# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'prototyping'}

packages = \
['pyegsnrc']

package_data = \
{'': ['*']}

install_requires = \
['jax', 'jaxlib', 'matplotlib', 'typing-extensions']

entry_points = \
{'console_scripts': ['pyegsnrc = pyegsnrc.__main__:main']}

setup_kwargs = {
    'name': 'pyegsnrc',
    'version': '0.1.0.dev1',
    'description': '',
    'long_description': None,
    'author': None,
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
