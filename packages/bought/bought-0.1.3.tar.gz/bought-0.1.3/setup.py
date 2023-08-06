# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bought', 'bought.sounds', 'bought.websites']

package_data = \
{'': ['*']}

install_requires = \
['click', 'lxml', 'playsound', 'requests', 'selenium']

entry_points = \
{'console_scripts': ['bought = bought.__main__:main']}

setup_kwargs = {
    'name': 'bought',
    'version': '0.1.3',
    'description': 'A bot that purchases items, rendering them bought.',
    'long_description': '# Bought\nA bot which can purchase items online, rendering them bought.\n\nThis bot is intended to combat scalping practices.\n\n## Installation\nInstalling this bot is a multi-step process involving a Command Line\nInterface (CLI) such as Windows PowerShell, Bash, Zsh, and Fish:\n1. [Download Python](#1-downloading-python)\n2. [Installing Bought](#2-installing-bought)\n3. [Download browser drivers](#3-install-webdriver)\n\n### 1. Downloading Python\nOpen up your respective CLI and type:\n```\npython --version\n```\nThis will display the python version on your system. Ensure you are running\nPython 3.7, or higher. If you are running an earlier version of Python,\nplease update your Python. If a Python version isn\'t installed on your\ncomputer and you received an error running this command, download Python from\n[Python.org](https://www.python.org/downloads/), or a Python distribution\nlike [Anaconda](https://www.anaconda.com/products/individual#Downloads).\n\n### 2. Installing Bought\nPython comes with its own package manager called `pip` which can install\npackages/libraries. Upgrade the pip package using pip:\n```\npython -m pip install --upgrade pip\n```\nNow run the following to download this project package to your system\'s\nPython:\n```\npip install bought\n```\n\n### 3. Install Webdriver\nVist the [selenium documentation](https://selenium-python.readthedocs.io/installation.html#drivers)\npage and download the driver for your preferred browser:\n[Firefox](https://github.com/mozilla/geckodriver/releases) | [Chrome](https://sites.google.com/a/chromium.org/chromedriver/downloads)\n\nThis driver will need to be added to your PATH environment variable. You can do this on your specific OS as follows:\n\n#### Windows Path\nPress the Windows key, and type "environment":\n![Edit the system environment variables - Control Panel](./readme_source/env.PNG)\n\nSelect the above item in the Control Panel, under the advanced tab, find\n`Environment Variables...` in the bottom right corner.\n\n![System Properties - Advanced - Environment Variables...](./readme_source/advanced.PNG)\n\nUnder User variables, select `Path`, `Edit...`, `New`, and provide the path to the driver you installed.\n\n![Environment variables](./readme_source/path.png)\n\n\n#### Linux/MacOS\nIn Linux and MacOS, your corresponding shell will have its own configuration\nfile (typically in your home folder). For bash and zsh, this is `~/.bashrc` and `~/.zshrc`, respectively.\n\nOpen the file and add the following line to the bottom:\n\n```\nexport PATH=/path/to/driver:$PATH\n```\n\nSave and exit. You can restart the shell, or execute the source command for your corresponding configuration file:\n```\nsource ~/.bashrc\nsource ~/.zshrc\netc...\n```\n\n## Usage\nBought uses Python\'s console scripts entry point. This allows you to use\nthe `bought` command from your CLI:\n\n```\nbought --help\n```\n\nThis will display a list of subcommands and flags that can be used to\nconfigure bought and run it from the command line; however, it is highly\nrecommended to use Bought with a config file:\n\n```\nbought -c config.ini\n```\n\nThe config.ini file can be specified in any directory. A sample one is\nprovided in this repository with descriptive comments about their usage.\n\n## Contributing\nFirst and foremost, [create an\nissue](https://github.com/boughts/bought/issues/new) on the github\nrepository. This is where issues can be made known publicly -- be sure to\ncheck for duplicates prior to submitting an issue.\n\nIf you want to address an issue yourself, fork this repository, develop\nyour changes in a branch seperate from `main`, and submit a pull request.\n\nThis project uses [poetry](https://python-poetry.org/docs/#installation)\nwhich allows for build isolation in a virtual environment. After downloading\nthe repository, run `poetry shell` and `poetry install` from the root of the\nrepository to install the project. You may need to uninstall the PyPI version\nof `bought` with `pip uninstall bought` to use your own version of `bought`.',
    'author': 'Jason G. Villanueva',
    'author_email': 'a@jsonvillanueva.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/boughts/bought',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
