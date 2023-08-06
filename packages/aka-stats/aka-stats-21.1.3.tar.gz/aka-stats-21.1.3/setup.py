# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aka_stats']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0', 'pytz>=2019.3,<2020.0', 'redis>=3.4.1,<4.0.0']

extras_require = \
{'fastapi': ['fastapi>=0.54.1,<0.55.0']}

setup_kwargs = {
    'name': 'aka-stats',
    'version': '21.1.3',
    'description': '',
    'long_description': None,
    'author': 'Michal Mazurek',
    'author_email': 'mazurek.michal@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
