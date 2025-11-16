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
# @file        index.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-29     xqyjlj       initial version
#

import json
from pathlib import Path

from utils.sys import SysUtils


class PackageIndex:
    def __init__(self, data: dict):
        self.__data = data

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict[str, dict[str, dict[str, str]]]:
        return self.__data

    def types(self) -> list[str]:
        return list(self.__data.keys())

    def items(self, kind: str) -> list[str]:
        return list(self.__data.get(kind, {}).keys())

    def versions(self, kind: str, name: str) -> list[str]:
        return list(self.__data.get(kind, {}).get(name, {}).keys())

    def path(self, kind: str, name: str, version: str) -> str:
        path = self.__data.get(kind, {}).get(name, {}).get(version, "")
        if not path:
            return path
        path = Path(path)
        if path.is_absolute():
            return str(path).replace("\\", "/")
        path = str((SysUtils.packages_folder() / path).resolve())
        return path.replace("\\", "/")
