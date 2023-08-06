# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['angelou']

package_data = \
{'': ['*']}

install_requires = \
['pyspark>=3.0.1,<4.0.0', 'quinn>=0.8.0,<0.9.0']

setup_kwargs = {
    'name': 'angelou',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'ext_jarismendi',
    'author_email': 'ext_jarismendi@bancofalabella.com.co',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
