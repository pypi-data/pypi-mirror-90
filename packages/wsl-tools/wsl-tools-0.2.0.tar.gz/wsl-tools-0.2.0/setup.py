# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wsl_tools']

package_data = \
{'': ['*']}

install_requires = \
['pyxdg>=0.27,<0.28']

setup_kwargs = {
    'name': 'wsl-tools',
    'version': '0.2.0',
    'description': 'WSL utilities library',
    'long_description': None,
    'author': 'Andrea Ghensi',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
