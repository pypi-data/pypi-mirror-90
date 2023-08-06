# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webknossos']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'webknossos',
    'version': '0.0.1',
    'description': 'Utilities for webKnossos',
    'long_description': None,
    'author': 'scalable minsd',
    'author_email': 'hello@scalableminds.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
