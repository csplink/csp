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

from PySide6.QtCore import Signal, QObject

from .settings import SETTINGS
from .database import DATABASE
from .package import PACKAGE


class Summary(QObject):

    __summary = {}
    __modulesList = []

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @property
    def hal(self) -> str:
        return self.__summary.get("hal", "unknown")

    @property
    def package(self) -> str:
        return self.__summary.get("package", "unknown")

    @property
    def pins(self) -> dict:
        return self.__summary.get("pins", {})

    @property
    def modules(self) -> dict:
        return self.__summary.get("modules", {})

    @property
    def pinIp(self) -> dict:
        return self.__summary.get("pinIp", "")

    @property
    def builder(self) -> dict[str, dict[str, list[str]]]:
        return self.__summary.get("builder", {})

    @property
    def linker(self) -> dict:
        return self.__summary.get("linker", {})

    @property
    def defaultHeapSize(self) -> str:
        return self.linker.get("defaultHeapSize", "")

    @property
    def defaultStackSize(self) -> str:
        return self.linker.get("defaultStackSize", "")

    @property
    def modulesList(self) -> list:
        return self.__modulesList

    @property
    def origin(self) -> dict:
        return self.__summary

    @origin.setter
    def origin(self, summary: dict):
        self.__summary = summary

        for _, moduleGroup in self.modules.items():
            for name, _ in moduleGroup.items():
                self.__modulesList.append(name)


class Ip(QObject):

    __ip = {}
    __ipTotal = {}
    __ipReverseTotal = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def ip(self, name: str) -> dict:
        if name not in self.__ip:
            return {}
        return self.__ip[name]

    def iptr(self, name: str) -> str:
        if name in self.__ipTotal:
            return self.__ipTotal[name]
        else:
            return name

    def iptr2(self, name: str) -> str:
        if name in self.__ipReverseTotal:
            return self.__ipReverseTotal[name]
        else:
            return name

    @property
    def origin(self) -> dict:
        return self.__ip

    @origin.setter
    def origin(self, ip: dict):
        self.__ip = ip

        locale = SETTINGS.get(SETTINGS.language).value.name()
        for name in ip.keys():
            for _, parameter in ip[name]["parameters"].items():
                for key, value in parameter["values"].items():
                    self.__ipTotal[key] = value["comment"][locale]
                    self.__ipReverseTotal[value["comment"][locale]] = key


