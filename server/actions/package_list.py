#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        package_list.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-30     xqyjlj       initial version
#

import copy
import json

from packages.package import Package


def action_package_list(dump: str = "") -> dict[str, dict[str, dict[str, str]]] | None:
    package_index = Package().index()
    index = copy.deepcopy(package_index.origin)
    for kind, package in index.items():
        for name, info in package.items():
            for version, _ in info.items():
                info[version] = package_index.path(kind, name, version)

    if dump == "json":
        print(json.dumps(index, indent=2, ensure_ascii=False))
    elif dump == "std":
        for kind, package in index.items():
            print(f"{kind}:")
            for name, info in package.items():
                print(f"  {name}:")
                for version, _ in info.items():
                    print(f"    {version}: {package_index.path(kind, name, version)}")
    else:
        return index
