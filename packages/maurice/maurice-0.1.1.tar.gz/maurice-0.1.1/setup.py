# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maurice', 'maurice.patchers']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.3,<0.4.0',
 'joblib>=1.0.0,<2.0.0',
 'scikit-learn>=0.24.0,<0.25.0',
 'wrapt>=1.12.1,<2.0.0']

setup_kwargs = {
    'name': 'maurice',
    'version': '0.1.1',
    'description': '',
    'long_description': None,
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomas@tiqets.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.6,<4.0.0',
}


setup(**setup_kwargs)
