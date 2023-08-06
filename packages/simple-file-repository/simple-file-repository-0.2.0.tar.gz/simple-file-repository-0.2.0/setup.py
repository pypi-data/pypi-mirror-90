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
    'version': '0.2.0',
    'description': 'A simple file and photo repository.',
    'long_description': "Simple File Repository\n======================\n\n![Build](https://github.com/theirix/simple-file-repository/workflows/build/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/simple-file-repository)\n\nA simple file and photo repository.\nUnderlying storage is a filesystem or a S3-compatible service.\n\n## Installation\n\n    pip install simple_file_repository\n\n## Usage\n\n### File storage\n\n```python\n    >>> import uuid\n    >>> from simple_file_repository import FileStorage\n    >>> storage = FileStorage(storage_directory='/tmp/repo', database='cats')\n    >>> storage.store(b'content')\n    UUID('72fc4a76-1ab7-4d60-9f6a-94aa0ad45b5b')\n    >>> storage.get(uuid.UUID(hex='72fc4a76-1ab7-4d60-9f6a-94aa0ad45b5b'))\n    b'content'\n    >>> list(storage.list())\n    ['72fc4a76-1ab7-4d60-9f6a-94aa0ad45b5b']\n```\n\n### Photo storage using S3\n\n```python\n\nfrom simple_file_repository import PhotoStorages\n\nstorages = PhotoStorages()\n\nstorages.init_app(names=['cats', 'dogs'],\n                  storage_directory='/tmp/repo',\n                  names_for_s3=['cats'],\n                  imagemagick_convert='/usr/bin/convert',\n                  access_key_id='',\n                  secret_access_key='',\n                  region='us-east-1', bucket='my-s3-bucket')\n\nstorages['cats'].store(b'image')\n\n```\n\n## License\n\nMIT",
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
