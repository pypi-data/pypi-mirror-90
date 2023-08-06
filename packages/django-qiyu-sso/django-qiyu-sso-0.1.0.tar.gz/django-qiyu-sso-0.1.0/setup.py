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
['django-qiyu-utils>=0.2,<0.3', 'django>=3.1,<3.2', 'qiyu-sso>=0.2.5,<0.3']

setup_kwargs = {
    'name': 'django-qiyu-sso',
    'version': '0.1.0',
    'description': 'QiYu SSO intergation for Django',
    'long_description': '# django-qiyu-sso\n\nQiYu SSO django integration\n\n![PyPI - Version](https://img.shields.io/pypi/v/django-qiyu-sso)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-qiyu-sso)\n![PyPI - Downloads](https://img.shields.io/pypi/dm/py_apple_signin)\n![PyPI - Wheel](https://img.shields.io/pypi/wheel/django-qiyu-sso)\n![GitHub repo size](https://img.shields.io/github/repo-size/qiyutechdev/py_apple_signin)\n![Lines of code](https://img.shields.io/tokei/lines/github/qiyutechdev/py_apple_signin)\n',
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
