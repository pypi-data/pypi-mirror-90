# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pib_cli', 'pib_cli.config', 'pib_cli.patchbay', 'pib_cli.support']

package_data = \
{'': ['*'], 'pib_cli': ['bash/*']}

install_requires = \
['PyYAML>=5.3.1,<5.4.0',
 'bandit>=1.6.2,<1.6.3',
 'click>=7.1.2,<7.2.0',
 'commitizen>=2.8.2,<3.0.0',
 'isort>=5.6.0,<5.7.0',
 'jinja2>=2.10.3,<3.0.0',
 'm2r2>=0.2.7,<0.3.0',
 'poetry>=1.1.4,<1.2.0',
 'pylint>=2.6.0,<2.7.0',
 'pytest-cov>=2.10.1,<2.11.0',
 'pytest-pylint>=0.18.0,<0.20.0',
 'pytest>=5.4.1,<5.5.0',
 'safety>=1.9.0',
 'sphinx>=3.0.4,<3.1.0',
 'wheel>=0.36.0',
 'yamllint>=1.25.0',
 'yapf>=0.30.0']

entry_points = \
{'console_scripts': ['dev = pib_cli.cli:cli', 'pib_cli = pib_cli.cli:cli']}

setup_kwargs = {
    'name': 'pib-cli',
    'version': '0.0.6',
    'description': 'Python Development CLI',
    'long_description': '# PIB CLI\n\nA development environment CLI, complete with tooling.\n\n[Project Documentation](https://pib_cli.readthedocs.io/en/latest/)\n\n## Develop Branch\n\n[![pib_cli-automation](https://github.com/shared-vision-solutions/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=develop)](https://github.com/shared-vision-solutions/pib_cli/actions)\n\n## Master Branch\n\n[![pib_cli-automation](https://github.com/shared-vision-solutions/pib_cli/workflows/pib_cli%20Automation/badge.svg?branch=master)](https://github.com/shared-vision-solutions/pib_cli/actions)\n\n## Installation\n\nThis is a development environment CLI, with a customizable yaml config.\n\nIt\'s built into this [Cookie Cutter](https://github.com/cookiecutter/cookiecutter) template:\n\n- [Python In A Box](https://github.com/shared-vision-solutions/python-in-a-box)\n\nTo install, simply use: `pip install pib_cli`\n\n## Usage\n\n- use the `dev` command for details once inside the container\n\n## Container\n\n[python:3.7-slim](https://github.com/docker-library/python/tree/master/3.7/buster/slim)\n\n## License\n\n[MPL-2](LICENSE)\n\n## Installed Packages:\n| package    | Description                       |\n| ---------- | --------------------------------- |\n| bandit     | Finds common security issues      |\n| commitizen | Standardizes commit messages      |\n| isort      | Sorts imports                     |\n| poetry     | Python Package Manager            |\n| pylint     | Static Code Analysis              |\n| pytest     | Test suite                        |\n| pytest-cov | Coverage support for pytest       |\n| sphinx     | Generating documentation          |\n| safety     | Dependency vulnerability scanning |\n| wheel      | Package distribution tools        |\n| yamllint   | Lint yaml configuration files     |\n| yapf       | Customizable Code Formatting      |\n\n## Customizing the Command Line Interface\n\nThe CLI has some defaults built in, but is customizable by setting the `PIB_CONFIG_FILE_LOCATION` environment variable.\nThe default config file can be found [here](pib_cli/config/config.yml).\n\nEach command is described by a yaml key in this format :\n\n```yaml\n- name: "command-name"\n  path_method: "location_string"\n  commands:\n    - "one or more"\n    - "shell commands"\n    - "each run in a discrete environment"\n  success: "Success Message"\n  failure: "Failure Message"\n```\n\nwhere `location_string` is one of:\n\n- `project_root` (`/app`)\n- `project_docs` (`/app/documentation`)\n- `project_home` (`/app/${PROJECT_HOME}`)\n\n## Installing a virtual environment, and the CLI on your host machine\n\nThe [scripts/extras.sh](scripts/extras.sh) script does this for you.\n\nFirst install [poetry](https://python-poetry.org/) on your host machine:\n- `pip install poetry`\n\nThen source this script, setup the hostmachine, and you can use the `dev` command on your host:\n- `source scripts/extras.sh`\n- `pib_setup_hostmachine` (to install the poetry dependencies)  \n- `dev --help` (to run the cli outside the container)\n\nIt is still recommended to work inside the container, as you\'ll have access to the full managed python environment, \nas well as any additional services you are running in containers.\n\n## Development Dependencies\n\nYou\'ll need to install:\n\n- [Docker](https://www.docker.com/)\n- [Docker Compose](https://docs.docker.com/compose/install/)\n\n## Setup the Development Environment\n\nBuild the development environment container (this takes a few minutes):\n\n- `docker-compose build`\n\nStart the environment container:\n\n- `docker-compose up -d`\n\nSpawn a shell inside the container:\n\n- `./container`\n',
    'author': 'Niall Byrne',
    'author_email': 'niall@niallbyrne.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/shared-vision-solutions/pib_cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7.0,<3.8.0',
}


setup(**setup_kwargs)
