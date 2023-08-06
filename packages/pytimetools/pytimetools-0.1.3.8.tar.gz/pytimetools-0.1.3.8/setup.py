# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytimetools']

package_data = \
{'': ['*']}

install_requires = \
['pytz>=2019.2,<2020.0']

setup_kwargs = {
    'name': 'pytimetools',
    'version': '0.1.3.8',
    'description': 'a time tools for django',
    'long_description': None,
    'author': 'huoyinghui',
    'author_email': 'hyhlinux@163.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/pydtools/pytimetools/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
}


setup(**setup_kwargs)
