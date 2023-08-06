# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytimetools']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<3.0']

setup_kwargs = {
    'name': 'pytimetools',
    'version': '0.1.2',
    'description': 'a time tools for django',
    'long_description': None,
    'author': 'huoyinghui',
    'author_email': 'hyhlinux@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
