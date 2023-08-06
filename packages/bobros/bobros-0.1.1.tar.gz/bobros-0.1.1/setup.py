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
    'version': '0.1.1',
    'description': 'A tool to set file and folder colours in Idea projects',
    'long_description': 'Bobros\n======\n_Making your life a bit more beautiful_\n\n`bobros` is a tool for setting the background colour for files in PyCharm project\nnavigator.\n\nIt was mainly created for working with Django projects where you can have lots\nof app folders, all of which may contain files with identical names like `views`\nor `models`, etc. It\'s much easier to work with them when you can easily \ntell them apart and can easily see where one app ends and another one begins in\nyour project navigation panel. Colour-coding the app folders makes that task a\nlot easier.\n\nHowever, it turned out that doing that using the standard PyCharm mechanisms is\nnot that easy. You have to navigate through several settings tabs and do a lot\nof clicking and typing. Well, there must be a better way!\n\nBobros takes a simple config and generates the correct xml files to make your\nproject files colour-coded. It also supports different colour-themes. \n\nSample config file::\n```yaml    \nthemes:\n    dark: # defines colours for a theme named "dark", names can be arbitrary\n        one: aabb00 # defines colour "one" to have the hex value of aabb00\n        two: bbaa00 # defines colour "two"\n    light: # defines colours for a theme named "light". Should contain the same colours as other themes\n        one: 99ff88\n        two: 9988ee\n\nitems: # defines colours for the items on disk\n    my_file.py: one\n    my_file_2.py: two\n    my_folder: one\n```\n\nSome special values: \n\n* `~` The "home" folder: in Django projects the settings folder by default has \n  the same name as the project folder. It\'s nice to have the settings folder \n  the same colour in all your projects\n\n* `Problems`, `Non-Project Files` special names used by Idea for files/folders\n  containing errors or not belonging to the current project',
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
