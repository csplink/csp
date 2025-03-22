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
# @file        tc_summary.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-13     xqyjlj       initial version
#

import unittest

from common import Repository, SUMMARY


class SummaryTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_getSummary(self):
        repository = Repository()
        socs = repository.repository().allSoc()
        for soc in socs:
            summary = SUMMARY.getSummary(soc.vendor, soc.name)
            self.assertGreater(len(summary.name), 0, msg="load failed.")
            self.assertGreater(len(summary.clockTree), 0, msg="load failed.")
            self.assertGreater(len(summary.vendor), 0, msg="load failed.")
            self.assertGreater(len(summary.vendorUrl.origin), 0, msg="load failed.")
            documents = summary.documents
            self.assertGreater(len(documents.datasheets), 0, msg="load failed.")
            self.assertGreater(len(documents.errata), 0, msg="load failed.")
            self.assertGreater(len(documents.references), 0, msg="load failed.")
            for _, doc in documents.datasheets.items():
                self.assertGreater(len(doc.url.origin), 0, msg="load failed.")
            for _, doc in documents.errata.items():
                self.assertGreater(len(doc.url.origin), 0, msg="load failed.")
            for _, doc in documents.references.items():
                self.assertGreater(len(doc.url.origin), 0, msg="load failed.")
            self.assertGreater(len(summary.hals), 0, msg="load failed.")
            # self.assertGreater(summary.hasPowerPad, 0, msg='load failed.')
            self.assertGreater(len(summary.illustrate.origin), 0, msg="load failed.")
            self.assertGreater(len(summary.introduction.origin), 0, msg="load failed.")
            modules = {}
            modules.update(summary.modules.peripherals)
            modules.update(summary.modules.middlewares)
            self.assertGreater(len(modules), 0, msg="load failed.")
            for _, group in modules.items():
                self.assertGreater(len(group), 0, msg="load failed.")
                for _, unit in group.items():
                    self.assertGreater(
                        len(unit.description.origin), 0, msg="load failed."
                    )
                    # self.assertGreater(len(unit.ip), 0, msg='load failed.')
            self.assertGreater(len(summary.package), 0, msg="load failed.")
            self.assertGreater(len(summary.url.origin), 0, msg="load failed.")
            builder = summary.builder
            for _, build in builder.items():
                self.assertGreater(len(build), 0, msg="load failed.")
                for _, version in build.items():
                    self.assertGreater(len(version), 0, msg="load failed.")
            linker = summary.linker
            self.assertGreater(linker.defaultHeapSize, -2, msg="load failed.")
            self.assertGreater(linker.defaultStackSize, -2, msg="load failed.")
            pins = summary.pins
            self.assertGreater(len(pins), 0, msg="load failed.")
            pinIp = None
            for _, pin in pins.items():
                # self.assertGreater(len(pin.position), 0, msg='load failed.')
                self.assertGreater(len(pin.type), 0, msg="load failed.")
                if pin.type == "I/O":
                    self.assertGreater(
                        len(pin.signals) + len(pin.modes), 0, msg="load failed."
                    )
                    if len(pin.modes) > 0:
                        if pinIp is None:
                            pinIp = pin.modes[0].split(":")[0]
                        for mode in pin.modes:
                            self.assertEqual(
                                pinIp, mode.split(":")[0], msg="load failed."
                            )

    def tearDown(self):
        pass
