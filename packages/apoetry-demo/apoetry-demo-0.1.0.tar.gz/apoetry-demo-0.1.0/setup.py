# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['apoetry_demo']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'apoetry-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': '61246880',
    'author_email': 'jorge.plautz@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
