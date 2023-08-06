# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['pyls_livepy', 'pyls_livepy.data']

package_data = \
{'': ['*']}

install_requires = \
['loguru>=0.5.3,<0.6.0']

extras_require = \
{'all': ['space-tracer>=4.2.0,<5.0.0',
         'python-language-server>=0.36.1,<0.37.0'],
 'pyls': ['python-language-server>=0.36.1,<0.37.0'],
 'runs': ['space-tracer>=4.2.0,<5.0.0']}

entry_points = \
{'console_scripts': ['pyls-livepy-runner = pyls_livepy.runner:run'],
 'pyls': ['pyls_livepy = pyls_livepy.plugin']}

setup_kwargs = {
    'name': 'pyls-livepy',
    'version': '0.1.0',
    'description': "A realtime debugging and testing plugin for Palantir's Python Language Server.",
    'long_description': None,
    'author': 'Andrew Phillips',
    'author_email': 'skeledrew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
