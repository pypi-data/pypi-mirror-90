# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_qiyu_utils']

package_data = \
{'': ['*']}

install_requires = \
['django>=3.1,<3.2']

setup_kwargs = {
    'name': 'django-qiyu-utils',
    'version': '0.1.0',
    'description': 'Django Utils for internal use',
    'long_description': '# django utils for internal use\n\nQiYuTech Django Utils(Only for internal use)\n\n# WARNING\n\nUSE IT AT YOUR OWN RISK!!\n',
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
