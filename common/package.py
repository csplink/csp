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
# @file        package.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-28     xqyjlj       initial version
#

from .database import Database


class Package():
    m_data = {}

    def __init__(self) -> None:
        self.m_data = Database.getPackageIndex()

    @property
    def hal(self) -> dict:
        return self.m_data.get("hal", {})

    def path(self, type: str, name: str, version: str):
        return self.m_data.get(type, {}).get(name, {}).get(version, "")

    @property
    def origin(self) -> dict:
        return self.m_data


PACKAGE = Package()
