# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dp2rathena']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.1,<6.0.0',
 'click>=7.1.2,<8.0.0',
 'python-dotenv>=0.15.0,<0.16.0',
 'tortilla>=0.5.0,<0.6.0']

entry_points = \
{'console_scripts': ['dp2rathena = dp2rathena.cli:dp2rathena']}

setup_kwargs = {
    'name': 'dp2rathena',
    'version': '0.1.1',
    'description': 'Convert Divine-Pride API data to rAthena YAML',
    'long_description': "# dp2rathena: Divine-Pride API to rAthena\n\n[![PyPI](https://img.shields.io/pypi/v/dp2rathena)](https://pypi.org/project/dp2rathena/)\n[![TravisCI Status](https://img.shields.io/travis/com/Latiosu/dp2rathena)](https://travis-ci.com/github/Latiosu/dp2rathena)\n\nConvert Divine-Pride API data to rAthena DB formats (item_db.yml).\n\n## Requirements\n\n* Python 3.7+\n\n## Installation\n\n```\npip install dp2rathena\n```\n\n## Usage\n\nGenerate a [divine-pride.net](https://www.divine-pride.net/) API key if you don't have one yet.\n\n```bash\n# Fetch items with id 501 and 1101\ndp2rathena item --api-key <your-api-key> -i 501 -i 1101\n```\n\nAlternatively, you can use an environment variable to pass your API key:\n```bash\nexport DIVINEPRIDE_API_KEY=<your-api-key>\ndp2rathena item -i 501 -i 1101\n```\n\n## Contributing\n\nThis project uses [poetry](https://python-poetry.org/) to manage the development enviroment.\n\n* Setup a local development environment with `poetry install`.\n* Run tests with `poetry run pytest`\n* Execute script with `poetry run dp2rathena`\n\n## Changelog\n\nSee [CHANGELOG.md](https://github.com/Latiosu/dp2rathena/blob/master/CHANGELOG.md)\n\n## License\n\nSee [LICENSE](https://github.com/Latiosu/dp2rathena/blob/master/LICENSE)\n",
    'author': 'Eric Liu',
    'author_email': 'latiosworks@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Latiosu/dp2rathena',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
