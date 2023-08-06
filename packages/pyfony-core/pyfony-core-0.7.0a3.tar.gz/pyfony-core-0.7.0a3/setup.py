# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyfonycore', 'pyfonycore.container']

package_data = \
{'': ['*'], 'pyfonycore': ['_config/*']}

install_requires = \
['injecta>=0.8.11,<0.9.0', 'pyfony-bundles==0.2.5a2']

setup_kwargs = {
    'name': 'pyfony-core',
    'version': '0.7.0a3',
    'description': 'Pyfony core',
    'long_description': '# Pyfony Core\n\n[Pyfony](https://github.com/pyfony/pyfony) is a **Dependency Injection (DI) powered framework** written in Python\n\n## Installation\n\n```\n$ pip add pyfony-core\n```\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/core',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
