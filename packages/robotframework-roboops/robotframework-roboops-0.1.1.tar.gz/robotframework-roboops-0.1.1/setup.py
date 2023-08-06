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
    'version': '0.1.1',
    'description': "Robot Framework's library for creating and running DevOps tasks easily and efficiently.",
    'long_description': '# robotframework-roboops\n\nRobot Framework\'s library for creating, sharing and running DevOps tasks easily and efficiently\n\n----\nPrimarly designed for testers/developers who use Robot Framework.\nThey often create own python libraries and must maintain them.\n\nBut it\'s not limited only to that - you can automate any stuff with it - with syntax you know and reports you love.\n\n# Features\n- uses robotframework for running tasks - see all the benefits of robotframework\n    - one that brings a lot of benefits are report and log files\n- keyword for running commands\n- keyword for linking artifacts into report metadata\n- any failure makes remaining tasks to fail automatically (skip)\n- others to come - raise your idea!\n\n# Installation instructions\npip install robotframework-roboops\n\n# Usage\nRoboOps is typical Robotframework library - use it as usual robot library.\n\nAs this library is mainly focused on running tasks instead of tests,\ntry to use "\\*** Tasks \\***" instead of "\\*** Test Cases \\***" in .robot files.\n\nThis repository uses RoboOps for building, testing (and in future deploying) itself.\nSee pipeline.robot to see example how to do it.\n\nThis repository uses github actions - check this out to see how to use it in CI pipeline.\n\n# Running tests\nTest everything (unit tests, acceptance tests, building wheel) by running:\n```\nrobot pipeline.robot\n```\nSo, instead of pushing to repository and wait until your CI/CD tool\n(like Jenkins/Github Actions/Travis etc.) tests if it is ok, run above command to get results 300% faster.\n \n ## running pipeline with docker (using python 3.6)\n build docker image and run it:\n ```docker build -t roboops:1.0.0 .\n docker run --rm -v "${PWD}":/code --env PYTHONPATH=. roboops:1.0.0```',
    'author': 'Łukasz Sójka',
    'author_email': 'soyacz@gmail.com',
    'maintainer': 'Łukasz Sójka',
    'maintainer_email': 'soyacz@gmail.com',
    'url': 'https://github.com/soyacz/robotframework-roboops/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
