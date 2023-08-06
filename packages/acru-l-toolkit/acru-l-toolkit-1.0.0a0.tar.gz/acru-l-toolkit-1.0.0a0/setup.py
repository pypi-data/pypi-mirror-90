# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['acrul_toolkit']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.16.40,<2.0.0']

entry_points = \
{'console_scripts': ['docs-autobuild = scripts.docs_autobuild:main',
                     'docs-build = scripts.docs_build:main',
                     'tests = scripts.tests:main']}

setup_kwargs = {
    'name': 'acru-l-toolkit',
    'version': '1.0.0a0',
    'description': '',
    'long_description': '# ACRU-L Toolkit\n\n[![codecov](https://codecov.io/gh/quadio-media/acru-l-toolkit/branch/main/graph/badge.svg?token=1GJo2XhY0S)](https://codecov.io/gh/quadio-media/acru-l-toolkit)\n\n\nPronounced _Ah-crew-el (*ə-kroo͞′l*)_ Toolkit\n\nPartner library to [ACRU-L](https://github.com/quadio-media/acru-l).\n\nThis project houses utilities that makes sense to use both in production application code (e.g. handler base classes) and in the main ACRU-L project, which is intended to only be used in development / devops enviroments.\n',
    'author': 'Anthony Almarza',
    'author_email': 'anthony.almarza@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
