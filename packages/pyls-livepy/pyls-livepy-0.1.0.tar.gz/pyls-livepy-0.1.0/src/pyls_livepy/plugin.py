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


import json
from os import environ as oenv
import subprocess as sp
from pathlib import Path
import sys

from pyls import hookimpl

from pyls_livepy import __version__ as plp_version
from pyls_livepy.utils import (
    _mark_err,
    find_project_root,
    LivepyError,
    logger,
    parse_config,
    resolve_env,
    set_log_level,
)


@hookimpl
def pyls_lint(document):
    logger.info(f"Plugin hooked at {Path(__file__).parent}")
    logger.info(f"and called on {document.path}")
    PYPT = "pyproject.toml"

    try:
        assert plp_version != "unknown"
        path = document.path
        proot = find_project_root(path, PYPT)

        if proot is None:
            raise LivepyError(f'unable to find a "{PYPT}" file')

        if (proot / "disable-pyls-livepy").exists() is True:
            return []
        config = parse_config((proot / PYPT).read_text())
        log_level = config.get("log-level", "warning")
        set_log_level(log_level, logger)

        if config.get("ensure_nox_test_env_maker", True):
            ensure_nox_test_env_maker(proot)
        env = resolve_env(config["env"], proot)
        result = run_tests_in_env(env, document.source, log_level)
        err_msg = f"Expecting a list, not {type(result).__name__}"
        assert isinstance(result, list), err_msg
        logger.debug('"run_tests_in_env" successfully returned')

    except LivepyError as e:
        logger.error(repr(e))
        result = [_mark_err(document.source, str(e))]

    except Exception as e:
        msg = "exception in pyls-livepy; see log"
        logger.exception(f"{repr(e)}\n\n")
        result = [_mark_err(document.source, msg)]
    return result


@hookimpl
def pyls_on_type_formatting(document):
    logger.debug(f"called on {document.path}")

    try:
        result = []  # TODO: implement

    except Exception as e:
        logger.exception(f"{repr(e)}\n\n")
        result = []
    return result


def run_tests_in_env(env: Path, src: str, log_level: str):
    """Run module source using a given environment.

    For best results the module should not run any code upon load.

    env -- A string or path that is ran with the "source" command.
    src -- Source of the module to be tested.
    """
    assert src and isinstance(src, str), "Source must be a string"

    try:
        compile(src, "<test>", "exec")

    except SyntaxError:
        return []
    run_data = {
        "source": src,
        "plp_version": plp_version,
        "log_level": log_level,
    }
    full_env = str(env)

    if not full_env.endswith("activate"):
        conda_bin = Path(oenv.get("CONDA_EXE", ""))
        act = conda_bin.parent / "activate"

        if not act.is_file():
            raise LivepyError("Conda is not active or is badly configured.")
        full_env = f"{act} {env}"

    def make_args(cmd):
        return ["bash", "-c", f"source {full_env.strip()} && {cmd}"]

    plr = "pyls-livepy-runner"
    plr_path = sp.run(
        make_args(f"which {plr}"),
        capture_output=True,
        text=True
    )

    if plr_path.returncode == 1:
        p = env if not env.name == "activate" else env.parent.parent
        err = f'runner not found at "{p}"; please install pyls-livepy'
        return [_mark_err(src, err)]

    elif plr_path.returncode == 0 and not plr_path.stdout.startswith(
            str(env.parent),
    ):
        p = env if not env.name == "activate" else env.parent.parent
        warn = f'Expecting runner at "{p}",'
        warn += f' not "{plr_path.stdout.strip()}"'
        logger.warning(warn)

    elif plr_path.returncode == 0 and plr_path.stdout:
        pass

    else:
        raise OSError("something went wrong detecting the runner path")
    logger.debug(f'sys.prefix = "{sys.prefix}"')
    out = sp.run(
        make_args(plr),
        capture_output=True,
        text=True,
        input="\n\n" + json.dumps(run_data),
    )

    if out.returncode == 0 and out.stdout:
        result = json.loads(out.stdout.rpartition("\n")[2])

    else:
        err = "Unexpecteded result invoking runner.\n"
        err += f"ARGS:\n{out.args}\n\nRETURNCODE: {out.returncode}\n\n"
        err += f"STDOUT:\n{out.stdout}\n\nSTDERR:\n{out.stderr}\n"
        logger.error(err)
        raise LivepyError("Unexpected error invoking runner. See log")
    return result


def ensure_nox_test_env_maker(proot: Path):
    """Ensure that the nox test env can be easily created."""
    pl_noxf = Path(__file__).parent / "data/noxfile.py"
    proot_noxf = proot / "noxfile.py"
    pln_content = pl_noxf.read_text()
    prn_content = proot_noxf.read_text() if proot_noxf.is_file() else ""

    if "setup_pyls_livepy_test_env_function" in prn_content:
        result = 0

    elif prn_content:
        prn_content += pln_content.rpartition("import nox")[2]
        proot_noxf.write_text(prn_content)
        result = 1

    else:
        proot_noxf.write_text(pln_content)
        result = 2
    return result
