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
# @file        tc_repository.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-08     xqyjlj       initial version
#

import unittest

from common import Repository


class RepositoryTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_getRepository(self):
        repository = Repository()
        repo = repository.repository()
        self.assertGreater(len(repo.origin), 0, msg="load failed.")

        types = repo.types()
        self.assertGreater(len(types), 0, msg="load failed.")
        for kind in types:
            vendors = repo.vendors(kind)
            self.assertGreater(len(vendors), 0, msg="load failed.")
            for vendor in vendors:
                series = repo.series(kind, vendor)
                self.assertGreater(len(series), 0, msg="load failed.")
                for ser in series:
                    lines = repo.lines(kind, vendor, ser)
                    self.assertGreater(len(lines), 0, msg="load failed.")
                    for line in lines:
                        names = repo.names(kind, vendor, ser, line)
                        self.assertGreater(len(names), 0, msg="load failed.")
                        for name in names:
                            if kind == "soc":
                                soc = repo.soc(kind, vendor, ser, line, name)
                                self.assertGreater(len(soc.core), 0, msg="load failed.")
                                self.assertGreater(
                                    soc.current.lowest, 0, msg="load failed."
                                )
                                self.assertGreater(
                                    soc.current.run, 0, msg="load failed."
                                )
                                self.assertGreater(soc.flash, 0, msg="load failed.")
                                self.assertGreater(soc.frequency, 0, msg="load failed.")
                                self.assertGreater(soc.io, 0, msg="load failed.")
                                self.assertGreater(
                                    len(soc.package), 0, msg="load failed."
                                )
                                self.assertGreater(
                                    len(soc.peripherals), 0, msg="load failed."
                                )
                                self.assertGreater(soc.ram, 0, msg="load failed.")
                                self.assertGreater(
                                    soc.temperature.max, 0, msg="load failed."
                                )
                                # self.assertGreater(soc.temperature.min, 0, msg='load failed.')
                                self.assertGreater(
                                    soc.voltage.max, 0, msg="load failed."
                                )
                                self.assertGreater(
                                    soc.voltage.min, 0, msg="load failed."
                                )

        self.assertGreater(len(repo.allSoc()), 0, msg="load failed.")

    def tearDown(self):
        pass
