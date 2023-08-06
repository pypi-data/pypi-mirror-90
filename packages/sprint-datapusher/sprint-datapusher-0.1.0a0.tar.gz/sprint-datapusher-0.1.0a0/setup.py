# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['sprint_datapusher']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'jsonpickle>=1.4.1,<2.0.0',
 'pandas>=1.1.5,<2.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'requests>=2.25.1,<3.0.0',
 'watchdog>=1.0.1,<2.0.0']

entry_points = \
{'console_scripts': ['sprint_datapusher = sprint_datapusher.datapusher:cli']}

setup_kwargs = {
    'name': 'sprint-datapusher',
    'version': '0.1.0a0',
    'description': 'A tool to read csv files, transform to json and push to sprint_excel_webserver.',
    'long_description': None,
    'author': 'Stig B. Dørmænen',
    'author_email': 'stigbd@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
