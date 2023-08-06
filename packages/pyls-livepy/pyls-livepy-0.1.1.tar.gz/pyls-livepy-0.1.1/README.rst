===========
pyls-livepy
===========


A realtime debugging and testing plugin for Palantir's `Python Language Server <https://github.com/palantir/python-language-server>`_ (pyls).



Who is it for?
==============

Anyone who creates/maintains projects in Python.


Why?
====

Debugging and testing tends to be fairly separate from editing code. Typically a developer needs to run tests each time changes are made and a file saved, and start a debug session when a non-obvious error is found. This slows down the development process considerably.

This plugin uses features provided by the `language server protocol <https://microsoft.github.io/language-server-protocol/>`_ (LSP) - as implemented in pyls - to run tests and provide debugging data* whenever code is updated, making the debug+test feedback process realtime.



How can I start using it?
=========================

- Install pyls into an IDE with LSP support (`instructions <https://github.com/palantir/python-language-server>`_).
- Install pyls-livepy into pyls, specifying the "pyls" extra.
    ::

     pip install pyls-livepy[pyls]
- Ensure your project has a pyproject.toml file created with `poetry <https://python-poetry.org/>`_.
- Install pyls-livepy into the project, specifying the "runs" extra.
    ::

     poetry add --dev pyls-livepy[runs]
- Install `nox <https://nox.thea.codes/en/stable/>`_ so it can be ran from within the project (globally is recommended).
- Open a Python project file in the editor to ensure pyls-livepy is detected, and to generate the `nox` config.
- Run `nox` at least once to create the project's environment.
- Write doctests** as you write your code; any failing/throwing tests will be marked.
- To disable per project, create a file called `disable-pyls-livepy` in the project's root folder.


What is the (default) expected behavior?
========================================

In addition to making debugging and testing easier, this plugin also aims to promote the use of `modern methods and tools <https://cjolowicz.github.io/posts/hypermodern-python-01-setup/>`_ for working with Python projects. It can be configured for other tools, but no configuration is required when `nox`, `poetry` and `pytest` are used. By default, the plugin:

- Creates a *noxfile.py* in the project or a pyls-livepy session is added if one exists (once a project file is accessed).
- Uses `poetry` to install the project into an existing nox environment.
- Runs tests on every syntatically correct change.
- Indicates failing/exception-throwing tests via LSP diagnostic markers.


Where can I find more information?
==================================

Further documentation is a work in progress.


Notes
=====

- Due to the fact that this plugin must be installed into the project, and it was created for Python v3.7, the project must also use minimum 3.7.
- `*` Debug data view functionality has not yet been implemented (as of v0.1.0).
- `**` Eventually this project will also be able to run pytest tests.
- This project has been set up using PyScaffold 3.2.3. For details and usage
  information on PyScaffold see https://pyscaffold.org/.
