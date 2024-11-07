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


class ProjectType(QObject):
    class ConfigsType(QObject):
        changed = Signal()
        pinConfigsChanged = Signal(list, object, object)
        configsChanged = Signal(list, object, object)

        def __init__(self, data: dict, parent=None):
            super().__init__(parent=parent)
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @origin.setter
        def origin(self, origin: dict):
            self.__data = origin

        def get(self, path: str, default=None):
            item = self.__data
            keys = path.split("/")
            for key in keys:
                if key not in item:
                    return default
                item = item[key]
            return item

        def set(self, path: str, value: object):
            item = self.__data
            keys = path.split("/")
            for key in keys[:-1]:
                if key not in item:
                    item[key] = {}
                item = item[key]
            if item.get(keys[-1], None) == value:
                return

            old = item.get(keys[-1], None)
            item[keys[-1]] = value

            # remove node
            if ((isinstance(value, dict) or isinstance(value, str) or isinstance(value, list))
                and len(value) == 0) or value is None:
                item.pop(keys[-1])

            if len(keys) >= 2:
                if keys[0] == "pin":
                    self.pinConfigsChanged.emit(keys, old, value)
                else:
                    self.configsChanged.emit(keys, old, value)

            self.changed.emit()

    class GenType(QObject):
        class LinkerType(QObject):
            changed = Signal()
            defaultHeapSizeChanged = Signal(str, str)
            defaultStackSizeChanged = Signal(str, str)

            def __init__(self, data: dict, parent=None):
                super().__init__(parent=parent)
                self.__data = data

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @origin.setter
            def origin(self, origin: dict):
                self.__data = origin

            @property
            def defaultHeapSize(self) -> str:
                return self.__data.get("defaultHeapSize", "")

            @defaultHeapSize.setter
            def defaultHeapSize(self, size: str):
                if self.defaultHeapSize == size:
                    return
                old = self.__data["defaultHeapSize"]
                self.__data["defaultHeapSize"] = size
                self.defaultHeapSizeChanged.emit(old, size)
                self.changed.emit()

            @property
            def defaultStackSize(self) -> str:
                return self.__data.get("defaultStackSize", "")

            @defaultStackSize.setter
            def defaultStackSize(self, size: str):
                if self.defaultStackSize == size:
                    return
                old = self.__data["defaultStackSize"]
                self.__data["defaultStackSize"] = size
                self.defaultStackSizeChanged.emit(old, size)
                self.changed.emit()

        changed = Signal()
        builderChanged = Signal(str, str)
        copyHalLibraryChanged = Signal(bool, bool)
        useToolchainsPackageChanged = Signal(bool, bool)
        toolchainsChanged = Signal(str, str)
        builderVersionChanged = Signal(str, str)
        toolchainsVersionChanged = Signal(str, str)
        halChanged = Signal(str, str)
        halVersionChanged = Signal(str, str)

        def __init__(self, data: dict, parent=None):
            super().__init__(parent=parent)
            self.__data = data
            self.__linker = self.LinkerType(self.__data.setdefault("linker", {}), self)
            self.__linker.changed.connect(self.changed)

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @origin.setter
        def origin(self, origin: dict):
            self.__data = origin
            self.__linker.origin = self.__data.setdefault("linker", {})

        @property
        def builder(self) -> str:
            return self.__data.get("builder", "")

        @builder.setter
        def builder(self, builder: str):
            if self.builder == builder:
                return
            old = self.__data["builder"]
            self.__data["builder"] = builder
            self.builderChanged.emit(old, builder)

        @property
        def copyHalLibrary(self) -> bool:
            return self.__data.get("copyHalLibrary", True)

        @copyHalLibrary.setter
        def copyHalLibrary(self, copyHalLibrary: bool):
            if self.copyHalLibrary == copyHalLibrary:
                return
            old = self.__data["copyHalLibrary"]
            self.__data["copyHalLibrary"] = copyHalLibrary
            self.copyHalLibraryChanged.emit(old, copyHalLibrary)

        @property
        def useToolchainsPackage(self) -> bool:
            return self.__data.get("useToolchainsPackage", False)

        @useToolchainsPackage.setter
        def useToolchainsPackage(self, useToolchainsPackage: bool):
            if self.useToolchainsPackage == useToolchainsPackage:
                return
            old = self.__data["useToolchainsPackage"]
            self.__data["useToolchainsPackage"] = useToolchainsPackage
            self.useToolchainsPackageChanged.emit(old, useToolchainsPackage)

        @property
        def toolchains(self) -> str:
            return self.__data.get("toolchains", "")

        @toolchains.setter
        def toolchains(self, toolchains: str):
            if self.toolchains == toolchains:
                return
            old = self.__data["toolchains"]
            self.__data["toolchains"] = toolchains
            self.toolchainsChanged.emit(old, toolchains)

        @property
        def builderVersion(self) -> str:
            return self.__data.get("builderVersion", "")

        @builderVersion.setter
        def builderVersion(self, version: str):
            if self.builderVersion == version:
                return
            old = self.__data["builderVersion"]
            self.__data["builderVersion"] = version
            self.builderVersionChanged.emit(old, version)

        @property
        def toolchainsVersion(self) -> str:
            return self.__data.get("toolchainsVersion", "")

        @toolchainsVersion.setter
        def toolchainsVersion(self, version: str):
            if self.toolchainsVersion == version:
                return
            old = self.__data["toolchainsVersion"]
            self.__data["toolchainsVersion"] = version
            self.toolchainsVersionChanged.emit(old, version)

        @property
        def hal(self) -> str:
            return self.__data.get("hal", "")

        @hal.setter
        def hal(self, hal: str):
            if self.hal == hal:
                return
            old = self.__data["hal"]
            self.__data["hal"] = hal
            self.halChanged.emit(old, hal)

        @property
        def halVersion(self) -> str:
            return self.__data.get("halVersion", "")

        @halVersion.setter
        def halVersion(self, version: str):
            if self.halVersion == version:
                return
            old = self.__data["halVersion"]
            self.__data["halVersion"] = version
            self.halVersionChanged.emit(old, version)

        @property
        def linker(self) -> LinkerType:
            return self.__linker

    changed = Signal()
    nameChanged = Signal(str, str)
    targetChipChanged = Signal(str, str)
    vendorChanged = Signal(str, str)
    modulesChanged = Signal(str, str)

    def __init__(self, data: dict, parent=None):
        super().__init__(parent=parent)
        self.__data = data
        self.__gen = self.GenType(self.__data.setdefault("gen", {}), self)
        self.__configs = self.ConfigsType(self.__data.setdefault("configs", {}), self)
        self.__gen.changed.connect(self.changed)
        self.__configs.changed.connect(self.changed)
        self.__configs.changed.connect(self.__on_configs_changed)

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @origin.setter
    def origin(self, origin: dict):
        self.__data = origin
        self.__gen.origin = self.__data.setdefault("gen", {})
        self.__configs.origin = self.__data.setdefault("configs", {})

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @name.setter
    def name(self, name: str):
        if self.name == name:
            return
        old = self.__data["name"]
        self.__data["name"] = name
        self.nameChanged.emit(old, name)
        self.changed.emit()

    @property
    def targetChip(self) -> str:
        return self.__data.get("targetChip", "")

    @targetChip.setter
    def targetChip(self, targetChip: str):
        if self.targetChip == targetChip:
            return
        old = self.__data["targetChip"]
        self.__data["targetChip"] = targetChip
        self.targetChipChanged.emit(old, targetChip)
        self.changed.emit()

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

    @vendor.setter
    def vendor(self, vendor: str):
        if self.vendor == vendor:
            return
        old = self.__data["vendor"]
        self.__data["vendor"] = vendor
        self.vendorChanged.emit(old, vendor)
        self.changed.emit()

    @property
    def version(self) -> str:
        return self.__data.setdefault("version", SETTINGS.VERSION)

    @property
    def modules(self) -> list:
        return self.__data.setdefault("modules", [])

    @modules.setter
    def modules(self, modules: list):
        if set(self.__data["modules"]) == set(modules):
            return
        old = self.__data["modules"]
        self.__data["modules"] = modules
        self.modulesChanged.emit(old, modules)
        self.changed.emit()

    @property
    def gen(self) -> GenType:
        return self.__gen

    @property
    def configs(self) -> ConfigsType:
        return self.__configs

    def __on_configs_changed(self):
        modules = set()
        # noinspection PyUnresolvedReferences
        for name, cfg in self.configs.origin.items():
            if name in SUMMARY.projectSummary().moduleList() and cfg is not None and len(cfg) > 0:
                modules.add(name)
        self.modules = modules


