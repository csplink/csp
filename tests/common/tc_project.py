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
# @file        tc_project.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-11-07     xqyjlj       initial version
#
import os
import unittest

from common import PROJECT


class ProjectTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_project(self):
        file = os.path.join(
            os.path.dirname(__file__), "resource", "project", "APM32F103ZET6.csp"
        )
        PROJECT.setPath(file)
        project = PROJECT.project()
        self.assertGreater(len(project.name), 0, msg="load failed.")
        self.assertGreater(len(project.targetChip), 0, msg="load failed.")
        self.assertGreater(len(project.vendor), 0, msg="load failed.")
        self.assertGreater(len(project.version), 0, msg="load failed.")
        self.assertGreater(len(project.modules), 0, msg="load failed.")
        self.assertGreater(len(project.gen.origin), 0, msg="load failed.")
        self.assertGreater(len(project.gen.builder), 0, msg="load failed.")
        self.assertGreater(len(project.gen.builderVersion), 0, msg="load failed.")
        self.assertGreater(len(project.gen.hal), 0, msg="load failed.")
        self.assertGreater(len(project.gen.halVersion), 0, msg="load failed.")
        self.assertGreater(project.gen.linker.defaultHeapSize, -2, msg="load failed.")
        self.assertGreater(project.gen.linker.defaultStackSize, -2, msg="load failed.")
        self.assertGreater(len(project.gen.toolchains), 0, msg="load failed.")
        self.assertGreater(len(project.gen.toolchainsVersion), 0, msg="load failed.")
        # self.assertGreater(project.gen.copyLibrary, 0, msg='load failed.')
        # self.assertGreater(project.gen.useToolchainsPackage, 0, msg='load failed.')
        self.assertGreater(len(project.configs.origin), 0, msg="load failed.")

    def tearDown(self):
        pass
