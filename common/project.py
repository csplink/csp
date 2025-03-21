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
        pin_configs_changed = Signal(list, object, object)
        configs_changed = Signal(list, object, object)

        def __init__(self, data: dict, parent=None):
            super().__init__(parent=parent)
            self.__data = data

            self.pin_configs_changed.connect(self.__on_configs_changed)
            self.configs_changed.connect(self.__on_configs_changed)

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
                    self.pin_configs_changed.emit(keys, old, value)
                else:
                    self.configs_changed.emit(keys, old, value)

            self.changed.emit()

        # noinspection PyUnusedLocal
        def __on_configs_changed(self, keys: list[str], old: object, value: object):
            if len(keys) >= 3:
                keys = keys[-3:]
            else:
                keys = keys[-2:]
            VALUE_HUB.set(".".join(keys), value)

    class GenType(QObject):
        class LinkerType(QObject):
            changed = Signal()
            default_heap_size_changed = Signal(int, int)
            default_stack_size_changed = Signal(int, int)

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
            def default_heap_size(self) -> int:
                return self.__data.get("defaultHeapSize", -1)

            @default_heap_size.setter
            def default_heap_size(self, size: int):
                if self.default_heap_size == size:
                    return
                old = self.default_heap_size
                self.__data["defaultHeapSize"] = size
                self.default_heap_size_changed.emit(old, size)
                self.changed.emit()

            @property
            def default_stack_size(self) -> int:
                return self.__data.get("defaultStackSize", -1)

            @default_stack_size.setter
            def default_stack_size(self, size: int):
                if self.default_stack_size == size:
                    return
                old = self.default_stack_size
                self.__data["defaultStackSize"] = size
                self.default_stack_size_changed.emit(old, size)
                self.changed.emit()

        changed = Signal()
        builder_changed = Signal(str, str)
        copy_library_changed = Signal(bool, bool)
        use_toolchains_package_changed = Signal(bool, bool)
        toolchains_changed = Signal(str, str)
        builder_version_changed = Signal(str, str)
        toolchains_version_changed = Signal(str, str)
        hal_changed = Signal(str, str)
        hal_version_changed = Signal(str, str)

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
            self.builder_changed.emit(old, builder)
            self.changed.emit()

        @property
        def copy_library(self) -> bool:
            return self.__data.setdefault("copyLibrary", True)

        @copy_library.setter
        def copy_library(self, copy_library: bool):
            if self.copy_library == copy_library:
                return
            old = self.copy_library
            self.__data["copyLibrary"] = copy_library
            self.copy_library_changed.emit(old, copy_library)
            self.changed.emit()

        @property
        def use_toolchains_package(self) -> bool:
            return self.__data.setdefault("useToolchainsPackage", False)

        @use_toolchains_package.setter
        def use_toolchains_package(self, use_toolchains_package: bool):
            if self.use_toolchains_package == use_toolchains_package:
                return
            old = self.use_toolchains_package
            self.__data["useToolchainsPackage"] = use_toolchains_package
            self.use_toolchains_package_changed.emit(old, use_toolchains_package)
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
            self.toolchains_changed.emit(old, toolchains)
            self.changed.emit()

        @property
        def builder_version(self) -> str:
            return self.__data.get("builderVersion", "")

        @builder_version.setter
        def builder_version(self, version: str):
            if self.builder_version == version:
                return
            old = self.builder_version
            self.__data["builderVersion"] = version
            self.builder_version_changed.emit(old, version)
            self.changed.emit()

        @property
        def toolchains_version(self) -> str:
            return self.__data.get("toolchainsVersion", "")

        @toolchains_version.setter
        def toolchains_version(self, version: str):
            if self.toolchains_version == version:
                return
            old = self.toolchains_version
            self.__data["toolchainsVersion"] = version
            self.toolchains_version_changed.emit(old, version)
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
            self.hal_changed.emit(old, hal)
            self.changed.emit()

        @property
        def hal_version(self) -> str:
            return self.__data.get("halVersion", "")

        @hal_version.setter
        def hal_version(self, version: str):
            if self.hal_version == version:
                return
            old = self.hal_version
            self.__data["halVersion"] = version
            self.hal_version_changed.emit(old, version)
            self.changed.emit()

        @property
        def linker(self) -> LinkerType:
            return self.__linker

    changed = Signal()
    name_changed = Signal(str, str)
    target_chip_changed = Signal(str, str)
    vendor_changed = Signal(str, str)
    version_changed = Signal(str, str)
    modules_changed = Signal(list, list)

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
        self.name_changed.emit(old, name)
        self.changed.emit()

    @property
    def target_chip(self) -> str:
        return self.__data.get("targetChip", "")

    @target_chip.setter
    def target_chip(self, target_chip: str):
        if self.target_chip == target_chip:
            return
        old = self.target_chip
        self.__data["targetChip"] = target_chip
        self.target_chip_changed.emit(old, target_chip)
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
        self.vendor_changed.emit(old, vendor)
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
        self.version_changed.emit(old, version)
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
        self.modules_changed.emit(old, modules)
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
                name in SUMMARY.project_summary().module_list()
                and cfg is not None
                and len(cfg) > 0
            ):
                ip = IP.project_ips().get(name)
                if ip and ip.activated:
                    modules.add(name)
        self.modules = sorted(modules)


