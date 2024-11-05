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

import json
import os

import jsonschema
import yaml
from PySide6.QtCore import Signal, QObject
from loguru import logger

from utils import converters
from .ip import IP
from .package import PACKAGE
from .settings import SETTINGS
from .summary import SUMMARY


class Project(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__data = {}
        self.__path = ""
        self.__valid = False

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def version(self) -> str:
        return self.__data.setdefault("version", SETTINGS.VERSION)

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

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

    @property
    def modules(self) -> list:
        return self.__data.setdefault("modules", [])

    # gen --------------------------------------------------------------------------------------------------------------
    # gen/copyHalLibrary ----------------------------------------------------------
    copyHalLibraryChanged = Signal(bool)

    @property
    def copyHalLibrary(self) -> bool:
        return self.__data.get("gen", {}).get("copyHalLibrary", True)

    @copyHalLibrary.setter
    def copyHalLibrary(self, is_copy_library: bool):
        if self.copyHalLibrary == is_copy_library:
            return
        self.__data.setdefault("gen", {})["copyHalLibrary"] = is_copy_library
        self.copyHalLibraryChanged.emit(is_copy_library)
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

    # gen/useToolchainsPackage -------------------------------------------------
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

    # gen/toolchains -----------------------------------------------------------
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

    # gen/builder --------------------------------------------------------------
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

    # gen/builderVersion -------------------------------------------------------
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

    # gen/toolchainsVersion ----------------------------------------------------
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

    # gen/hal ------------------------------------------------------------------
    halChanged = Signal(str)

    @property
    def hal(self) -> str:
        return self.__data.get("gen", {}).get("hal", "")

    @hal.setter
    def hal(self, hal: str):
        if self.hal == hal:
            return
        self.__data.setdefault("gen", {})["hal"] = hal
        self.halChanged.emit(hal)
        self.saveTmp()

    # gen/halVersion -----------------------------------------------------------
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

    # ------------------------------------------------------------------------------------------------------------------

    @property
    def valid(self) -> bool:
        return self.__valid

    # ------------------------------------------------------------------------------------------------------------------
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

    def folder(self) -> str:
        return os.path.dirname(self.__path)

    def halFolder(self) -> str:
        return PACKAGE.index().path("hal", self.hal, self.halVersion)

    def toolchainsFolder(self) -> str:
        return PACKAGE.index().path("toolchains", self.toolchains, self.toolchainsVersion)

    def load(self, path: str) -> bool:
        self.__valid = False

        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = yaml.load(f.read(), Loader=yaml.FullLoader)
            with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "project.yml"), 'r', encoding='utf-8') as f:
                schema = yaml.load(f.read(), Loader=yaml.FullLoader)

            try:
                jsonschema.validate(instance=data, schema=schema)
                self.__data = data
            except jsonschema.exceptions.ValidationError as exception:
                print(f"invalid yaml {path}")
                print(exception)
                return self.__valid

            summary = SUMMARY.setProjectSummary(self.vendor, self.targetChip)
            if len(summary.origin) == 0:
                logger.error(f"invalid summary {self.vendor}, {self.targetChip}!")
                return self.__valid

            for _, group in summary.modules.items():
                for name, module in group.items():
                    if module.ip != '':
                        ip = IP.setProjectIp(self.vendor, name, module.ip)
                        if len(ip.origin) == 0:
                            logger.error(f"invalid ip {self.vendor}, {self.targetChip}, {name} {module.ip}!")
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
        item = self.__data.get("config", {})
        keys = path.split("/")
        for key in keys:
            if key not in item:
                return default
            item = item[key]
        return item

    def setConfig(self, path: str, value: object):
        item = self.__data.setdefault("config", {})
        keys = path.split("/")
        for key in keys[:-1]:
            if key not in item:
                item[key] = {}
            item = item[key]
        if item.get(keys[-1], None) != value:
            old = item.get(keys[-1], None)
            item[keys[-1]] = value

            # remove node
            if ((isinstance(value, dict) or isinstance(value, str) or isinstance(value, list))
                and len(value) == 0) or value is None:
                item.pop(keys[-1])

            if len(keys) >= 2:
                if keys[0] == "pin":
                    self.pinConfigChanged.emit(keys, old, value)
                else:
                    self.configChanged.emit(keys, old, value)

            modules = set()
            # noinspection PyUnresolvedReferences
            for name, cfg in self.__data["config"].items():
                if name in SUMMARY.projectSummary().moduleList() and cfg is not None and len(cfg) > 0:
                    modules.add(name)
            if set(self.modules) != modules:
                self.__data["modules"] = list(modules)
                self.modulesChanged.emit()

            self.saveTmp()

    def isGenerateSettingValid(self) -> bool:
        if not os.path.isdir(self.toolchainsFolder()):
            return False
        elif not os.path.isdir(self.halFolder()):
            return False
        elif self.builder == "":
            return False
        elif self.builderVersion == "":
            return False

        if (not converters.ishex(self.defaultHeapSize)) and converters.ishex(
                SUMMARY.projectSummary().linker.defaultHeapSize):
            return False
        elif not converters.ishex(self.defaultStackSize) and converters.ishex(
                SUMMARY.projectSummary().linker.defaultStackSize):
            return False

        return True


PROJECT = Project()
