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
# @file        tc_database.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-13     xqyjlj       initial version
#

import unittest

from common import DATABASE


class DatabaseTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_getRepository(self):
        repository = DATABASE.getRepository()
        self.assertGreater(len(repository), 0, msg='load failed.')

    def test_getSummary(self):
        repository = DATABASE.getRepository()
        soc = repository["soc"]
        for companyName, companyItem in soc.items():
            for seriesName, seriesItem in companyItem.items():
                for lineName, lineItem in seriesItem.items():
                    for socName, socItem in lineItem.items():
                        summary = DATABASE.getSummary(companyName, socName)
                        self.assertGreater(len(summary),
                                           0,
                                           msg=f'load failed in {companyName}/{seriesName}/{lineName}/{socName}')

    def test_getIp(self):
        repository = DATABASE.getRepository()
        soc = repository["soc"]
        for companyName, companyItem in soc.items():
            for seriesName, seriesItem in companyItem.items():
                for lineName, lineItem in seriesItem.items():
                    for socName, socItem in lineItem.items():
                        summary = DATABASE.getSummary(companyName, socName)
                        modules = summary["modules"]
                        for groupName, groupItem in modules.items():
                            for moduleName, moduleItem in groupItem.items():
                                ipName = moduleItem.get("ip", "nil")
                                if ipName == "nil":
                                    continue
                                ip = DATABASE.getIp(companyName, ipName)
                                self.assertGreater(len(ip), 0,
                                                   msg=
                                                   f'load failed in {companyName}/{seriesName}/{lineName}/{socName}/{groupName}/{groupName}/{moduleName}/{ipName}'
                                                   )

    def tearDown(self):
        pass
