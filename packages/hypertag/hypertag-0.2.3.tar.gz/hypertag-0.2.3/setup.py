# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hypertag']

package_data = \
{'': ['*']}

install_requires = \
['filetype>=1.0.7,<2.0.0',
 'fire>=0.3.1,<0.4.0',
 'tqdm>=4.55.0,<5.0.0',
 'watchdog>=1.0.2,<2.0.0']

setup_kwargs = {
    'name': 'hypertag',
    'version': '0.2.3',
    'description': 'File organization made easy using tags',
    'long_description': '# HyperTag\n\nFile organization made easy. HyperTag let\'s humans intuitively express how they think about their files using tags.\n\n## Install\n`$ pip install hypertag`\n\n## Quickstart\nHyperTag offers a slick CLI but more importantly it creates a directory called ```HyperTagFS``` which is a file system based representation of your files and tags using symbolic links and directories.\n\n**Directory Import**: Import your existing directory hierarchies using ```$ hypertag import path/to/directory```. HyperTag converts it automatically into a tag hierarchy using metatagging.\n\n**File Type Groups**: HyperTag automatically creates folders containing common files (e.g. Images: jpg, png, etc., Documents: txt, pdf, etc., Source Code: py, js, etc.), which can be found in ```HyperTagFS```.\n\n**HyperTagFS Daemon  (Experimental)**: Monitors `HyperTagFS` for user changes. Currently supports file and directory (tag) deletions + directory (query) creation.\n\n## CLI Functions\n\n### Start HyperTagFS daemon\nStarts process watching HyperTagFS dir for user changes.\n\n```$ hypertag daemon```\n\n### Set HyperTagFS directory path\nDefault is the user\'s home directory.\n\n```$ hypertag set_hypertagfs_dir path/to/directory```\n\n### Import existing directory recursively\nImport files with tags inferred from existing directory hierarchy\n\n```$ hypertag import path/to/directory```\n\n### Tag file/s\nManually tag files\n\n```$ hypertag tag humans/*.txt with human "Homo Sapiens"```\n\n### Untag file/s\nManually remove tag/s from file/s\n\n```$ hypertag untag humans/*.txt with human "Homo Sapiens"```\n\n### Tag a tag\nMetatag tag/s to create tag hierarchies\n\n```$ hypertag metatag human with animal```\n\n### Merge tags\nMerges all associations (files & tags) of tag A into tag B\n\n```$ hypertag merge human into "Homo Sapiens"```\n\n### Query using Set Theory\nPrints file names matching the query. Nesting is currently not supported, queries are evaluated from left to right.\n\nPrint paths: ```$ hypertag query human --path```\n\nDefault operand is AND (intersection): <br>\n```$ hypertag query human "Homo Sapiens"```\n\nOR (union): <br>\n```$ hypertag query human or "Homo Sapiens"```\n\nMINUS (difference): <br>\n```$ hypertag query human minus "Homo Sapiens"```\n\n### Print all tags of file/s\n\n```$ hypertag tags filename1 filename2```\n\n### Print all metatags of tag/s\n\n```$ hypertag metatags tag1 tag2```\n\n### Print all tags\n\n```$ hypertag show```\n\n### Print all files\n\nPrint names:\n```$ hypertag show files```\n\nPrint paths:\n```$ hypertag show files --path```\n\n## Architecture\n- Python powers HyperTag\n- SQLite3 serves as the meta data storage engine (located at `~/.config/hypertag/hypertag.db`)\n- Symbolic links are used to create the HyperTagFS directory structure\n\n## Development\n- Clone repo: ```$ git clone https://github.com/SeanPedersen/HyperTag.git```\n- `$ cd HyperTag/`\n- Install [Poetry](https://python-poetry.org/docs/#installation)\n- Install dependencies: `$ poetry install`\n- Activate virtual environment: `$ poetry shell`\n- Run all tests: ```$ pytest -v```\n- Run Black formatter: ```$ black hypertag/```\n- Run PyLint: ```$ pylint **/*.py```\n- Run MyPy: ```$ mypy **/*.py```\n- Run Bandit: ```$ bandit --exclude tests/ -r .```\n- Run HyperTag: ```$ python -m hypertag```\n\n## Inspiration\nThis project is inspired by other existing open-source projects:\n- [TMSU](https://github.com/oniony/TMSU): Written in Go\n- [SuperTag](https://github.com/amoffat/supertag): Written in Rust\n\n**What is the point of HyperTag\'s existence?** HyperTag offers some unique features such as the import function that make it very convenient to use. Also HyperTag\'s code base is written in Python and thus extremely small (<600 LOC) compared to TMSU (>10,000 LOC) and SuperTag (>25,000 LOC), making it very easy to modify / extend / fix it yourself.\n',
    'author': 'Sean',
    'author_email': 'sean-p-96@hotmail.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/SeanPedersen/HyperTag',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
