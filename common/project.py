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
# @file        project.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-29     xqyjlj       initial version
#

import jsonschema
import yaml, os

from PyQt5.QtCore import pyqtSignal, QObject

from common.settings import VERSION
from common.database import Database


class Project(QObject):

    pinConfigChanged = pyqtSignal(list, object)
    configChanged = pyqtSignal(str, list, object)
    reloaded = pyqtSignal()

    __p_map__ = {}
    __p_path__ = ""
    __p_summary__ = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @property
    def version(self) -> str:
        return self.__p_map__.setdefault("version", VERSION)

    @property
    def vendor(self) -> str:
        return self.__p_map__.setdefault("vendor", "unknown")

    @vendor.setter
    def vendor(self, vendor: str):
        self.__p_map__["vendor"] = vendor
        self.saveTmp()

    @property
    def targetChip(self) -> str:
        return self.__p_map__.setdefault("targetChip", "unknown")

    @targetChip.setter
    def targetChip(self, targetChip: str):
        self.__p_map__["targetChip"] = targetChip
        self.saveTmp()

    @property
    def name(self) -> str:
        return self.__p_map__.setdefault("name", "unknown")

    @name.setter
    def name(self, name: str):
        self.__p_map__["name"] = name
        self.saveTmp()

    @property
    def halVersion(self) -> str:
        return self.__p_map__.setdefault("halVersion", "unknown")

    @halVersion.setter
    def halVersion(self, halVersion: str):
        self.__p_map__["halVersion"] = halVersion
        self.saveTmp()

    @property
    def path(self) -> str:
        return self.__p_path__

    @path.setter
    def path(self, path: str):
        if self.__p_path__ != path:
            self.load(path)
            self.reloaded.emit()
        self.__p_path__ = path

    @property
    def hal(self) -> str:
        return self.__p_summary__.setdefault("hal", "unknown")

    @property
    def package(self) -> str:
        return self.__p_summary__.setdefault("package", "unknown")

    @property
    def pins(self) -> str:
        return self.__p_summary__.setdefault("pins", {})

    def load(self, path: str):
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                map = yaml.load(f.read(), Loader=yaml.FullLoader)
            with open("resource/database/schema/project.yml", 'r', encoding='utf-8') as f:
                schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            try:
                jsonschema.validate(instance=map, schema=schema)
                self.__p_map__ = map
            except jsonschema.exceptions.ValidationError as exception:
                print(f"invalid yaml {path}")
                print(exception)

            self.__p_summary__ = Database.getSummary(self.vendor, self.targetChip)

        else:
            print(f"{path} is not file!")

    def dump(self):
        return yaml.dump(self.__p_map__)

    def saveTmp(self):
        if self.__p_path__ != "":
            path = f"{self.__p_path__}.tmp" if self.__p_path__.endswith(".csp") else self.__p_path__
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.dump())

    def config(self, path: str, default=None):
        map = self.__p_map__.setdefault("config", {})
        keys = path.split("/")
        for key in keys:
            if key not in map:
                return default
            map = map[key]
        return map

    def setConfig(self, path: str, value: object):
        map = self.__p_map__.setdefault("config", {})
        keys = path.split("/")
        for key in keys[:-1]:
            if key not in map:
                map[key] = {}
            map = map[key]
        if map.get(keys[-1], None) != value:
            map[keys[-1]] = value
            if len(keys) > 2:
                if keys[0] == "pin":
                    self.pinConfigChanged.emit(keys, value)
                else:
                    self.configChanged.emit(keys[0], keys, value)
            self.saveTmp()


PROJECT = Project()
