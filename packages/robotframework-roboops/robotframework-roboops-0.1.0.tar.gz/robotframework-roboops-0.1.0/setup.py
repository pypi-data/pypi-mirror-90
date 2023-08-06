# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['RoboOps']

package_data = \
{'': ['*']}

install_requires = \
['robotframework>=3.2.2,<4.0.0']

setup_kwargs = {
    'name': 'robotframework-roboops',
    'version': '0.1.0',
    'description': "Robot Framework's library for creating and running DevOps tasks easily and efficiently.",
    'long_description': "# robotframework-roboops\n----\nRobot Framework's library for creating, sharing and running DevOps tasks easily and efficiently\n\n# Installation instructions\ntodo\n\n# Usage\n\n# running tests\n```\ncoverage run --source=. -m pytest . && coverage report -m && coverage html\nfirefox htmlcov/index.html\n```",
    'author': 'Łukasz Sójka',
    'author_email': 'soyacz@gmail.com',
    'maintainer': 'Łukasz Sójka',
    'maintainer_email': 'soyacz@gmail.com',
    'url': 'https://github.com/soyacz/robotframework-roboops/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
