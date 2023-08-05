# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tompy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tompy',
    'version': '0.1.2',
    'description': 'Tompy is the powerful package for time series and statistics.',
    'long_description': '# tompy',
    'author': 'Thomas Jeong',
    'author_email': 'nanticj@users.noreply.github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nanticj/tompy',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
