# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mongomodel']

package_data = \
{'': ['*']}

install_requires = \
['pymongo>=3.10.1,<4.0.0', 'pytest>=5.4.3,<6.0.0']

setup_kwargs = {
    'name': 'mongomodel',
    'version': '0.5.2',
    'description': 'Tiny mongodb orm document oriented',
    'long_description': None,
    'author': 'Sébastien NICOLET',
    'author_email': 'snicolet@student.42.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
