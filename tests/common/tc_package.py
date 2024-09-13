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
# @file        tc_package.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-13     xqyjlj       initial version
#

import os
import unittest

from common import PACKAGE, SETTINGS


class PackageTest(unittest.TestCase):

    def __init__(self, parent: None) -> None:
        super().__init__(parent)

    def setUp(self):
        pass

    def test_install(self):
        file = os.path.join(os.path.dirname(__file__), "resource", "package", "test.7z")
        succeed = 0

        def callback(file: str, progress: float):
            nonlocal succeed
            succeed = progress

        status = PACKAGE.install(
            "C:/Users/xqyjl/Documents/git/github/csplink/csp/build/gcc-arm-none-eabi-10-2020-q4-major.7z", callback)

        self.assertTrue(status, msg='load failed.')
        self.assertGreater(succeed, 0, msg='load failed.')

    def tearDown(self):
        pass
