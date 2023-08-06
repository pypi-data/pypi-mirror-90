# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cyclopy']

package_data = \
{'': ['*']}

install_requires = \
['GitPython>=3.1.12,<4.0.0']

entry_points = \
{'console_scripts': ['cyclopy = cyclopy:main']}

setup_kwargs = {
    'name': 'cyclopy',
    'version': '1.0',
    'description': 'A tool for calculating the cyclomatic complexity of projects written in python',
    'long_description': '### A tool for calculating the cyclomatic complexity of projects written in python\n\n# Installation\n\n```\npip install cyclopy\n```\n\n# Calculation in a local directory\n\nsingle file:\n\n```python cc.py -f "./cc.py"``` \n\n![single file example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_single.png)\n\nproject:\n\n```python cc.py -s path_to_project_src``` \n\n![example local dir](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_localdir.png)\n\n\n# Computing from git repository\n\n```python3 cc.py -g "https://github.com/Split174/financial-accounting"```\n\n![git example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc1.png)\n\n\n# Calculate with limit flag\n\n```python3 cc.py -g "https://github.com/Split174/financial-accounting" -l 5```\n\n![limit flag example](https://raw.githubusercontent.com/Split174/cyclopy/assets/example_cc_limitflag.png)\n',
    'author': 'Sergey Popov',
    'author_email': 'sergei.popov174@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Split174/cyclopy',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
