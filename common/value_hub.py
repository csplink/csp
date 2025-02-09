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
# @file        value_hub.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-11-21     xqyjlj       initial version
#

import json
import os

import yaml
from PySide6.QtCore import QObject, Signal


class ValueHub(QObject):
    changed = Signal()
    itemUpdated = Signal(list, object, object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__data = {}

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    def values(self) -> dict:
        return self.__data

    def assign(self, values: dict):
        self.__data = self.__convertToNestedDict(values)
        self.changed.emit()

    def set(self, path: str, value: object):
        item = self.__data
        keys = path.split(".")
        for key in keys[:-1]:
            if key not in item:
                item[key] = {}
            item = item[key]
        if item.get(keys[-1], None) == value:
            return

        old = item.get(keys[-1], None)
        item[keys[-1]] = value

        # remove node
        if (
            (
                isinstance(value, dict)
                or isinstance(value, str)
                or isinstance(value, list)
            )
            and len(value) == 0
        ) or value is None:
            item.pop(keys[-1])

        self.itemUpdated.emit(keys, old, value)
        self.changed.emit()

    def save(self, folder: str):
        folder = os.path.join(folder, ".csp")
        if not os.path.exists(folder):
            os.makedirs(folder)
        path = os.path.join(folder, "value_hub.yaml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(yaml.dump(self.__data))

    def __convertToNestedDict(self, data: dict[str, str]) -> dict:
        def __nestedSet(dic, keys_, value_):
            for key_ in keys_[:-1]:
                dic = dic.setdefault(key_, {})
            dic[keys_[-1]] = value_

        nested = {}

        for key, value in data.items():
            # split the key into parts by '.'
            keys = key.split(".")
            __nestedSet(nested, keys, value)
        return nested


VALUE_HUB = ValueHub()
