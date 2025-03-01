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
from typing import Any

import jsonschema
import yaml
from PySide6.QtCore import Signal, QObject
from loguru import logger

from .ip import IP, IpType
from .package import PACKAGE
from .settings import SETTINGS
from .summary import SUMMARY
from .value_hub import VALUE_HUB


class ProjectType(QObject):
    class ConfigsType(QObject):
        changed = Signal()
        pinConfigsChanged = Signal(list, object, object)
        configsChanged = Signal(list, object, object)

        def __init__(self, data: dict, parent=None):
            super().__init__(parent=parent)
            self.__data = data

            self.pinConfigsChanged.connect(self.__on_configsChanged)
            self.configsChanged.connect(self.__on_configsChanged)

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @origin.setter
        def origin(self, origin: dict):
            self.__data = origin

        def get(self, path: str, default=None) -> Any:
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
            if (
                (
                    isinstance(value, dict)
                    or isinstance(value, str)
                    or isinstance(value, list)
                )
                and len(value) == 0
            ) or value is None:
                item.pop(keys[-1])

            if len(keys) >= 2:
                if keys[0] == "pin":
                    self.pinConfigsChanged.emit(keys, old, value)
                else:
                    self.configsChanged.emit(keys, old, value)

            self.changed.emit()

        # noinspection PyUnusedLocal
        def __on_configsChanged(self, keys: list[str], old: object, value: object):
            if len(keys) >= 3:
                keys = keys[-3:]
            else:
                keys = keys[-2:]
            VALUE_HUB.set(".".join(keys), value)

    class GenType(QObject):
        class LinkerType(QObject):
            changed = Signal()
            defaultHeapSizeChanged = Signal(int, int)
            defaultStackSizeChanged = Signal(int, int)

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
            def defaultHeapSize(self) -> int:
                return self.__data.get("defaultHeapSize", -1)

            @defaultHeapSize.setter
            def defaultHeapSize(self, size: int):
                if self.defaultHeapSize == size:
                    return
                old = self.defaultHeapSize
                self.__data["defaultHeapSize"] = size
                self.defaultHeapSizeChanged.emit(old, size)
                self.changed.emit()

            @property
            def defaultStackSize(self) -> int:
                return self.__data.get("defaultStackSize", -1)

            @defaultStackSize.setter
            def defaultStackSize(self, size: int):
                if self.defaultStackSize == size:
                    return
                old = self.defaultStackSize
                self.__data["defaultStackSize"] = size
                self.defaultStackSizeChanged.emit(old, size)
                self.changed.emit()

        changed = Signal()
        builderChanged = Signal(str, str)
        copyLibraryChanged = Signal(bool, bool)
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
            old = self.builder
            self.__data["builder"] = builder
            self.builderChanged.emit(old, builder)
            self.changed.emit()

        @property
        def copyLibrary(self) -> bool:
            return self.__data.setdefault("copyLibrary", True)

        @copyLibrary.setter
        def copyLibrary(self, copyLibrary: bool):
            if self.copyLibrary == copyLibrary:
                return
            old = self.copyLibrary
            self.__data["copyLibrary"] = copyLibrary
            self.copyLibraryChanged.emit(old, copyLibrary)
            self.changed.emit()

        @property
        def useToolchainsPackage(self) -> bool:
            return self.__data.setdefault("useToolchainsPackage", False)

        @useToolchainsPackage.setter
        def useToolchainsPackage(self, useToolchainsPackage: bool):
            if self.useToolchainsPackage == useToolchainsPackage:
                return
            old = self.useToolchainsPackage
            self.__data["useToolchainsPackage"] = useToolchainsPackage
            self.useToolchainsPackageChanged.emit(old, useToolchainsPackage)
            self.changed.emit()

        @property
        def toolchains(self) -> str:
            return self.__data.get("toolchains", "")

        @toolchains.setter
        def toolchains(self, toolchains: str):
            if self.toolchains == toolchains:
                return
            old = self.toolchains
            self.__data["toolchains"] = toolchains
            self.toolchainsChanged.emit(old, toolchains)
            self.changed.emit()

        @property
        def builderVersion(self) -> str:
            return self.__data.get("builderVersion", "")

        @builderVersion.setter
        def builderVersion(self, version: str):
            if self.builderVersion == version:
                return
            old = self.builderVersion
            self.__data["builderVersion"] = version
            self.builderVersionChanged.emit(old, version)
            self.changed.emit()

        @property
        def toolchainsVersion(self) -> str:
            return self.__data.get("toolchainsVersion", "")

        @toolchainsVersion.setter
        def toolchainsVersion(self, version: str):
            if self.toolchainsVersion == version:
                return
            old = self.toolchainsVersion
            self.__data["toolchainsVersion"] = version
            self.toolchainsVersionChanged.emit(old, version)
            self.changed.emit()

        @property
        def hal(self) -> str:
            return self.__data.get("hal", "")

        @hal.setter
        def hal(self, hal: str):
            if self.hal == hal:
                return
            old = self.hal
            self.__data["hal"] = hal
            self.halChanged.emit(old, hal)
            self.changed.emit()

        @property
        def halVersion(self) -> str:
            return self.__data.get("halVersion", "")

        @halVersion.setter
        def halVersion(self, version: str):
            if self.halVersion == version:
                return
            old = self.halVersion
            self.__data["halVersion"] = version
            self.halVersionChanged.emit(old, version)
            self.changed.emit()

        @property
        def linker(self) -> LinkerType:
            return self.__linker

    changed = Signal()
    nameChanged = Signal(str, str)
    targetChipChanged = Signal(str, str)
    vendorChanged = Signal(str, str)
    versionChanged = Signal(str, str)
    modulesChanged = Signal(list, list)

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
        old = self.name
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
        old = self.targetChip
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
        old = self.vendor
        self.__data["vendor"] = vendor
        self.vendorChanged.emit(old, vendor)
        self.changed.emit()

    @property
    def version(self) -> str:
        return self.__data.setdefault("version", SETTINGS.VERSION)

    @version.setter
    def version(self, version: str):
        if self.version == version:
            return
        old = self.version
        self.__data["version"] = version
        self.versionChanged.emit(old, version)
        self.changed.emit()

    @property
    def modules(self) -> list[str]:
        return self.__data.setdefault("modules", [])

    @modules.setter
    def modules(self, modules: list[str]):
        if set(self.modules) == set(modules):
            return
        old = self.modules
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
            if (
                name in SUMMARY.projectSummary().moduleList()
                and cfg is not None
                and len(cfg) > 0
            ):
                ip = IP.projectIps().get(name)
                if ip and ip.activated:
                    modules.add(name)
        self.modules = sorted(modules)


