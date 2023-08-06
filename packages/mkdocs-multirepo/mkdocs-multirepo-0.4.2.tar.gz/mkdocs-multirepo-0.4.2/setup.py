# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mkdocs_multirepo']

package_data = \
{'': ['*'],
 'mkdocs_multirepo': ['demo/*', 'demo/images/*', 'demo/site/images/*']}

install_requires = \
['beautifulsoup4>=4.9,<5.0', 'click>=7.1,<8.0', 'pyyaml>=5.3,<6.0']

entry_points = \
{'console_scripts': ['mkdocs-multirepo = mkdocs_multirepo:cli']}

setup_kwargs = {
    'name': 'mkdocs-multirepo',
    'version': '0.4.2',
    'description': '',
    'long_description': None,
    'author': 'Lars Wilhelmer',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
