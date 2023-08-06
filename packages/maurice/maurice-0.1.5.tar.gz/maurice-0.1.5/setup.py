# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maurice', 'maurice.patchers']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.1,<0.4.0', 'wrapt>=1.12.1,<2.0.0']

extras_require = \
{'sklearn': ['scikit-learn'], 'tensorflow': ['tensorflow>=2.4.0,<3.0.0']}

setup_kwargs = {
    'name': 'maurice',
    'version': '0.1.5',
    'description': '',
    'long_description': None,
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomasvasconcelos1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.0,<4.0.0',
}


setup(**setup_kwargs)
