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
# @file        linker.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#


import json


class Linker:
    def __init__(self, data: dict):
        self._data = data

    def __str__(self) -> str:
        return json.dumps(self._data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self._data

    @property
    def heapSize(self) -> int:
        return self._data.get("heapSize", -1)

    @property
    def stackSize(self) -> int:
        return self._data.get("stackSize", -1)
