# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyruicore', 'pyruicore.data_type', 'pyruicore.model']

package_data = \
{'': ['*']}

install_requires = \
['typing>=3.7.4,<4.0.0']

setup_kwargs = {
    'name': 'pyruicore',
    'version': '0.1.3',
    'description': 'load python dict data to python class',
    'long_description': '# pyruicore\n\n[![Build Status](https://travis-ci.com/RuiCoreSci/pyruicore.svg?branch=master)](https://travis-ci.com/RuiCoreSci/pyruicore) &nbsp; [![Coverage Status](https://coveralls.io/repos/github/RuiCoreSci/pyruicore/badge.svg?branch=master)](https://coveralls.io/github/RuiCoreSci/pyruicore?branch=master) &nbsp; [![codebeat badge](https://codebeat.co/badges/af92f04f-6d5e-4a0a-82c6-53a8bcfb0341)](https://codebeat.co/projects/github-com-ruicoresci-pyruicore-master) &nbsp; ![python3.8](https://img.shields.io/badge/language-python3.8-blue.svg) &nbsp; ![issues](https://img.shields.io/github/issues/RuiCoreSci/pyruicore) ![stars](https://img.shields.io/github/stars/RuiCoreSci/pyruicore) &nbsp; ![license](https://img.shields.io/github/license/RuiCoreSci/pyruicore)\n\n* This package is used to load python dict data to python class.\n\n## Usage\n\n* pip install pyruicore -i https://pypi.org/simple\n\n```py\n\n\nfrom pyruicore import BaseModel, Field\n\n\nclass Department(BaseModel):\n    name: str\n    address: str\n\n\nclass User(BaseModel):\n    age: int = Field(default_factory=lambda: 1)\n    departs: List[Department]\n\n\nuser = User(\n    departs=[\n        {"name": "de1", "address": "address1"},\n        Department(name="2", address="address2"),\n    ]\n)\nuser_dict = user.dict()\n"""\nuser_dict = {\n    "age": 1,\n    "departs": [\n        {"name": "de1", "address": "address1"},\n        {"name": "2", "address": "address2"},\n    ]\n}\n"""\n\n```\n\n##  Maintainers\n\n[@ruicore](https://github.com/ruicore)\n\n## Contributing\n\nPRs are accepted, this is first workout version, may have many bugs, so welcome to point out bugs and fix it.\n\n## License\n\nMIT © 2020 ruicore\n',
    'author': 'ruicore',
    'author_email': 'hrui835@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/RuiCoreSci/pyruicore',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
