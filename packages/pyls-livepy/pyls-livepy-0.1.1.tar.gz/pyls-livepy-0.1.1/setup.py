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
    'version': '0.1.1',
    'description': "A realtime debugging and testing plugin for Palantir's Python Language Server.",
    'long_description': '===========\npyls-livepy\n===========\n\n\nA realtime debugging and testing plugin for Palantir\'s `Python Language Server <https://github.com/palantir/python-language-server>`_ (pyls).\n\n\n\nWho is it for?\n==============\n\nAnyone who creates/maintains projects in Python.\n\n\nWhy?\n====\n\nDebugging and testing tends to be fairly separate from editing code. Typically a developer needs to run tests each time changes are made and a file saved, and start a debug session when a non-obvious error is found. This slows down the development process considerably.\n\nThis plugin uses features provided by the `language server protocol <https://microsoft.github.io/language-server-protocol/>`_ (LSP) - as implemented in pyls - to run tests and provide debugging data* whenever code is updated, making the debug+test feedback process realtime.\n\n\n\nHow can I start using it?\n=========================\n\n- Install pyls into an IDE with LSP support (`instructions <https://github.com/palantir/python-language-server>`_).\n- Install pyls-livepy into pyls, specifying the "pyls" extra.\n    ::\n\n     pip install pyls-livepy[pyls]\n- Ensure your project has a pyproject.toml file created with `poetry <https://python-poetry.org/>`_.\n- Install pyls-livepy into the project, specifying the "runs" extra.\n    ::\n\n     poetry add --dev pyls-livepy[runs]\n- Install `nox <https://nox.thea.codes/en/stable/>`_ so it can be ran from within the project (globally is recommended).\n- Open a Python project file in the editor to ensure pyls-livepy is detected, and to generate the `nox` config.\n- Run `nox` at least once to create the project\'s environment.\n- Write doctests** as you write your code; any failing/throwing tests will be marked.\n- To disable per project, create a file called `disable-pyls-livepy` in the project\'s root folder.\n\n\nWhat is the (default) expected behavior?\n========================================\n\nIn addition to making debugging and testing easier, this plugin also aims to promote the use of `modern methods and tools <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/>`_ for working with Python projects. It can be configured for other tools, but no configuration is required when `nox`, `poetry` and `pytest` are used. By default, the plugin:\n\n- Creates a *noxfile.py* in the project or a pyls-livepy session is added if one exists (once a project file is accessed).\n- Uses `poetry` to install the project into an existing nox environment.\n- Runs tests on every syntatically correct change.\n- Indicates failing/exception-throwing tests via LSP diagnostic markers.\n\n\nWhere can I find more information?\n==================================\n\nFurther documentation is a work in progress.\n\n\nNotes\n=====\n\n- Due to the fact that this plugin must be installed into the project, and it was created for Python v3.7, the project must also use minimum 3.7.\n- `*` Debug data view functionality has not yet been implemented (as of v0.1.0).\n- `**` Eventually this project will also be able to run pytest tests.\n- This project has been set up using PyScaffold 3.2.3. For details and usage\n  information on PyScaffold see https://pyscaffold.org/.\n',
    'author': 'Andrew Phillips',
    'author_email': 'skeledrew@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/skeledrew/pyls-livepy',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
