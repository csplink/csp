#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        test.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-31     xqyjlj       initial version
#


import sys
import unittest
from pathlib import Path

import click
from loguru import logger
from utils.sys import SYS_UTILS

__test_folder = SYS_UTILS.exe_folder() / "tests"


@click.group(invoke_without_command=True)
@click.version_option(version=SYS_UTILS.version(), message="%(version)s")
@click.option(
    "--trace",
    type=click.Choice(
        ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    help="Logging level.",
)
@click.pass_context
def cli(ctx: click.Context, trace: str):
    """CSP Server TestCase - CSP TestCase CLI."""

    logger.configure(
        handlers=[
            {
                "sink": sys.stderr,
                "format": "<level>{message}</level>",
                "colorize": True,
                "level": trace or "WARNING",
            }
        ]
    )

    if ctx.invoked_subcommand is not None:
        return

    discover = discover_tests(__test_folder, "tc_*.py")

    print(f"find {discover.countTestCases()} testcases !!!", flush=True)

    result = run_testcase(discover)

    if len(result.errors) + len(result.failures) != 0:
        exit(1)


@cli.command(name="list")
@click.option(
    "--verbose",
    "-v",
    is_flag=True,
    help="Show detailed information about test classes and methods",
)
def cli_list(verbose):
    """List all available test cases."""

    discover = discover_tests(__test_folder, "tc_*.py")
    total = discover.countTestCases()

    if not verbose:
        print(f"Total test cases: {total}", flush=True)
        return

    print(f"Total test cases: {total}", flush=True)
    for test in iter_tests(discover):
        print(f"  {test.id()}", flush=True)


@cli.command(name="run")
@click.argument("path", required=True, type=click.Path(exists=True))
def cli_run(path: str):
    """Run test cases by path (file or directory)."""

    p = Path(path)
    if p.is_dir():
        discover = discover_tests(p, "tc_*.py")
    else:
        discover = discover_tests(p.parent, p.name)

    result = run_testcase(discover)

    if len(result.errors) + len(result.failures) != 0:
        exit(1)


# ---------------------------------------------------------------------------- #


def discover_tests(start_dir: Path, pattern: str) -> unittest.TestSuite:
    """Discover all tests under test_folder."""
    loader = unittest.defaultTestLoader
    return loader.discover(
        start_dir=str(start_dir),
        pattern=pattern,
        top_level_dir=".",
    )


def iter_tests(suite: unittest.TestSuite):
    """Flatten TestSuite into individual test cases."""
    for item in suite:
        if isinstance(item, unittest.TestSuite):
            yield from iter_tests(item)
        else:
            yield item


def run_testcase(suite: unittest.TestSuite) -> unittest.result.TestResult:
    runner = unittest.TextTestRunner(verbosity=1)
    return runner.run(suite)


if __name__ == "__main__":
    cli()
