# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bobros']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'colour>=0.1.5,<0.2.0',
 'ruamel.yaml>=0.16.12,<0.17.0']

setup_kwargs = {
    'name': 'bobros',
    'version': '0.1.0',
    'description': 'A tool to set file and folder colours in Idea projects',
    'long_description': None,
    'author': 'Timofey Danshin',
    'author_email': 't.danshin@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
