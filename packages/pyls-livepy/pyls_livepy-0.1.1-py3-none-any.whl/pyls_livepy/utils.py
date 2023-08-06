# Copyright (c) 2021  Andrew Phillips <skeledrew@gmail.com>

#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""

"""


from pathlib import Path
from os import environ as oenv

from loguru import logger
import toml


class LivepyError(BaseException):
    pass


logger.remove(0)
logger.add("pyls-livepy.log", level="WARNING")


def _mark_err(src, msg):
    """Create an error mark for an entire document with the given message.

        >>> type(_mark_err("", "")) == dict
        True
    """
    lines = src.split("\n")
    err_range = {
        "start": {"line": 0, "character": 0},
        "end": {"line": len(lines) - 1, "character": 0},
    }
    marker = {
        "source": "livepy",
        "range": err_range,
        "message": msg,
        "severity": 1,  # lsp.DiagnosticSeverity.Error,
    }
    return marker


def find_project_root(path, name):
    """Find a project's root with the given path and name.

    path -- path to a file/folder in the project.
    name -- name of a file/folder in the project root.
    returns a Path object or None.
    """
    # TODO: move to utils lib
    root = None

    for p in Path(path).parents:
        if name in [f.name for f in p.iterdir()]:
            root = p
    return root


def parse_config(content):
    """Get plugin config from pyproject.toml content or default.

        >>> "env" in parse_config("")
        True
    """
    defaults = {
        "env": ".nox/make_pyls_livepy_test_env",
    }

    if not content:
        return defaults

    try:
        pyproject_toml = toml.loads(content)
    except toml.TomlDecodeError:
        return defaults

    file_config = pyproject_toml.get("tool", {}).get("pyls-livepy", {})
    config = {**defaults, **file_config}
    return config


def resolve_env(rel_path, proot):
    """Convert a possibly relative path to a concrete one.

    The given path can start with a tilde, be a glob and point either directly
    to an activate file or a folder with bin/activate.
    """
    path = Path(rel_path)

    if rel_path.startswith("~"):
        path = path.expanduser()

    if not path.root:
        path = Path(proot) / Path(path)

    if "*" in rel_path:
        try:
            path = sorted(
                Path(path.parent).glob(path.name), key=lambda p: p.name
            )[0]

        except IndexError:
            raise LivepyError(f"Unable to resolve environment at {path}")

    if not path.name.startswith("activate"):
        path = path / "bin/activate"

    if path.name == "activate-conda":
        env_name = path.name

        try:
            env_name = path.read_text().strip()
            path = (Path(oenv["CONDA_PREFIX"]).parent / env_name).resolve()
            assert path.is_dir(), f"{path} is not a folder"

        except Exception as e:
            raise LivepyError(f"Unable to resolve Conda env '{env_name}': {e}")
    return path


def set_log_level(level, logger):
    """Set the logger level."""
    # FIXME: this update will get triggered on each call!
    log_levels = ("debug", "info", "warning", "error")
    msg = f'config log level "{level}" not in {", ".join(log_levels)}'
    assert level.lower() in log_levels, msg
    default = "warning"

    if level != default:
        logger.remove()
        logger.add("pyls-livepy.log", level=level.upper())
    return logger
