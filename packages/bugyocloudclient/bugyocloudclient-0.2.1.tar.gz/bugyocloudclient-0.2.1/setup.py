# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bugyocloudclient',
 'bugyocloudclient.endpoints',
 'bugyocloudclient.endpoints.base',
 'bugyocloudclient.models',
 'bugyocloudclient.tasks',
 'bugyocloudclient.utils']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.9.3,<5.0.0', 'requests>=2.25.0,<3.0.0']

setup_kwargs = {
    'name': 'bugyocloudclient',
    'version': '0.2.1',
    'description': 'Bugyo Cloud Client',
    'long_description': None,
    'author': 'sengokyu',
    'author_email': 'sengokyu+gh@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sengokyu/bugyo-cloud-client',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
