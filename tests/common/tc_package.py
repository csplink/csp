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
import sys
import unittest

from PySide6.QtWidgets import QApplication

from common import PACKAGE


class PackageTest(unittest.TestCase):

    def setUp(self):
        app = QApplication(sys.argv)
        pass

    def test_getPackageDescription(self):
        file = os.path.join(os.path.dirname(__file__), "resource", "package", "test.csppdsc")
        print(PACKAGE.getPackageDescription(file))

    def test_install(self):
        file = os.path.join(os.path.dirname(__file__), "resource", "package", "test.7z")
        succeed = 0

        def callback(_: str, progress: float):
            nonlocal succeed
            succeed = progress

        status = PACKAGE.install(file, callback)

        self.assertTrue(status, msg='install failed.')
        self.assertGreater(succeed, 0, msg='install failed.')

    def tearDown(self):
        pass
