# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qsde', 'qsde.filestore']

package_data = \
{'': ['*']}

install_requires = \
['google-cloud-storage>=1.35.0,<2.0.0', 'pandas>=1.1.5,<2.0.0']

setup_kwargs = {
    'name': 'qsde',
    'version': '0.1.2',
    'description': '',
    'long_description': None,
    'author': 'Huan Nguyen',
    'author_email': 'ngtrunghuan@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
