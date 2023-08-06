# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['docformatter_toml']

package_data = \
{'': ['*']}

install_requires = \
['docformatter>=1.4,<2.0', 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['docformatter = docformatter_toml.__main__:main']}

setup_kwargs = {
    'name': 'docformatter-toml',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Pedro Pablo Correa',
    'author_email': 'pbcorrea@uc.cl',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.9,<4.0.0',
}


setup(**setup_kwargs)
