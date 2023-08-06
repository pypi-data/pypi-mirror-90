# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpletiming']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simpletiming',
    'version': '0.1.0',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>Simple Timing</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/simpletiming" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/simpletiming" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/simpletiming/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/simpletiming">\n    <br />\n    <a href="https://pypi.org/project/simpletiming" target="_blank">\n        <img src="https://img.shields.io/pypi/v/simpletiming" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/simpletiming">\n    <img src="https://img.shields.io/github/license/Kludex/simpletiming">\n</p>\n\n\n## Installation\n\n``` bash\npip install simpletiming\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
    'author': 'Marcelo Trylesinski',
    'author_email': 'marcelotryle@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Kludex/simpletiming',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
