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
    'version': '0.1.1',
    'description': 'File organization made easy using tags',
    'long_description': '# HyperTag\n\nFile organization made easy. HyperTag let\'s the user express intuitively how they think about their files using tags.\n\n## Install\nCurrently there is no easy install available. Gotta clone this repo.\n\nInstall packages: `$ python -m pip install fire tqdm filetype`\n\nSetup alias: `alias hypertag=\'python your/clone/path/hypertag/hypertag/hypertag.py\'`\n\n## Quickstart\nHyperTag offers a slick CLI but more importantly it creates a directory called ```HyperTagFS``` which is a file system based representation of your files and tags using symbolic links and directories. HyperTag recognizes a multitude of file types and groups them automatically together into folders, which can be found in ```HyperTagFS```.\n\n## CLI Functions\n\n### Set HyperTagFS directory path\nDefault is the user\'s home directory.\n\n```$ hypertag set_hypertagfs_dir path/to/directory```\n\n### Import existing directory recursively\nImport files with tags inferred from existing directory hierarchy\n\n```$ hypertag import path/to/directory```\n\n### Tag file/s\nManually tag files\n\n```$ hypertag tag humans/*.txt with human "Homo Sapiens"```\n\n### Tag a tag\nMetatag tag/s to create tag hierarchies\n\n```$ hypertag metatag human with animal```\n\n### Merge tags\nMerges all associations (files & tags) of tag_a into tag_b\n\n```$ hypertag merge human into "Homo Sapiens"```\n\n### Query using Set Theory\nPrints file names matching the query. Nesting is currently not supported, queries are evaluated from left to right.\n\nDefault operand is AND (intersection): <br>\n```$ hypertag query human "Homo Sapiens"```\n\nOR (union): <br>\n```$ hypertag query human or "Homo Sapiens"```\n\nMINUS (difference): <br>\n```$ hypertag query human minus "Homo Sapiens"```\n\n### Print all tags\n\n```$ hypertag show```\n\n### Print all files\n\n```$ hypertag show files```\n\n## Architecture\n- Python 3.9 powers HyperTag\n- SQLite3 serves as the meta data storage engine\n- Symbolic links are used to create the HyperTagFS directory structure\n\n## Inspiration\nThis project is inspired by other existing open-source projects:\n- [TMSU](https://github.com/oniony/TMSU)\n- [SuperTag](https://github.com/amoffat/supertag)\n\n**What is the point of HyperTag\'s existence?** HyperTag offers some unique features such as the import function that make it very convenient to use. Also HyperTag\'s code base is written in Python and thus extremely small (<500 LOC) compared to TMSU (>10,000 LOC) and SuperTag (>25,000 LOC), making it very easy to modify / extend / fix it yourself.\n',
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
