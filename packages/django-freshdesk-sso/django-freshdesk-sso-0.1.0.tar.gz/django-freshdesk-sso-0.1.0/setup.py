# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_freshdesk_sso']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-freshdesk-sso',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Wout De Puysseleir',
    'author_email': 'woutdp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
