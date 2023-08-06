# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dailycovid']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.0.0,<4.0.0', 'numpy>=1.0.0,<2.0.0', 'requests>=2.24.0,<3.0.0']

entry_points = \
{'console_scripts': ['dailycovid = dailycovid:main']}

setup_kwargs = {
    'name': 'dailycovid',
    'version': '1.0.4',
    'description': 'U.S.A daily covid information.',
    'long_description': '# dailycovid - Easily get covid updates\n\n# Pypi installation\n`pip3 install dailycovid`\n\n# Usage\n\n\n## Simplest\n\n`dailycovid -s statecode`\n\n## Specific Counties in a State\n\nThree ways to do the same thing.\n\n`dailycovid -sc "California-Los Angeles"`\n\n`dailycovid -s CA -c "Los Angeles"`\n\n`dailycovid --state CA --county "Los Angeles"`\n\n## Updating Data\n\nOn the first run it will download a csv file containing the most recent data.\n\n\nUse `dailycovid -g` to update the cache.\n\n\n# Examples of plots\n\n![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_los-angeles_california.png)\n\n![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_suffolk_massachusetts.png)   \n\n![image](https://raw.githubusercontent.com/Fitzy1293/daily-covid/master/examples/plots_new-york-city_new-york.png)\n',
    'author': 'fitzy1293',
    'author_email': 'berkshiremind@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
