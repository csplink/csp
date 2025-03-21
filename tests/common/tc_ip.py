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
# @file        tc_ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-11-03     xqyjlj       initial version
#

import unittest

from common import Repository, SUMMARY, IP, IpType


class IpTest(unittest.TestCase):

    def setUp(self):
        pass

    def _find_default_condition(
        self, conditions: list[IpType.ConditionUnitType]
    ) -> IpType.ConditionUnitType | None:
        for condition in conditions:
            if condition._condition == "default":
                return condition
        return None

    def test_getIp(self):
        repository = Repository()
        socs = repository.repository().all_soc()
        for soc in socs:
            summary = SUMMARY.get_summary(soc.vendor, soc.name)
            modules = {}
            modules.update(summary.modules.peripherals)
            modules.update(summary.modules.middlewares)
            for _, group in modules.items():
                for name, module in group.items():
                    if len(module.ip) == 0:
                        continue
                    ip = IP.get_ip(soc.vendor, name, module.ip)
                    self.assertGreater(len(ip.parameters), 0, msg="load failed.")
                    for _, parameter in ip.parameters.items():
                        self.assertGreater(len(parameter.type), 0, msg="load failed.")
                        for _, value in parameter.values.items():
                            self.assertGreater(
                                len(value.comment.origin), 0, msg="load failed."
                            )
                    for _, mode_group in ip.pin_modes.items():
                        for _, mode in mode_group.items():
                            self.assertGreater(len(mode.values), 0, msg="load failed.")
                    # check default conditions
                    if len(ip._parameters_conditions()) > 0:
                        for name, conditions in ip._parameters_conditions().items():
                            self.assertIsNotNone(self._find_default_condition(conditions))

    def tearDown(self):
        pass
