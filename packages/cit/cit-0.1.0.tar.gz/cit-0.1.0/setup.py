# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cit']

package_data = \
{'': ['*']}

install_requires = \
['sh>=1.14.1,<2.0.0']

setup_kwargs = {
    'name': 'cit',
    'version': '0.1.0',
    'description': '让github的下载速度比之前快一千倍',
    'long_description': None,
    'author': '中箭的吴起',
    'author_email': 'solider245@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
