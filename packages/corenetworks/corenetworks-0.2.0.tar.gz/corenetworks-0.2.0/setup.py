# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['corenetworks',
 'corenetworks.test',
 'corenetworks.test.fixtures',
 'corenetworks.test.unit']

package_data = \
{'': ['*']}

install_requires = \
['jsonschema>=3.2.0,<4.0.0', 'requests>=2.25.1,<3.0.0', 'six>=1.15.0,<2.0.0']

setup_kwargs = {
    'name': 'corenetworks',
    'version': '0.2.0',
    'description': 'Python library for the core-networks.de DNS API.',
    'long_description': '# corenetworks\n\n[![Build Status](https://img.shields.io/drone/build/thegeeklab/corenetworks?logo=drone)](https://cloud.drone.io/thegeeklab/corenetworks)\n[![Python Version](https://img.shields.io/pypi/pyversions/corenetworks.svg)](https://pypi.org/project/corenetworks/)\n[![PyPI Status](https://img.shields.io/pypi/status/corenetworks.svg)](https://pypi.org/project/corenetworks/)\n[![PyPI Release](https://img.shields.io/pypi/v/corenetworks.svg)](https://pypi.org/project/corenetworks/)\n[![Codecov](https://img.shields.io/codecov/c/github/thegeeklab/corenetworks)](https://codecov.io/gh/thegeeklab/corenetworks)\n[![GitHub contributors](https://img.shields.io/github/contributors/thegeeklab/corenetworks)](https://github.com/thegeeklab/corenetworks/graphs/contributors)\n[![License: MIT](https://img.shields.io/github/license/thegeeklab/corenetworks)](https://github.com/thegeeklab/corenetworks/blob/main/LICENSE)\n\nPython library for the [https://core-networks.de](https://beta.api.core-networks.de/doc/) DNS API.\n\nYou can find the full documentation at [https://corenetworks.geekdocs.de](https://corenetworks.geekdocs.de/).\n\n## Contributors\n\nSpecial thanks goes to all [contributors](https://github.com/thegeeklab/corenetworks/graphs/contributors). If you would like to contribute,\nplease see the [instructions](https://github.com/thegeeklab/corenetworks/blob/main/CONTRIBUTING.md).\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](https://github.com/thegeeklab/corenetworks/blob/main/LICENSE) file for details.\n',
    'author': 'Robert Kaussow',
    'author_email': 'mail@thegeeklab.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/thegeeklab/corenetworks/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.0,<4.0.0',
}


setup(**setup_kwargs)
