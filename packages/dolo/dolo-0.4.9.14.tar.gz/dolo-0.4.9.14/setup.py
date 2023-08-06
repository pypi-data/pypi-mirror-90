# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dolo',
 'dolo.algos',
 'dolo.compiler',
 'dolo.misc',
 'dolo.numeric',
 'dolo.numeric.discretization',
 'dolo.numeric.extern',
 'dolo.numeric.optimize',
 'dolo.tests']

package_data = \
{'': ['*']}

install_requires = \
['dolang==0.0.14',
 'interpolation>=2.1.6,<3.0.0',
 'ipython>=7.13.0,<8.0.0',
 'matplotlib>=3.0.1,<4.0.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'numpy>=1.16.0,<2.0.0',
 'pandas>=1.0.3,<2.0.0',
 'pyyaml>=5.3.1,<6.0.0',
 'quantecon>=0.4.7,<0.5.0',
 'scipy>=1.4.1,<2.0.0',
 'xarray>=0.15.1,<0.16.0']

setup_kwargs = {
    'name': 'dolo',
    'version': '0.4.9.14',
    'description': 'Economic Modeling in Python',
    'long_description': 'Complete documentation with installation instruction, available at http://dolo.readthedocs.org/en/latest/\nNew in-progress [version](https://www.econforge.org/dolo.py).\n\nJoin the chat at https://gitter.im/EconForge/dolo\n\n[![codecov](https://codecov.io/gh/EconForge/dolo.py/branch/master/graph/badge.svg?token=hLAd1OaTRp)](https://codecov.io/gh/EconForge/dolo.py)\n\n![CI](https://github.com/EconForge/dolo.py/workflows/CI/badge.svg)\n\n![Publish docs via GitHub Pages](https://github.com/EconForge/dolo.py/workflows/Publish%20docs%20via%20GitHub%20Pages/badge.svg)\n\n[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/EconForge/dolo.git/master?urlpath=lab)\n',
    'author': 'Winant Pablo',
    'author_email': 'pablo.winant@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