class Project(QObject):
    __data = {}
    __path = ""
    __summary = None
    __ip = None
    __valid = False

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__summary = Summary(self)
        self.__ip = Ip(self)

    @property
    def version(self) -> str:
        return self.__data.setdefault("version", VERSION)

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def summary(self) -> Summary:
        return self.__summary

    @property
    def ip(self) -> Summary:
        return self.__ip

    @property
    def valid(self) -> bool:
        return self.__valid

    @vendor.setter
    def vendor(self, vendor: str):
        self.__data["vendor"] = vendor
        self.saveTmp()

    @property
    def targetChip(self) -> str:
        return self.__data.get("targetChip", "")

    @targetChip.setter
    def targetChip(self, chip: str):
        self.__data["targetChip"] = chip
        self.saveTmp()

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @name.setter
    def name(self, name: str):
        self.__data["name"] = name
        self.saveTmp()

    # gen --------------------------------------------------------------------------------------------------------------
    # gen/copyLibrary ----------------------------------------------------------
    copyLibraryChanged = Signal(bool)

    @property
    def copyLibrary(self) -> bool:
        return self.__data.get("gen", {}).get("copyLibrary", True)

    @copyLibrary.setter
    def copyLibrary(self, is_copy_library: bool):
        if self.copyLibrary == is_copy_library:
            return
        self.__data.setdefault("gen", {})["copyLibrary"] = is_copy_library
        self.copyLibraryChanged.emit(is_copy_library)
        self.saveTmp()

    # gen/defaultHeapSize ------------------------------------------------------

    defaultHeapSizeChanged = Signal(str)

    @property
    def defaultHeapSize(self) -> str:
        return self.__data.get("gen", {}).get("linker", {}).get("defaultHeapSize", "")

    @defaultHeapSize.setter
    def defaultHeapSize(self, size: str):
        if self.defaultHeapSize == size:
            return
        self.__data.setdefault("gen", {}).setdefault("linker", {})["defaultHeapSize"] = size
        self.defaultHeapSizeChanged.emit(size)
        self.saveTmp()

    # gen/defaultStackSize -----------------------------------------------------

    defaultStackSizeChanged = Signal(str)

    @property
    def defaultStackSize(self) -> str:
        return self.__data.get("gen", {}).get("linker", {}).get("defaultStackSize", "")

    @defaultStackSize.setter
    def defaultStackSize(self, size: str):
        if self.defaultStackSize == size:
            return
        self.__data.setdefault("gen", {}).setdefault("linker", {})["defaultStackSize"] = size
        self.defaultStackSizeChanged.emit(size)
        self.saveTmp()

    # gen/useToolchainsPackage
    useToolchainsPackageChanged = Signal(bool)

    @property
    def useToolchainsPackage(self) -> bool:
        return self.__data.get("gen", {}).get("useToolchainsPackage", False)

    @useToolchainsPackage.setter
    def useToolchainsPackage(self, is_use_toolchains_package: bool):
        if self.useToolchainsPackage == is_use_toolchains_package:
            return
        self.__data.setdefault("gen", {})["useToolchainsPackage"] = is_use_toolchains_package
        self.useToolchainsPackageChanged.emit(is_use_toolchains_package)
        self.saveTmp()

    # gen/toolchains
    toolchainsChanged = Signal(str)

    @property
    def toolchains(self) -> str:
        return self.__data.get("gen", {}).get("toolchains", "")

    @toolchains.setter
    def toolchains(self, toolchains: str):
        if self.toolchains == toolchains:
            return
        self.__data.setdefault("gen", {})["toolchains"] = toolchains
        self.toolchainsChanged.emit(toolchains)
        self.saveTmp()

    # gen/builder
    builderChanged = Signal(str)

    @property
    def builder(self) -> str:
        return self.__data.get("gen", {}).get("builder", "")

    @builder.setter
    def builder(self, builder: str):
        if self.builder == builder:
            return
        self.__data.setdefault("gen", {})["builder"] = builder
        self.builderChanged.emit(builder)
        self.saveTmp()

    # gen/builderVersion
    builderVersionChanged = Signal(str)

    @property
    def builderVersion(self) -> str:
        return self.__data.get("gen", {}).get("builderVersion", "")

    @builderVersion.setter
    def builderVersion(self, version: str):
        if self.builderVersion == version:
            return
        self.__data.setdefault("gen", {})["builderVersion"] = version
        self.builderVersionChanged.emit(version)
        self.saveTmp()

    # gen/toolchainsVersion
    toolchainsVersionChanged = Signal(str)

    @property
    def toolchainsVersion(self) -> str:
        return self.__data.get("gen", {}).get("toolchainsVersion", "")

    @toolchainsVersion.setter
    def toolchainsVersion(self, version: str):
        if self.toolchainsVersion == version:
            return
        self.__data.setdefault("gen", {})["toolchainsVersion"] = version
        self.toolchainsVersionChanged.emit(version)
        self.saveTmp()

    # gen/halVersion
    halVersionChanged = Signal(str)

    @property
    def halVersion(self) -> str:
        return self.__data.get("gen", {}).get("halVersion", "")

    @halVersion.setter
    def halVersion(self, version: str):
        if self.halVersion == version:
            return
        self.__data.setdefault("gen", {})["halVersion"] = version
        self.halVersionChanged.emit(version)
        self.saveTmp()

    reloaded = Signal()

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, path: str):
        if self.__path != path:
            self.load(path)
            self.reloaded.emit()
        self.__path = path

    @property
    def dir(self) -> str:
        return os.path.dirname(self.__path)

    @property
    def modules(self) -> list:
        return self.__data.setdefault("modules", [])

    @property
    def halDir(self) -> str:
        return PACKAGE.path("hal", self.__summary.hal, self.halVersion)

    @property
    def toolchainsDir(self) -> str:
        return PACKAGE.path("toolchains", self.toolchains, self.toolchainsVersion)

    def load(self, path: str) -> bool:
        self.__valid = False

        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                map = yaml.load(f.read(), Loader=yaml.FullLoader)
            with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "project.yml"), 'r', encoding='utf-8') as f:
                schema = yaml.load(f.read(), Loader=yaml.FullLoader)

            try:
                jsonschema.validate(instance=map, schema=schema)
                self.__data = map
            except jsonschema.exceptions.ValidationError as exception:
                print(f"invalid yaml {path}")
                print(exception)
                return self.__valid

            try:
                self.__summary.origin = DATABASE.getSummary(self.vendor, self.targetChip)
            except jsonschema.exceptions.ValidationError as exception:
                print(f"invalid yaml {path}")
                print(exception)
                return self.__valid

            try:
                ip = {}
                for _, module_group in self.__summary.modules.items():
                    for name, module in module_group.items():
                        if "ip" in module:
                            ip[name] = DATABASE.getIp(self.vendor, module["ip"])
                self.__ip.origin = ip
            except jsonschema.exceptions.ValidationError as exception:
                print(f"invalid yaml {path}")
                print(exception)
                return self.__valid

            self.__valid = True

            return self.__valid

        else:
            print(f"{path} is not file!")
            return self.__valid

    def dump(self):
        return yaml.dump(self.__data)

    def saveTmp(self):
        if self.__path != "":
            path = f"{self.__path}.tmp" if self.__path.endswith(".csp") else self.__path
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.dump())

    pinConfigChanged = Signal(list, object, object)
    configChanged = Signal(list, object, object)
    modulesChanged = Signal()

    def config(self, path: str, default=None):
        map = self.__data.get("config", {})
        keys = path.split("/")
        for key in keys:
            if key not in map:
                return default
            map = map[key]
        return map

    def setConfig(self, path: str, value: object):
        map = self.__data.setdefault("config", {})
        keys = path.split("/")
        for key in keys[:-1]:
            if key not in map:
                map[key] = {}
            map = map[key]
        if map.get(keys[-1], None) != value:
            old = map.get(keys[-1], None)
            map[keys[-1]] = value

            if ((isinstance(value, dict) or isinstance(value, str) or isinstance(value, list))
                    and len(value) == 0) or value == None:
                map.pop(keys[-1])

            if len(keys) >= 2:
                if keys[0] == "pin":
                    self.pinConfigChanged.emit(keys, old, value)
                else:
                    self.configChanged.emit(keys, old, value)

            modules = set()
            for name, cfg in self.__data["config"].items():
                if name in self.__summary.modulesList and cfg != None and len(cfg) > 0:
                    modules.add(name)
            if set(self.modules) != modules:
                self.__data["modules"] = list(modules)
                self.modulesChanged.emit()

            self.saveTmp()


PROJECT = Project()
