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
# @file        document.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-12     xqyjlj       initial version
#


import json

from .document_unit import DocumentUnit


class Documents:
    def __init__(self, data: dict):
        self.__data = data
        self.__datasheets = None
        self.__errata = None
        self.__references = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def datasheets(self) -> dict[str, DocumentUnit]:
        if self.__datasheets is None:
            self.__datasheets = {}
            datasheets = self.__data.get("datasheets", {})
            for name, unit in datasheets.items():
                self.__datasheets[name] = DocumentUnit(unit if unit is not None else {})
        return self.__datasheets

    @property
    def errata(self) -> dict[str, DocumentUnit]:
        if self.__errata is None:
            self.__errata = {}
            errata = self.__data.get("errata", {})
            for name, unit in errata.items():
                self.__errata[name] = DocumentUnit(unit if unit is not None else {})
        return self.__errata

    @property
    def references(self) -> dict[str, DocumentUnit]:
        if self.__references is None:
            self.__references = {}
            references = self.__data.get("references", {})
            for name, unit in references.items():
                self.__references[name] = DocumentUnit(unit if unit is not None else {})
        return self.__references
