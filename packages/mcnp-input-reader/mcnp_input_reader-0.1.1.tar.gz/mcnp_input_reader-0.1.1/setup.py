# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcnp_input_reader']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcnp-input-reader',
    'version': '0.1.1',
    'description': 'MCNP Input reader',
    'long_description': None,
    'author': 'gmariano',
    'author_email': 'giovanni.mariano@enea.it',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.0.0,<4.0.0',
}


setup(**setup_kwargs)
