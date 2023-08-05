# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['luz']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.3.2,<4.0.0', 'networkx>=2.5,<3.0', 'torch>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'luz',
    'version': '4.0.0',
    'description': 'blahblah',
    'long_description': '==============\nLuz Module\n==============\n\n.. image:: https://codecov.io/gh/kijanac/luz/branch/master/graph/badge.svg\n  :target: https://codecov.io/gh/kijanac/luz\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github\n\n**Framework for rapid research and development of machine learning projects using PyTorch.**\n\nLonger description coming soon!\n\n---------------\nGetting Started\n---------------\n\nPrerequisites\n-------------\n\nInstalling\n----------\n\nTo install, open a shell terminal and run::\n\n`conda create -n luz -c conda-forge -c pytorch -c kijana luz`\n\n----------\nVersioning\n----------\n\n-------\nAuthors\n-------\n\nKi-Jana Carter\n\n-------\nLicense\n-------\nThis project is licensed under the MIT License - see the LICENSE file for details.\n',
    'author': 'Ki-Jana Carter',
    'author_email': 'kijana@mit.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kijanac/luz',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
