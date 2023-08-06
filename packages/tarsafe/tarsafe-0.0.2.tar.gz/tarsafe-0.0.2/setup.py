# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tarsafe']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'tarsafe',
    'version': '0.0.2',
    'description': 'A safe subclass of the TarFile class for interacting with tar files. Can be used as a direct drop-in replacement for safe usage of extractall()',
    'long_description': '# Tarsafe\n![Unit Tests](https://github.com/beatsbears/tarsafe/workflows/Unit%20Tests/badge.svg)\n\nTarsafe is a drop-in replacement for the tarfile module from the standard library to safely handle the vulnerable `extractall()` method. Inspired by a [6 year old security bug](https://bugs.python.org/issue21109).\n\n## Installation\n```\n$ pip install tarsafe\n```\n\n## Usage\n```\nimport sys\n\nfrom tarsafe import TarSafe\n\ntar = TarSafe.open(sys.argv[1], "r")\ntar.extractall()\ntar.close()\n```',
    'author': 'Andrew Scott',
    'author_email': 'a.clayton.scott@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
