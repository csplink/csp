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

from common import PACKAGE, PackageDescriptionType


class PackageTest(unittest.TestCase):

    def setUp(self):
        pass

    def check_getPackageDescription(self, sc: PackageDescriptionType):
        self.assertNotEqual(sc.author.name, "", msg='failed.')
        self.assertNotEqual(sc.author.email, "", msg='failed.')
        self.assertNotEqual(sc.author.website.blog, "", msg='failed.')
        self.assertNotEqual(sc.author.website.github, "", msg='failed.')
        self.assertNotEqual(sc.name, "", msg='failed.')
        self.assertNotEqual(sc.version, "", msg='failed.')
        self.assertNotEqual(sc.license, "", msg='failed.')
        self.assertNotEqual(sc.type, "", msg='failed.')
        self.assertNotEqual(sc.vendor, "", msg='failed.')
        self.assertGreater(len(sc.vendorUrl), 0, msg='install failed.')
        self.assertGreater(len(sc.description), 0, msg='install failed.')
        self.assertGreater(len(sc.url), 0, msg='install failed.')
        self.assertNotEqual(sc.support, "", msg='failed.')

    def test_getPackageDescription(self):
        file = os.path.join(os.path.dirname(__file__), "resource", "package", "test.csppdsc")
        sc = PACKAGE.getPackageDescription(file)
        self.check_getPackageDescription(sc)

        folder = os.path.join(os.path.dirname(__file__), "resource", "package")
        sc = PACKAGE.getPackageDescription(folder)
        self.check_getPackageDescription(sc)

    def test_getPackageIndex(self):
        index = PACKAGE.getPackageIndex()
        self.assertGreater(len(index.origin), 0, msg='install failed.')

    def test_install(self):
        file = os.path.join(os.path.dirname(__file__), "resource", "package", "test.7z")
        succeed = 0

        def callback(_: str, progress: float):
            nonlocal succeed
            succeed = progress

        status = PACKAGE.install(file, callback)

        self.assertTrue(status, msg='install failed.')
        self.assertGreater(succeed, 0, msg='install failed.')

    def test_uninstall(self):
        self.test_install()
        status = PACKAGE.uninstall('hal', 'test', '0.0.2')
        self.assertTrue(status, msg='uninstall failed.')

    def tearDown(self):
        pass
