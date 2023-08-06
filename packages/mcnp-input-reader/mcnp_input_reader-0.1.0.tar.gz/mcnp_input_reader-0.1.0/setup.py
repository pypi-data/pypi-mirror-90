# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcnp_input_reader']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcnp-input-reader',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'gmariano',
    'author_email': 'giovanni.mariano@enea.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
}


setup(**setup_kwargs)
