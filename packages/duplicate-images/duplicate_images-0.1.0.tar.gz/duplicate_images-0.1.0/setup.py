# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['duplicate_images']

package_data = \
{'': ['*']}

install_requires = \
['Wand>=0.6.5,<0.7.0', 'pillow>=8.1.0,<9.0.0']

entry_points = \
{'console_scripts': ['find-dups = duplicate_images.duplicate:main']}

setup_kwargs = {
    'name': 'duplicate-images',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Lene Preuss',
    'author_email': 'lene.preuss@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.5,<4.0.0',
}


setup(**setup_kwargs)
