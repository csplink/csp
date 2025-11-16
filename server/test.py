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


import os
import sys
import unittest

import click
from loguru import logger
from utils.sys import SYS_UTILS

test_folder = os.path.join(SYS_UTILS.exe_folder(), "tests")


@click.group(invoke_without_command=True)
@click.version_option(version=SYS_UTILS.version(), message="%(version)s")
@click.option(
    "--trace",
    type=click.Choice(
        ["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False
    ),
    help="Logging level.",
)
def cli(trace):
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

    discover = unittest.defaultTestLoader.discover(
        start_dir=test_folder, pattern="tc_*.py", top_level_dir="."
    )

    print(
        "find {count} testcases !!!".format(count=discover.countTestCases()), flush=True
    )

    suite = unittest.TestSuite()
    suite.addTest(discover)

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    if len(result.errors) + len(result.failures) != 0:
        exit(1)


if __name__ == "__main__":
    cli()
