# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simple_file_repository']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.14.53,<2.0.0', 'filemagic>=1.6,<2.0', 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'simple-file-repository',
    'version': '0.1.0',
    'description': 'A simple file and photo repository.',
    'long_description': None,
    'author': 'theirix',
    'author_email': 'theirix@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
