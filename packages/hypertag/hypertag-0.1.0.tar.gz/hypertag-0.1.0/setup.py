# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypertag']

package_data = \
{'': ['*']}

install_requires = \
['filetype>=1.0.7,<2.0.0', 'fire>=0.3.1,<0.4.0', 'tqdm>=4.55.0,<5.0.0']

setup_kwargs = {
    'name': 'hypertag',
    'version': '0.1.0',
    'description': 'File organization made easy using tags',
    'long_description': None,
    'author': 'Sean',
    'author_email': 'sean-p-96@hotmail.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SeanPedersen/HyperTag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
