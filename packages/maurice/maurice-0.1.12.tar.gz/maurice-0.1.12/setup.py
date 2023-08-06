# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['maurice', 'maurice.patchers']

package_data = \
{'': ['*']}

install_requires = \
['dill>=0.3.1,<0.4.0', 'wrapt>=1.12.1,<2.0.0']

extras_require = \
{'all': ['scikit-learn', 'tensorflow>=2.4.0,<3.0.0', 'pandas>=1.0.0,<2.0.0'],
 'pandas': ['pandas>=1.0.0,<2.0.0'],
 'sklearn': ['scikit-learn'],
 'tensorflow': ['tensorflow>=2.4.0,<3.0.0']}

setup_kwargs = {
    'name': 'maurice',
    'version': '0.1.12',
    'description': 'Ship better machine learning projects, faster!',
    'long_description': '# Maurice\n\n\n## Installation\n\n### Using pypi\n\n```shell\npip install -U maurice\n```\n\n## Integrate it with your workflow\n\n### Automatic caching\n\nAdd any of the following patches at the top of your scripts\n\nCache SQL queries executed from the pandas library\n```python\nfrom maurice.patchers import caching_patch_pandas_db; caching_patch_pandas_db()\nimport pandas as pd\n\n\ndf = pd.read_sql_query(con=your_connection, sql="select * from your_table")\n```\n\nCache `.fit()` calls from any `sklearn` Estimator (...)\n```python\nfrom maurice.patchers import caching_patch_sklearn_estimators; caching_patch_sklearn_estimators()\n\n...\n```',
    'author': 'Tomas Pereira de Vasconcelos',
    'author_email': 'tomasvasconcelos1@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/tpvasconcelos/maurice',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<4.0.0',
}


setup(**setup_kwargs)