class Project(QObject):
    reloaded = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__path = ''
        self.__valid = False
        self.__project = ProjectType({}, self)
        self.__project.changed.connect(self.__saveTmp)

    @logger.catch(default=False)
    def __checkProject(self, project: dict) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "project.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=project, schema=schema)
        return True

    @logger.catch(default={})
    def __getProject(self, file: str) -> dict:
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as f:
                project = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkProject(project)
            if succeed:
                return project
            else:
                return {}
        else:
            logger.error(f"{file} is not file!")
            return {}

    def valid(self) -> bool:
        return self.__valid

    def path(self) -> str:
        return self.__path

    def setPath(self, path: str):
        if self.__path != path:
            self.load(path)
            self.reloaded.emit()
        self.__path = path

    def folder(self) -> str:
        return os.path.dirname(self.__path)

    def halFolder(self) -> str:
        return PACKAGE.index().path("hal", self.__project.gen.hal, self.__project.gen.halVersion)

    def toolchainsFolder(self) -> str:
        return PACKAGE.index().path("toolchains", self.__project.gen.toolchains, self.__project.gen.toolchainsVersion)

    def load(self, path: str) -> bool:
        self.__valid = False
        # noinspection PyTypeChecker,PyArgumentList
        self.__project.origin = self.__getProject(path)

        if len(self.__project.origin) == 0:
            logger.error(f'project "{path}" load failed.')
            return self.__valid

        summary = SUMMARY.setProjectSummary(self.__project.vendor, self.__project.targetChip)
        if len(summary.origin) == 0:
            logger.error(f"invalid summary {self.__project.vendor}, {self.__project.targetChip}!")
            return self.__valid

        for _, group in summary.modules.items():
            for name, module in group.items():
                if module.ip != '':
                    ip = IP.setProjectIp(self.__project.vendor, name, module.ip)
                    if len(ip.origin) == 0:
                        logger.error(
                            f"invalid ip {self.__project.vendor}, {self.__project.targetChip}, {name} {module.ip}!")
                        return self.__valid

        self.__valid = True
        return self.__valid

    def project(self) -> ProjectType:
        return self.__project

    def dump(self):
        return yaml.dump(self.__project.origin)

    def isGenerateSettingValid(self) -> bool:
        if not os.path.isdir(self.toolchainsFolder()):
            return False
        elif not os.path.isdir(self.halFolder()):
            return False
        elif self.__project.gen.builder == "":
            return False
        elif self.__project.gen.builderVersion == "":
            return False

        if (not converters.ishex(self.__project.gen.linker.defaultHeapSize)) and converters.ishex(
                SUMMARY.projectSummary().linker.defaultHeapSize):
            return False
        elif not converters.ishex(self.__project.gen.linker.defaultStackSize) and converters.ishex(
                SUMMARY.projectSummary().linker.defaultStackSize):
            return False

        return True

    def __saveTmp(self):
        if self.__path != "":
            path = f"{self.__path}.tmp" if self.__path.endswith(".csp") else self.__path
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.dump())


PROJECT = Project()
