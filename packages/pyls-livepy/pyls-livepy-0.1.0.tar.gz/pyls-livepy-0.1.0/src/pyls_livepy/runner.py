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


import doctest
import json
from pathlib import Path
import subprocess as sp
import sys
import types

from pyls_livepy import __version__ as plr_version
from pyls_livepy.utils import (
    _mark_err,
    LivepyError,
    logger,
    set_log_level,
)


def _get_stdin():
    return "".join([ln for ln in sys.stdin])


def _put_stdout(out):
    sys.stdout.write(out)
    return


class CapDocTestRunner(doctest.DocTestRunner):
    def report_failure(self, out, test, example, got):
        res = {
            "type": "failure",
            "test": test,
            "example": example,
            "got": got,
        }
        out(res)
        return

    def report_unexpected_exception(self, out, test, example, exc_info):
        res = {
            "type": "exception",
            "test": test,
            "example": example,
            "exc_info": exc_info,
        }
        out(res)
        return

    def report_success(self, out, test, example, got):
        res = {
            "type": "success",
            "test": test,
            "example": example,
            "got": got,
        }
        out(res)
        return

    def report_start(self, out, test, example):
        return


def capout(hold=None):
    """Capture values as a callable and return them elsewhere."""
    hold = hold or []

    def inner(val=NotImplemented):
        nonlocal hold
        if val is NotImplemented:
            return hold

        else:
            hold.append(val)
        return

    return inner


def run_doctests(src, which=None):
    """Run the doctests in a document."""
    # TODO: move to runner module
    run_env = sp.run(
        ["bash", "-c", "which pyls-livepy-runner"],
        capture_output=True,
        text=True,
    ).stdout.strip()
    logger.info(f'Runner at "{run_env}"')
    mod = types.ModuleType("mod")  # TODO: get name from document
    w_path = "\n  ".join(sys.path)
    logger.info(f"Working PATH:\n  {w_path}\n")

    try:
        exec(src, mod.__dict__)

    except Exception as e:
        logger.exception(f"Exception while exec'ing MUT: {repr(e)}")
        return {}
    doctests = doctest.DocTestFinder().find(mod)
    runner = CapDocTestRunner()
    results = {}

    for dt in doctests:
        # TODO: allow filtering by 'which'
        if not dt.examples:
            continue
        co = capout()
        res = runner.run(dt, out=co)._asdict()
        bad = [tr for tr in co() if tr["type"] in ["failure", "exception"]]
        res["out"] = bad
        results[dt.name] = res
    return results


def create_markers(results):
    """Create diagnostic lint markers for failing doctests."""
    err_msg = f"Expected a dict but got {type(results).__name__}"
    assert isinstance(results, dict), err_msg
    markers = []

    for name, res in results.items():
        out = res["out"]

        for tr in out:
            ex = tr["example"]
            lineno = tr["test"].lineno + ex.lineno
            offset = ex.indent + 4
            err_range = {
                "start": {"line": lineno, "character": offset},
                "end": {
                    "line": lineno,
                    "character": offset + len(ex.source) - 1,
                },
            }
            msg = f"{tr['type']} in doctest"
            marker = {
                "source": "livepy",
                "range": err_range,
                "message": msg,
                "severity": 1,  # lsp.DiagnosticSeverity.Error,
            }
            markers.append(marker)
    return markers


def run():
    """Run doctests and print diagnostic markers.

    Only accepts input from stdin and writes output as JSON to stdout."""
    run_data = json.loads(_get_stdin().rpartition("\n")[2])
    src = run_data["source"]
    plp_version = run_data["plp_version"]
    log_level = run_data["log_level"]
    set_log_level(log_level, logger)
    logger.debug(f'sys.prefix = "{sys.prefix}"')
    logger.info(f'Runner active at "{Path(__file__).parent}"')

    if plp_version == plr_version:
        markers = create_markers(run_doctests(src))

    else:
        err = "version mismatch error; "
        err += f"plugin: {plp_version} vs runner: {plr_version}"
        logger.error(repr(LivepyError(err)))
        markers = _mark_err(src, err)
    _put_stdout("\n\n" + json.dumps(markers))
    return
