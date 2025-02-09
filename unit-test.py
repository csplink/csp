#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        tester.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-13     xqyjlj       initial version
#

import sys
import unittest

from PySide6.QtWidgets import QApplication


def main(folder):
    stdout = sys.stdout
    sys.stdout = None

    discover = unittest.defaultTestLoader.discover(
        start_dir=folder, pattern="tc_*.py", top_level_dir="."
    )

    sys.stdout = stdout

    app = QApplication(sys.argv)

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
    main("./tests")
