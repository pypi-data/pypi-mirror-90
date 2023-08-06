# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['transitions_anyio']

package_data = \
{'': ['*']}

install_requires = \
['anyio>=2.0.2,<3.0.0', 'transitions>=0.8.6,<0.9.0']

setup_kwargs = {
    'name': 'transitions-anyio',
    'version': '0.1.0',
    'description': 'An extension for the transitions state machine library which runs asynchronous state machines using anyio.',
    'long_description': "=================\ntransitions-anyio\n=================\n\nAn extension for the `transitions`_ state machine library\nwhich runs asynchronous state machines using `anyio`_.\n\nThis library provides the `AnyIOMachine`, `AnyIOGraphMachine`, `HierarchicalAnyIOMachine`\nand the `HierarchicalAnyIOGraphMachine` variants.\nThey function exactly like their respective `Async*` variants.\nPlease refer to transitions' documentation for usage examples.\n\n.. _transitions: https://github.com/pytransitions/transitions\n.. _anyio: https://github.com/agronholm/anyio",
    'author': 'Alexander Neumann',
    'author_email': 'aleneum@gmail.com',
    'maintainer': 'Omer Katz',
    'maintainer_email': 'omer.drow@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
