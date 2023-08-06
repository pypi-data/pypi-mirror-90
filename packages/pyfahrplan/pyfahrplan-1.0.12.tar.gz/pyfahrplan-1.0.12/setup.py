# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfahrplan']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'python-dateutil>=2.8.1,<3.0.0',
 'requests>=2.22.0,<3.0.0',
 'requests_cache>=0.5.2,<0.6.0',
 'tabulate>=0.8.7,<0.9.0']

entry_points = \
{'console_scripts': ['pyfahrplan = pyfahrplan.pyfahrplan:cli']}

setup_kwargs = {
    'name': 'pyfahrplan',
    'version': '1.0.12',
    'description': 'A CCC Fahrplan CLI',
    'long_description': "# pyfahrplan\n\nCLI application for several CCC fahrplan files\n\n## Usage\n\n```\nUsage: pyfahrplan.py [OPTIONS]\n\nOptions:\n  -s, --speaker TEXT              Name of a speaker you want to search.\n  -t, --title TEXT                A part of the title of the talk(s) you want\n                                  to search.\n  -tr, --track TEXT               A part of the track description you want to\n                                  search.\n  -d, --day INTEGER               Day you want to filter [1-4] or 0 for all\n                                  days.\n  -st, --start TEXT               Start time of the talk(s) you want to\n                                  search.\n  -r, --room TEXT                 Name of the room you want to filter [room\n                                  names] or 'all' for all rooms\n  -c, --conference TEXT           CCC acronym (32c3 to 36c3 plus rc3) that you\n                                  want to filter on, all for all conferences\n  --show-abstract                 Shows abstracts, default False, experimental\n  --show-description              Shows descriptions, default False,\n                                  experimental\n  --sort [day|speakers|title|track|room]\n                                  Sort by day|speakers|title|track|room\n  --reverse                       Reverse results\n  --tablefmt [simple|plain|grid|fancy_grid|github|pipe|orgtbl|jira|presto|pretty|psql|rst|mediawiki|moinmoin|youtrack|html|latex|latex_raw|latex_booktabs|tsv|textile]\n                                  Choose a tableformat that is supported by\n                                  python-tabular\n  --column-width INTEGER          Set the max width of the wide columns (which is everything string based)\n  --update-cache                  Delete the cache file and redownload all fahrplans\n  --help                          Show this message and exit.\n```\n\n## Development\n\nClone this repository, then create a virtualenv, e.g., inside the repository:\n\n```bash\npython3 -m venv .venv\npip install poetry  # if you don't have it globally installed\npoetry install  # install all dependencies, including dev dependencies\npoe test  # to run the tests\npytest --cov=pyfahrplan tests/ && coverage html  # to create a coverage report\n```\n",
    'author': 'Sascha',
    'author_email': 'saschalalala@github.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/saschalalala/pyfahrplan',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
