# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_qiyu_sso',
 'django_qiyu_sso.logic',
 'django_qiyu_sso.migrations',
 'django_qiyu_sso.views']

package_data = \
{'': ['*'], 'django_qiyu_sso': ['templates/user/*']}

install_requires = \
['django-qiyu-utils>=0.1,<0.2', 'django>=3.1,<3.2', 'qiyu-sso>=0.2.5,<0.3']

setup_kwargs = {
    'name': 'django-qiyu-sso',
    'version': '0.0.1',
    'description': 'QiYu SSO intergation for Django',
    'long_description': '# django-qiyu-sso\n\nQiYu SSO django intertation\n',
    'author': 'dev',
    'author_email': 'dev@qiyutech.tech',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
