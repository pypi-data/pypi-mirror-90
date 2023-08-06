# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dolang', 'dolang.tests']

package_data = \
{'': ['*']}

install_requires = \
['lark-parser>=0.9.0,<0.10.0',
 'lark>=0.10.1,<0.11.0',
 'numba>=0.50',
 'numpy>=1.18.3,<2.0.0',
 'sympy>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'dolang',
    'version': '0.0.14',
    'description': 'Dolo Modeling Language',
    'long_description': '# dolang.py\n\nVery empty README file.\n\n[![codecov](https://codecov.io/gh/EconForge/dolang.py/branch/master/graph/badge.svg?token=1U3Q8FLOFK)](https://codecov.io/gh/EconForge/dolang.py)\n\n  ![CI](https://github.com/EconForge/dolang.py/workflows/CI/badge.svg)\n![Docs](https://github.com/EconForge/dolang.py/workflows/Publish%20docs%20via%20GitHub%20Pages/badge.svg)\n',
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
