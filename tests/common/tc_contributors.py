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
# @file        tc_contributors.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-14     xqyjlj       initial version
#

import unittest

from common import Contributor


class ContributorTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_getContributor(self):
        contributors = Contributor().getContributors()
        for contributor in contributors:
            self.assertGreater(len(contributor.name), 0, msg='load failed.')
            self.assertGreater(len(contributor.htmlUrl), 0, msg='load failed.')
            self.assertGreater(contributor.contributions, 0, msg='load failed.')
            self.assertGreater(len(contributor.avatar), 0, msg='load failed.')

    def tearDown(self):
        pass
