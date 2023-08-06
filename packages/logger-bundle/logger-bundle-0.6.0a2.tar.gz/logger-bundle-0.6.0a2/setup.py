# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['loggerbundle',
 'loggerbundle.extra',
 'loggerbundle.handler',
 'loggerbundle.stdout']

package_data = \
{'': ['*'], 'loggerbundle': ['_config/*']}

install_requires = \
['colorlog>=4.0.0,<4.1.0', 'pyfony-bundles==0.2.5a2']

entry_points = \
{'pyfony.bundle': ['autodetect = '
                   'loggerbundle.LoggerBundle:LoggerBundle.autodetect']}

setup_kwargs = {
    'name': 'logger-bundle',
    'version': '0.6.0a2',
    'description': 'Logger bundle for the Pyfony framework',
    'long_description': 'Logger bundle for the Pyfony Framework\n',
    'author': 'Jiri Koutny',
    'author_email': 'jiri.koutny@datasentics.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pyfony/logger-bundle',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.3,<3.8.0',
}


setup(**setup_kwargs)
