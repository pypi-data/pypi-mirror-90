# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['freshdesk_sso']

package_data = \
{'': ['*']}

install_requires = \
['Django>=2.2.17,<3.0.0']

setup_kwargs = {
    'name': 'django-freshdesk-sso',
    'version': '0.2.0',
    'description': 'Django Freshdesk SSO enables SSO for freshdesk from your django application.',
    'long_description': '====================\nDjango Freshdesk SSO\n====================\n.. image:: https://badge.fury.io/py/django-freshdesk-sso.svg\n    :target: https://badge.fury.io/py/django-freshdesk-sso\n\nDjango Freshdesk SSO enables SSO for freshdesk from your django application.\n\nThis package replaces the stale and out of date `django-freshdesk <https://pypi.org/project/django-freshdesk/>`_ package.\n\nQuick start\n-----------\n\n1. Add "freshdesk_sso" to your INSTALLED_APPS setting like this::\n\n    INSTALLED_APPS = [\n        ...\n        \'freshdesk_sso\',\n    ]\n\n2. Include the freshdesk SSO URLconf in your project urls.py like this::\n\n    path(\'accounts/login/sso/\', include(\'freshdesk_sso.urls\')),\n\n\n3. Add the required environment variables to your settings.py file::\n\n    FRESHDESK_URL = \'http://yourcompany.freshdesk.com/\'\n    FRESHDESK_SECRET_KEY = \'YOUR_SECRET_GOES_HERE\'\n\n',
    'author': 'Wout De Puysseleir',
    'author_email': 'woutdp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/soundradix-website/django-freshdesk-sso',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
