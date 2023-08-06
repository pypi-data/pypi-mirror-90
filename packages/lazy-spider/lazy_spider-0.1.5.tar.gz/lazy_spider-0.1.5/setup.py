# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['spider',
 'spider.gerneric',
 'spider.templates',
 'spider.utils',
 'spider.utils.parse']

package_data = \
{'': ['*']}

install_requires = \
['fake-useragent>=0.1.11,<0.2.0',
 'lxml>=4.6.2,<5.0.0',
 'peewee>=3.14.0,<4.0.0',
 'requests>=2.25.1,<3.0.0']

setup_kwargs = {
    'name': 'lazy-spider',
    'version': '0.1.5',
    'description': 'A lazy spider tools which intergrate lxml, requests, peewee......',
    'long_description': None,
    'author': 'notnotype',
    'author_email': '2056369669@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
