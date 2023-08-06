# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hlm_texts']

package_data = \
{'': ['*']}

install_requires = \
['Morfessor>=2.0.6,<3.0.0',
 'cchardet>=2.1.7,<3.0.0',
 'halo>=0.0.31,<0.0.32',
 'logzero>=1.6.3,<2.0.0',
 'polyglot>=16.7.4,<17.0.0',
 'sentence_splitter>=1.4,<2.0',
 'tqdm>=4.54.1,<5.0.0']

setup_kwargs = {
    'name': 'hlm-texts',
    'version': '0.1.3',
    'description': '',
    'long_description': "# hlm-texts [![Codacy Badge](https://api.codacy.com/project/badge/Grade/31c6bcb6723942a3bb12474cd7e74dac)](https://app.codacy.com/gh/ffreemt/hlm-texts?utm_source=github.com&utm_medium=referral&utm_content=ffreemt/hlm-texts&utm_campaign=Badge_Grade)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/hlm-texts.svg)](https://badge.fury.io/py/hlm-texts)\nHlm at your fingertips\n\nThis repo currently just has\n  * `340-脂砚斋重批红楼梦.txt`: hlm_zh\n  * `david-hawks-the-story-of-the-stone.txt`: hlm_en\n  * `yang-hlm.txt`: hlm_en1\n  * `joly-hlm.txt`: hlm_en2\n\nIt may expand to other versions. If you wish to have one particular version included, make a `pull request` (fork, upload files and click the pull request button) or provide a text file to me.\n\n## Special Dependencies\n`hlm_texts` depends on polyglot that in turn depends on `libicu`\n\nTo install `libicu`\n### For Linux/OSX\n\nE.g.\n* Ubuntu: `sudo apt install libicu-dev`\n* Centos: `yum install libicu`\n* OSX: `brew install icu4c`\n\nThen use `poetry` or `pip` to install ` PyICU pycld2 Morfessor`, e.g.\n```bash\npip install PyICU pycld2 Morfessor\n```bash\nor\n```python\npoetry add PyICU pycld2 Morfessor\n```\n### For Windows\n\nDownload and install the `pyicu` and `pycld2` (possibly also `Morfessor`) whl packages for your OS/Python version from https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyicu and https://www.lfd.uci.edu/~gohlke/pythonlibs/#pycld2 (possibly also Morfessor https://www.lfd.uci.edu/~gohlke/pythonlibs/)\n\n\n## Installation\n`pip install hlm-texts`\n\n## Usage\n\n```python\nfrom hlm_texts import hlm_en, hlm_zh\n```\n\n`hlm_zh` and `hlm_en` are copies of `340-脂砚斋重批红楼梦.txt` and `david-hawks-the-story-of-the-stone.txt`, respectively, with blank lines removed and paragraphs retaind.\n\n## Notes\nThe repo is for study purpose only. If you believe that your interests have been violated in any way, please let me know. I'll promptly follow it up with appropriate actions.",
    'author': 'freemt',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ffreemt/hlm-texts',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
