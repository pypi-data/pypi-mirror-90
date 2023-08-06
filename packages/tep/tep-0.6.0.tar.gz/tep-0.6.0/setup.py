# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tep',
 'tep.demo',
 'tep.demo.fixtures',
 'tep.demo.tests',
 'tep.demo.tests.sample',
 'tep.demo.tests.sample.case_reuse']

package_data = \
{'': ['*'],
 'tep': ['.pytest_cache/*', '.pytest_cache/v/cache/*'],
 'tep.demo': ['.pytest_cache/*',
              '.pytest_cache/v/*',
              '.pytest_cache/v/cache/*']}

install_requires = \
['allure-pytest>=2.8.16,<3.0.0',
 'allure-python-commons>=2.8.16,<3.0.0',
 'faker>=4.1.1,<5.0.0',
 'jmespath>=0.10.0,<0.11.0',
 'loguru>=0.5.1,<0.6.0',
 'pandas>=1.1.0,<2.0.0',
 'pymysql>=0.10.1,<0.11.0',
 'pyyaml>=5.3.1,<6.0.0',
 'requests>=2.24.0,<3.0.0',
 'sqlalchemy>=1.3.22,<2.0.0',
 'texttable>=1.6.3,<2.0.0',
 'urllib3>=1.25.9,<2.0.0']

entry_points = \
{'console_scripts': ['tep = tep.cli:main'],
 'pytest11': ['tep = tep.plugin:Plugin']}

setup_kwargs = {
    'name': 'tep',
    'version': '0.6.0',
    'description': 'tep is a testing tool to help you write pytest more easily. Try Easy Pytest!',
    'long_description': '# tep\n\ntep is a testing tool to help you write pytest more easily. Try Easy Pytest!\n\n# Design Philosophy\n\n- Simple is better\n- Everyone can write automation in python\n\n# Installation\n\n`tep` is developed with Python, it supports Python `3.6+` and most operating systems.\n\n`tep` is available on [`PyPI`](https://pypi.python.org/pypi) and can be installed through `pip`.\n\n```\n$ pip install tep\n```\n\nor domestic mirror.\n\n```\n$ pip --default-timeout=600 install -i https://pypi.tuna.tsinghua.edu.cn/simple tep\n```\n\n# Check Installation\n\nWhen tep is installed, tep command will be added in your system.\n\nTo see `tep` version:\n\n```\n$ tep -V  # tep --version\n0.2.3\n```\n\n# Usage\n\nIf you want to know more usages, you can read [pytest docs](https://docs.pytest.org/).\n\nYou know pytest.\n\nYou know tep.\n',
    'author': 'dongfanger',
    'author_email': 'dongfanger@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/dongfanger/tep',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.1,<4.0.0',
}


setup(**setup_kwargs)
