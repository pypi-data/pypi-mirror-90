# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_report_me']

package_data = \
{'': ['*'], 'pytest_report_me': ['templates/*']}

install_requires = \
['pytest']

entry_points = \
{'pytest11': ['report = pytest_report_me:plugin']}

setup_kwargs = {
    'name': 'pytest-report-me',
    'version': '0.0.3',
    'description': 'A pytest plugin to generate report.',
    'long_description': None,
    'author': 'yuze',
    'author_email': 'looker53@sina.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
