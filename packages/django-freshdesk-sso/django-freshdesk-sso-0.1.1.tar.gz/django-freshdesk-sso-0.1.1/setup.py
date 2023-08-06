# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_freshdesk_sso']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'django-freshdesk-sso',
    'version': '0.1.1',
    'description': 'Django Freshdesk SSO enables SSO for freshdesk from your django application.',
    'long_description': '====================\nDjango Freshdesk SSO\n====================\n\nDjango Freshdesk SSO enables SSO for freshdesk from your django application.\n\nQuick start\n-----------\n\n1. Add "freshdesk_sso" to your INSTALLED_APPS setting like this::\n\n    INSTALLED_APPS = [\n        ...\n        \'freshdesk_sso\',\n    ]\n\n2. Include the freshdesk SSO URLconf in your project urls.py like this::\n\n    path(\'accounts/login/sso/\', include(\'freshdesk_sso.urls\')),\n\n\n3. Add the required environment variables to your settings.py file::\n\n    FRESHDESK_URL = \'http://yourcompany.freshdesk.com/\'\n    FRESHDESK_SECRET_KEY = \'YOUR_SECRET_GOES_HERE\'\n\n',
    'author': 'Wout De Puysseleir',
    'author_email': 'woutdp@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/soundradix-website/django-freshdesk-sso',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