class Project(QObject):
    reloaded = Signal()
    title_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__path = ""
        self.__valid = False
        self.__project = ProjectType({}, self)
        self.__project.changed.connect(self.__on_project_changed)
        self.__is_changed = False

    @logger.catch(default=False)
    def __check_project(self, project: dict) -> bool:
        with open(
            os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "project.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=project, schema=schema)
        return True

    @logger.catch(default={})
    def __get_project(self, file: str) -> dict:
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                project = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__check_project(project)
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

    def set_path(self, path: str):
        path = os.path.abspath(path)
        if self.__path != path:
            self.load(path)
            self.reloaded.emit()
            self.__path = path

    def new(self, path: str, name: str, target_chip: str, vendor: str):
        self.__path = os.path.abspath(os.path.join(path, name, f"{name}.csp"))
        p = os.path.dirname(self.__path)
        if not os.path.isdir(p):
            os.makedirs(p)

        project = self.project()
        project.name = name
        project.target_chip = target_chip
        project.vendor = vendor
        project.version = SETTINGS.VERSION

        self.save()
        self.load(self.__path)

    def folder(self) -> str:
        return os.path.dirname(self.__path)

    def hal_folder(self) -> str:
        return PACKAGE.index().path(
            "hal", self.__project.gen.hal, self.__project.gen.hal_version
        )

    def toolchains_folder(self) -> str:
        return PACKAGE.index().path(
            "toolchains",
            self.__project.gen.toolchains,
            self.__project.gen.toolchains_version,
        )

    def __build_values_hub(
        self, nested_dict: dict, parent_key: str = "", sep: str = "."
    ):
        flattened = {}
        ignore = ["configs"]
        for key, value in nested_dict.items():
            if isinstance(value, dict):
                if key in ignore:
                    new_key = parent_key
                else:
                    new_key = f"{parent_key}{sep}{key}" if parent_key else key
                flattened.update(self.__build_values_hub(value, new_key, sep))
            else:
                new_key = (
                    f"{parent_key}{sep}{key}" if parent_key else f"project{sep}{key}"
                )
                flattened[new_key] = value
        return flattened

    def load(self, path: str) -> bool:
        self.__valid = False
        # noinspection PyTypeChecker,PyArgumentList
        self.__project.origin = self.__get_project(path)

        if len(self.__project.origin) == 0:
            logger.error(f'project "{path}" load failed.')
            return self.__valid

        summary = SUMMARY.set_project_summary(
            self.__project.vendor, self.__project.target_chip
        )
        if len(summary.origin) == 0:
            logger.error(
                f"invalid summary {self.__project.vendor}, {self.__project.target_chip}!"
            )
            return self.__valid

        modules = {}
        modules.update(summary.modules.peripherals)
        modules.update(summary.modules.middlewares)
        for _, group in modules.items():
            for name, module in group.items():
                if module.ip != "":
                    ip = IP.set_project_ip(self.__project.vendor, name, module.ip)
                    if len(ip.origin) == 0:
                        logger.error(
                            f"invalid ip {self.__project.vendor}, {self.__project.target_chip}, {name} {module.ip}!"
                        )
                        return self.__valid

        # init
        value_hub = self.__build_values_hub(self.__project.origin)
        for k, v in SUMMARY.project_summary().origin.items():
            if not isinstance(v, dict):
                value_hub[f"summary.{k}"] = v
        VALUE_HUB.assign(value_hub)

        self.__valid = True
        return self.__valid

    def project(self) -> ProjectType:
        return self.__project

    def dump(self):
        return yaml.dump(self.__project.origin)

    def is_generate_setting_valid(self) -> tuple[bool, str]:
        if self.project().gen.use_toolchains_package and not os.path.isdir(
            self.toolchains_folder()
        ):
            return (
                False,
                f"the toolchains folder does not exist! maybe the toolchains '{self.project().gen.toolchains}:{self.project().gen.toolchains_version}' is not installed yet",
            )
        elif not os.path.isdir(self.hal_folder()):
            return (
                False,
                f"the hal folder does not exist! maybe the hal '{self.project().gen.hal}:{self.project().gen.hal_version}' is not installed yet",
            )
        elif self.project().gen.builder == "":
            return False, "the builder is not set"
        elif self.project().gen.builder_version == "":
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
            self.__is_changed = False
            self.title_changed.emit(self.title())

    def title(self):
        if self.__is_changed:
            return self.__project.name + "*"
        else:
            return self.__project.name

    def is_changed(self) -> bool:
        return self.__is_changed

    def __on_project_changed(self):
        self.__is_changed = True
        self.title_changed.emit(self.title())

    def pin_instance(self) -> IpType | None:
        pin_instance = SUMMARY.project_summary().pin_instance()
        ips = IP.project_ips()
        if pin_instance in ips:
            return ips[pin_instance]
        else:
            logger.error(f"invalid pin instance: {pin_instance}!")
            return None


PROJECT = Project()
