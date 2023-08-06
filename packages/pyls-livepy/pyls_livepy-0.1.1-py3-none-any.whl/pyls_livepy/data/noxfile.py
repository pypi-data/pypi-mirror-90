"""
nox (https://nox.thea.codes/) is a command-line tool that automates testing in
multiple Python environments. It uses a standard Python file for configuration.
This file in particular is a generic adapter that reads from a pyproject.toml
file located in the same folder and sets up a live testing environment.

Configurables:
  python -- Python interpreter to use for tests.
  deps -- List of testing dependencies.
  venv -- One of "virtualenv" or "conda".
  pass-env -- List of existing env vars to pass.
  whitelist-externals -- List of apps not installed in env but used.
  commands -- List of commands to run after setup.
  make-env -- List of "var=value" to add to env.
  conda-deps -- List of "conda install" dependencies.
  conda-channel -- Optional channel from which to get packages.
  editable -- Install project in develop mode.

  --test-only -- CLI switch to skip install.
"""


import nox


def ensure_list(v):
    if not isinstance(v, list):
        v = [v]
    return v


def setup_pyls_livepy_test_env_function():
    """Read pyproject.toml and setup the session function."""
    import shlex
    import sys

    from pathlib import Path
    import toml

    pyp_path = Path(__file__).parent / "pyproject.toml"
    deco_args = {}

    if not pyp_path.exists():
        raise OSError("A pyproject.toml file must be in the same folder")
    pyp_toml = toml.loads(pyp_path.read_text())
    pl_nox_sec = pyp_toml.get("tool", {}).get("pyls-livepy", {}).get("nox", {})
    deco_args["python"] = pl_nox_sec.get(
        "python",
        ".".join([str(n) for n in sys.version_info[:2]])
    )
    deco_args["venv_backend"] = pl_nox_sec.get("venv", "virtualenv")

    @nox.session(**deco_args)
    def make_pyls_livepy_test_env(session):
        deps = ensure_list(pl_nox_sec.get("deps", []))
        commands = ensure_list(pl_nox_sec.get("commands", []))
        commands = commands or ["poetry install", "pytest"]
        externals = ensure_list(pl_nox_sec.get("whitelist-externals", []))
        conda_deps = ensure_list(pl_nox_sec.get("conda-deps", []))
        conda_channel = pl_nox_sec.get("conda-channel", None)
        editable = pl_nox_sec.get("editable", False)
        pa = session.posargs
        pkg = [".", "--no-deps"]

        if conda_deps and "--test-only" not in pa:
            if conda_channel:
                conda_deps.append(f"--channel={conda_channel}")
            session.conda_install(*conda_deps)

        if deps and "--test-only" not in pa:
            if editable:
                pkg.insert(0, "-e")
            session.install(*deps)
            session.install(*pkg)
        pa.remove("--test-only") if "--test-only" in pa else None

        for c in commands:
            cmd = shlex.split(c)
            external = True if cmd[0] in externals else False
            cmd.extend(pa) if cmd[0] == "pytest" and pa else None
            session.run(
                *cmd,
                external=external,
            )
        return
    return


setup_pyls_livepy_test_env_function()
