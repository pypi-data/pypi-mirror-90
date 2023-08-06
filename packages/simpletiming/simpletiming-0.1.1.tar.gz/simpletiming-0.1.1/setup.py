# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simpletiming']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'simpletiming',
    'version': '0.1.1',
    'description': '',
    'long_description': '<h1 align="center">\n    <strong>Simple Timing</strong>\n</h1>\n<p align="center">\n    <a href="https://github.com/Kludex/simpletiming" target="_blank">\n        <img src="https://img.shields.io/github/last-commit/Kludex/simpletiming" alt="Latest Commit">\n    </a>\n        <img src="https://img.shields.io/github/workflow/status/Kludex/simpletiming/Test">\n        <img src="https://img.shields.io/codecov/c/github/Kludex/simpletiming">\n    <br />\n    <a href="https://pypi.org/project/simpletiming" target="_blank">\n        <img src="https://img.shields.io/pypi/v/simpletiming" alt="Package version">\n    </a>\n    <img src="https://img.shields.io/pypi/pyversions/simpletiming">\n    <img src="https://img.shields.io/github/license/Kludex/simpletiming">\n</p>\n\n## Installation\n\n``` bash\npip install simpletiming\n```\n\n## Usage\n\n###  As decorator\n\n``` Python\nfrom simpletiming import Timer\nfrom time import sleep\n\n@Timer(name="Potato")\ndef potato():\n    sleep(1)\n\npotato()\n\n# Elapsed time: 1.0011 seconds\n```\n\n### As object\n\n``` Python\ntimer = Timer()\n\ntimer.start()\nsleep(1)\ntimer.stop()\n\n# Elapsed time 1.0011 seconds\n```\n\n### As context manager\n\n``` Python\nwith Timer(message="Elapsed time: {minutes:0.4f} minutes"):\n    sleep(1)\n\n# Elapsed time: 0.0167 minutes\n```\n\n### On all class methods\n\n``` Python\n@Timer(name="MyClass", message="{name}: {seconds:0.4f} seconds")\nclass MyClass:\n    def potato(self):\n        sleep(1)\n\nobj = MyClass()\nobj.potato()\n\n# MyClass: 1.0011 seconds\n```\n\n## License\n\nThis project is licensed under the terms of the MIT license.\n',
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
