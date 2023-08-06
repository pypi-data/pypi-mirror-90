# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mcnp_input_reader']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'mcnp-input-reader',
    'version': '0.1.7',
    'description': 'MCNP Input reader',
    'long_description': "# MCNP Input Reader\n> The python package for reading mcnp input in a python way\n\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/mcnp-input-reader)\nMCNP Input Reader is a python package developed in ENEA to help the modifications and the check integrity \nof large mcnp input files.\n\n## Install\n\n```shell\npip install mcnp-input-reader\n```\n\n## Usage\n\n```python\nimport mcnp_input_reader as mir\n\nmcnp_input = mir.read_file('input.i') \nmcnp_input.cells # return the table of cells\nmcnp_input.cells.filter(lambda cell: cell.mat_id == 2) # return the cells using material M2\n```\n## TODO\n\nA lot of things...\n\n## Example\n\nExample taken from [here](https://www.utoledo.edu/med/depts/radther/pdf/MCNP5%20practical%20examples%20lecture%207%20companion.pdf) \n\n",
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
