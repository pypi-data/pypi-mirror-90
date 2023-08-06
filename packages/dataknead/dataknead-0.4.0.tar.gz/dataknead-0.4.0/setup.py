# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dataknead', 'dataknead.loaders']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.5,<4.0.0', 'toml>=0.10.2,<0.11.0', 'xmltodict>=0.12.0,<0.13.0']

entry_points = \
{'console_scripts': ['knead = dataknead.console:run']}

setup_kwargs = {
    'name': 'dataknead',
    'version': '0.4.0',
    'description': 'Fluent conversion between data formats like JSON, XML and CSV',
    'long_description': '# dataknead\n**Fluent conversion between data formats like JSON, XML and CSV**\n\n[Read the docs](https://hay.github.io/dataknead/)\n\nEver sighed when you wrote code to convert CSV to JSON for the thousandth time?\n\n```python\nimport csv\nimport json\n\ndata = []\n\nwith open("cities.csv") as f:\n    reader = csv.DictReader(f)\n\n    for row in reader:\n        data.append(row)\n\nwith open("cities.json", "w") as f:\n    json.dump(data, f)\n```\n\nStop sighing and use `dataknead`. Fetch it with `pip`:\n\n```bash\n$ pip install dataknead\n```\n\nAnd use it like this:\n\n```python\nfrom dataknead import Knead\nKnead("cities.csv").write("cities.json")\n```\n\nOr make it even easier on the command line:\n\n```bash\nknead cities.csv cities.json\n```\n\n`dataknead` has inbuilt loaders for CSV, Excel, JSON, TOML and XML and you can easily write your own.\n\nPiqued your interest? [Read the docs!](https://hay.github.io/dataknead/).',
    'author': 'Hay Kranen',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://hay.github.io/dataknead/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
