# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfgcaddy']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.1.2,<8.0.0',
 'pathspec>=0.8.1,<0.9.0',
 'questionary>=1.9.0,<2.0.0',
 'ruamel.yaml>=0.16.12,<0.17.0',
 'whaaaaat>=0.5.2,<0.6.0']

entry_points = \
{'console_scripts': ['cfgcaddy = cfgcaddy.__main__:main',
                     'publish = cfgcaddy.publish:publish']}

setup_kwargs = {
    'name': 'cfgcaddy',
    'version': '0.1.3',
    'description': "A cli for managing user's config files",
    'long_description': "# Config Caddy\n\n![Travis CI](https://travis-ci.org/tstapler/cfgcaddy.svg?branch=master)\n[![PyPI version](https://badge.fury.io/py/cfgcaddy.svg)](https://badge.fury.io/py/cfgcaddy)\n\n\nConfig Caddy is a tool used for managing your configuration files. \n\nOne way to version your configuration files is to keep them in a [git](https://git-scm.com/) repository. This has several drawbacks, among them, git requires the files it manages to be located within a single file tree. You can overcome this limitation by using symbolic links. The links point from locations in your filesystem such as `/etc/someconfig.conf`to files within the git repository like `$HOME/tstapler/dotfiles/someconfig.conf`.\n\nConfig Caddy creates symlinks to your dotfiles directory, so you don't have to. Each time you add a new file to your dotfiles repo, run `cfgcaddy link` to generate symlinks. By default `cfgcaddy` will create links from files in the dotfiles repo to their relative location in your home directory. `cfgcaddy` will also read from a configuration file. This allows the user to ignore certain files and create more complex linking relationships.\n\n\n## Usage\n\n2. Install using pip\n\n```shell\n\npip install cfgcaddy\n\n````\n2. Generate or import a configuration file for cfgcaddy\n\n```shell\ncfgcaddy init --help\n\nUsage: cfgcaddy init [OPTIONS] SRC_DIRECTORY DEST_DIRECTORY\n\n  Create or import a caddy config\n\nOptions:\n  -c, --config PATH  The path to your cfgcaddy.yml\n  --help             Show this message and exit.\n\ncfgcaddy init $HOME/dotfiles $HOME\n```\n\n3. Run the linker\n```bash\ncfgcaddy link\n```\n\n## Configuration File Format\n\n`cfgcaddy` uses a configuration file to store important information about your configuration. The `.cfgcaddy.yml` consists of several parts. A *preferences* section which contains information like where your dotfiles are located and where you want them linked to, A *links* section where you can specify more complex symlinks, and an `ignore` section where you specify files you do not want managed by `cfgcaddy`.\n\nConfig files for cfgcaddy are stored in your home directory by default. `$HOME/.cfgcaddy.yml`\n\nA sample `.cfgcaddy.yml` which leverages most features can be found [here](https://github.com/tstapler/dotfiles/blob/master/.cfgcaddy.yml)\n\n## Development\n\n1. Clone the repository\n\n```shell\n\ngit clone https://github.com/tstapler/cfgcaddy\n\n```\n\n2. Install cfgcaddy as an editable package\n\n```shell\n\npip install --editable ./cfgcaddy\n\n```\n\n3. ??????\n\n4. Profit\n\n## Motivation/Prior Art\n\nI'm an automation fiend, this tool grew out of a personal need to manage my configurations across multiple machines and operating systems. It fits my needs and I'll add features as I need them (Like Windows support). PRs are always welcome :)\n\nHere are several projects that I've drawn inspiration from:\n\n- https://github.com/charlesthomas/linker\n- https://github.com/thoughtbot/rcm\n",
    'author': 'Tyler Stapler',
    'author_email': 'tystapler@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.10',
}


setup(**setup_kwargs)
