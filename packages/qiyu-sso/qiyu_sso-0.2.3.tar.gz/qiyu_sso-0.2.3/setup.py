# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['qiyu_sso', 'qiyu_sso.api', 'qiyu_sso.forms', 'qiyu_sso.resp']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp>=3,<4', 'pydantic>=1.7,<2', 'requests>=2,<3']

setup_kwargs = {
    'name': 'qiyu-sso',
    'version': '0.2.3',
    'description': 'SSO client from QiYuTech',
    'long_description': "# QiYu-SSO Client\n\n![Upload Python Package To Pypi](https://github.com/QiYuTechDev/qiyu-sso/workflows/Upload%20Python%20Package%20To%20Pypi/badge.svg)\n![Code Format Check](https://github.com/QiYuTechDev/qiyu-sso/workflows/Code%20Format%20Check/badge.svg)\n\nONLY FOR INTERNAL USE, CURRENTLY\n\nIt's may be useless for you :)\n",
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
