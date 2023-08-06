# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcnp_input_reader']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcnp-input-reader',
    'version': '0.1.2',
    'description': 'MCNP Input reader',
    'long_description': '# MCNP Input Reader\n\nMCNP Input Reader is a python package developed in order to facilitate the modifications and the check integrity \nof large mcnp input files.\n\n## Install\n\n```shell\npip install mcnp-input-reader\n```\n',
    'author': 'gmariano',
    'author_email': 'giovanni.mariano@enea.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ENEA-Fusion-Neutronics/MCNP-Input-Reader.git',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
