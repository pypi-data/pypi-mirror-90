# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['janzeng']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.0.0,<3.0.0']

extras_require = \
{':python_version < "3.8"': ['importlib-metadata>=1.0,<2.0']}

setup_kwargs = {
    'name': 'janzeng',
    'version': '0.0.1.dev1',
    'description': 'Game engine for Pygame',
    'long_description': 'Janzeng\n=======\n\nJanzeng\n\nDocumentation\n-------------\n\nDocumentation is located at https://janzeng.readthedocs.io/\n\nFeatures\n--------\n\nMinimal engine to dispatch events, entity system and sprites.\n\nInstallation\n------------\n\nInstall janzeng by running:\n\n    pip install janzeng\n\nContribute\n----------\n\n- Issue Tracker: https://github.com/jtiai/janzeng/issues\n- Source Code: https://github.com/jtiai/janzeng\n\nSupport\n-------\n\n[TBD]\n\nLicense\n-------\n\nThe project is licensed under the 3-clause BSD license.\n\n.. |RTD| image:: https://readthedocs.org/projects/janzeng/badge/?version=latest\n    :target: https://janzeng.readthedocs.io/en/latest/?badge=latest\n    :alt: Documentation Status\n\n.. |lint| image:: https://github.com/jtiai/janzeng/workflows/Test%20and%20lint/badge.svg\n    :alt: Test and lint\n\n.. |publish| image:: https://github.com/jtiai/janzeng/workflows/Build%20and%20publish%20packages/badge.svg\n    :alt: Build and publish packages\n\n.. |pypi| image:: https://img.shields.io/pypi/v/janzeng\n    :target: https://pypi.org/project/janzeng/\n    :alt: PyPi\n',
    'author': 'Jani Tiainen',
    'author_email': 'jani@tiainen.cc',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/jtiai/janzeng',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