class Project(QObject):
    reloaded = Signal()
    titleChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__path = ""
        self.__valid = False
        self.__project = ProjectType({}, self)
        self.__project.changed.connect(self.__on_project_changed)
        self.__isChanged = False

    @logger.catch(default=False)
    def __checkProject(self, project: dict) -> bool:
        with open(
            os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "project.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=project, schema=schema)
        return True

    @logger.catch(default={})
    def __getProject(self, file: str) -> dict:
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
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
        path = os.path.abspath(path)
        if self.__path != path:
            self.load(path)
            self.reloaded.emit()
            self.__path = path

    def new(self, path: str, name: str, targetChip: str, vendor: str):
        self.__path = os.path.abspath(os.path.join(path, name, f"{name}.csp"))
        p = os.path.dirname(self.__path)
        if not os.path.isdir(p):
            os.makedirs(p)

        project = self.project()
        project.name = name
        project.targetChip = targetChip
        project.vendor = vendor
        project.version = SETTINGS.VERSION

        self.save()
        self.load(self.__path)

    def folder(self) -> str:
        return os.path.dirname(self.__path)

    def halFolder(self) -> str:
        return PACKAGE.index().path(
            "hal", self.__project.gen.hal, self.__project.gen.halVersion
        )

    def toolchainsFolder(self) -> str:
        return PACKAGE.index().path(
            "toolchains",
            self.__project.gen.toolchains,
            self.__project.gen.toolchainsVersion,
        )

    def __buildValuesHub(self, nestedDict: dict, parentKey: str = "", sep: str = "."):
        flattened = {}
        ignore = ["configs"]
        for key, value in nestedDict.items():
            if isinstance(value, dict):
                if key in ignore:
                    new_key = parentKey
                else:
                    new_key = f"{parentKey}{sep}{key}" if parentKey else key
                flattened.update(self.__buildValuesHub(value, new_key, sep))
            else:
                new_key = (
                    f"{parentKey}{sep}{key}" if parentKey else f"project{sep}{key}"
                )
                flattened[new_key] = value
        return flattened

    def load(self, path: str) -> bool:
        self.__valid = False
        # noinspection PyTypeChecker,PyArgumentList
        self.__project.origin = self.__getProject(path)

        if len(self.__project.origin) == 0:
            logger.error(f'project "{path}" load failed.')
            return self.__valid

        summary = SUMMARY.setProjectSummary(
            self.__project.vendor, self.__project.targetChip
        )
        if len(summary.origin) == 0:
            logger.error(
                f"invalid summary {self.__project.vendor}, {self.__project.targetChip}!"
            )
            return self.__valid

        modules = {}
        modules.update(summary.modules.peripherals)
        modules.update(summary.modules.middlewares)
        for _, group in modules.items():
            for name, module in group.items():
                if module.ip != "":
                    ip = IP.setProjectIp(self.__project.vendor, name, module.ip)
                    if len(ip.origin) == 0:
                        logger.error(
                            f"invalid ip {self.__project.vendor}, {self.__project.targetChip}, {name} {module.ip}!"
                        )
                        return self.__valid

        # init
        valueHub = self.__buildValuesHub(self.__project.origin)
        for k, v in SUMMARY.projectSummary().origin.items():
            if not isinstance(v, dict):
                valueHub[f"summary.{k}"] = v
        VALUE_HUB.assign(valueHub)

        self.__valid = True
        return self.__valid

    def project(self) -> ProjectType:
        return self.__project

    def dump(self):
        return yaml.dump(self.__project.origin)

    def isGenerateSettingValid(self) -> tuple[bool, str]:
        if self.project().gen.useToolchainsPackage and not os.path.isdir(
            self.toolchainsFolder()
        ):
            return (
                False,
                f"the toolchains folder does not exist! maybe the toolchains '{self.project().gen.toolchains}:{self.project().gen.toolchainsVersion}' is not installed yet",
            )
        elif not os.path.isdir(self.halFolder()):
            return (
                False,
                f"the hal folder does not exist! maybe the hal '{self.project().gen.hal}:{self.project().gen.halVersion}' is not installed yet",
            )
        elif self.project().gen.builder == "":
            return False, "the builder is not set"
        elif self.project().gen.builderVersion == "":
            return (
                False,
                f"the builder {self.project().gen.builder!r} version is not set",
            )

        return True, ""

    def save(self):
        if self.__path != "":
            with open(self.__path, "w", encoding="utf-8") as f:
                f.write(self.dump())
            VALUE_HUB.save(self.folder())
            self.__isChanged = False
            self.titleChanged.emit(self.title())

    def title(self):
        if self.__isChanged:
            return self.__project.name + "*"
        else:
            return self.__project.name

    def isChanged(self) -> bool:
        return self.__isChanged

    def __on_project_changed(self):
        self.__isChanged = True
        self.titleChanged.emit(self.title())

    def pinIp(self) -> IpType | None:
        pinInstance = SUMMARY.projectSummary().pinInstance()
        ips = IP.projectIps()
        if pinInstance in ips:
            return ips[pinInstance]
        else:
            logger.error(f"invalid pin instance: {pinInstance}!")
            return None


PROJECT = Project()
