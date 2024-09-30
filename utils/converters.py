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
# @file        converters.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-08-31     xqyjlj       initial version

import re
from functools import reduce


def ishex(string: str) -> bool:
    pattern = r'^0x[0-9A-Fa-f]+$'
    return bool(re.match(pattern, string))


def isurl(string: str) -> bool:
    pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    return bool(re.match(pattern, string))


def isemail(string: str) -> bool:
    pattern = r'^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\\.[a-zA-Z0-9_-]+)+$'
    return bool(re.match(pattern, string))


def paths2dict(paths: list[str], separator='/'):
    pathDict = {}
    for path in paths:
        parts = path.strip().split(separator)

        def updateDict(dt, key):
            if key not in dt:
                dt[key] = {}
            return dt[key]

        currentDict = reduce(updateDict, parts[:-1], pathDict)
        currentDict[parts[-1]] = ""
    return pathDict
