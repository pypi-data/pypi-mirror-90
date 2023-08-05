# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pylocalc']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pylocalc',
    'version': '0.1.2',
    'description': 'Python interface for manipulating LibreOffice Calc spreadsheets',
    'long_description': '# PyLOcalc\n',
    'author': 'Viliam Valent',
    'author_email': 'pylocalc@viliamvalent.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ViliamV/pylocalc',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
