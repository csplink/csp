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
# @file        project.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#

import json
from pathlib import Path

from .configs import Configs
from .gen import Gen


class Project:
    def __init__(self, data: dict, user_data: dict = {}):
        self._data = data
        self._gen = Gen(self._data.get("gen", {}))
        self._configs = Configs(self._data.get("configs", {}))
        self._user_data = user_data

    def __str__(self) -> str:
        return json.dumps(self._data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self._data

    @property
    def name(self) -> str:
        return self._data["name"]

    @property
    def targetChip(self) -> str:
        return self._data["targetChip"]

    @property
    def vendor(self) -> str:
        return self._data["vendor"]

    @property
    def version(self) -> str:
        return self._data["version"]

    @property
    def modules(self) -> list[str]:
        return self._data.get("modules", [])

    @property
    def gen(self) -> Gen:
        return self._gen

    @property
    def configs(self) -> Configs:
        return self._configs

    def hal_folder(self) -> str:
        return self._user_data.get("hal_folder", "")

    def toolchains_folder(self) -> str:
        return self._user_data.get("toolchains_folder", "")

    def path(self) -> str:
        return self._user_data.get("path", "")

    def folder(self) -> str:
        return str(Path(self.path()).parent)
