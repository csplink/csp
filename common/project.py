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

from .settings import SETTINGS, VERSION
from .database import Database
from .package import PACKAGE


class Summary(QObject):

    m_summary = {}
    m_modules_list = []

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    @property
    def hal(self) -> str:
        return self.m_summary.get("hal", "unknown")

    @property
    def package(self) -> str:
        return self.m_summary.get("package", "unknown")

    @property
    def pins(self) -> dict:
        return self.m_summary.get("pins", {})

    @property
    def modules(self) -> dict:
        return self.m_summary.get("modules", {})

    @property
    def pinIp(self) -> dict:
        return self.m_summary.get("pinIp", "")

    @property
    def builder(self) -> dict[str, dict[str, list[str]]]:
        return self.m_summary.get("builder", {})

    @property
    def linker(self) -> dict:
        return self.m_summary.get("linker", {})

    @property
    def default_heap_size(self) -> str:
        return self.linker.get("defaultHeapSize", "")

    @property
    def default_stack_size(self) -> str:
        return self.linker.get("defaultStackSize", "")

    @property
    def modules_list(self) -> list:
        return self.m_modules_list

    @property
    def origin(self) -> dict:
        return self.m_summary

    @origin.setter
    def origin(self, summary: dict):
        self.m_summary = summary

        for _, module_group in self.modules.items():
            for name, _ in module_group.items():
                self.m_modules_list.append(name)


class Ip(QObject):

    m_ip = {}
    m_ip_total = {}
    m_ip_reverse_total = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def ip(self, name: str) -> dict:
        if name not in self.m_ip:
            return {}
        return self.m_ip[name]

    def iptr(self, name: str) -> str:
        if name in self.m_ip_total:
            return self.m_ip_total[name]
        else:
            return name

    def iptr2(self, name: str) -> str:
        if name in self.m_ip_reverse_total:
            return self.m_ip_reverse_total[name]
        else:
            return name

    @property
    def origin(self) -> dict:
        return self.m_ip

    @origin.setter
    def origin(self, ip: dict):
        self.m_ip = ip

        locale = SETTINGS.get(SETTINGS.language).value.name()
        for name in ip.keys():
            for _, parameter in ip[name]["parameters"].items():
                for key, value in parameter["values"].items():
                    self.m_ip_total[key] = value["comment"][locale]
                    self.m_ip_reverse_total[value["comment"][locale]] = key


class Project(QObject):
    m_data = {}
    m_path = ""
    summary = None
    ip = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.summary = Summary(self)
        self.ip = Ip(self)

    @property
    def version(self) -> str:
        return self.m_data.setdefault("version", VERSION)

    @property
    def vendor(self) -> str:
        return self.m_data.get("vendor", "")

    @property
    def origin(self) -> dict:
        return self.m_data

    @vendor.setter
    def vendor(self, vendor: str):
        self.m_data["vendor"] = vendor
        self.save_tmp()

    @property
    def target_chip(self) -> str:
        return self.m_data.get("targetChip", "")

    @target_chip.setter
    def target_chip(self, chip: str):
        self.m_data["targetChip"] = chip
        self.save_tmp()

    @property
    def name(self) -> str:
        return self.m_data.get("name", "")

    @name.setter
    def name(self, name: str):
        self.m_data["name"] = name
        self.save_tmp()

    # gen

    # gen/copyLibrary
    sig_copy_library_changed = Signal(bool)

    @property
    def copy_library(self) -> bool:
        return self.m_data.get("gen", {}).get("copyLibrary", True)

    @copy_library.setter
    def copy_library(self, is_copy_library: bool):
        if self.copy_library == is_copy_library:
            return
        self.m_data.setdefault("gen", {})["copyLibrary"] = is_copy_library
        self.sig_copy_library_changed.emit(is_copy_library)
        self.save_tmp()

    @property
    def default_heap_size(self) -> str:
        return self.m_data.get("gen", {}).get("linker", {}).get("defaultHeapSize", "")

    @default_heap_size.setter
    def default_heap_size(self, size: str):
        self.m_data.setdefault("gen", {}).setdefault("linker", {})["defaultHeapSize"] = size
        self.save_tmp()

    @property
    def default_stack_size(self) -> str:
        return self.m_data.get("gen", {}).get("linker", {}).get("defaultStackSize", "")

    @default_stack_size.setter
    def default_stack_size(self, size: str):
        self.m_data.setdefault("gen", {}).setdefault("linker", {})["defaultStackSize"] = size
        self.save_tmp()

    # gen/useToolchainsPackage
    sig_use_toolchains_package_changed = Signal(bool)

    @property
    def use_toolchains_package(self) -> bool:
        return self.m_data.get("gen", {}).get("useToolchainsPackage", False)

    @use_toolchains_package.setter
    def use_toolchains_package(self, is_use_toolchains_package: bool):
        if self.use_toolchains_package == is_use_toolchains_package:
            return
        self.m_data.setdefault("gen", {})["useToolchainsPackage"] = is_use_toolchains_package
        self.sig_use_toolchains_package_changed.emit(is_use_toolchains_package)
        self.save_tmp()

    # gen/toolchains
    sig_toolchains_changed = Signal(str)

    @property
    def toolchains(self) -> str:
        return self.m_data.get("gen", {}).get("toolchains", "")

    @toolchains.setter
    def toolchains(self, toolchains: str):
        if self.toolchains == toolchains:
            return
        self.m_data.setdefault("gen", {})["toolchains"] = toolchains
        self.sig_toolchains_changed.emit(toolchains)
        self.save_tmp()

    # gen/builder
    sig_builder_changed = Signal(str)

    @property
    def builder(self) -> str:
        return self.m_data.get("gen", {}).get("builder", "")

    @builder.setter
    def builder(self, builder: str):
        if self.builder == builder:
            return
        self.m_data.setdefault("gen", {})["builder"] = builder
        self.sig_builder_changed.emit(builder)
        self.save_tmp()

    # gen/builderVersion
    sig_builder_version_changed = Signal(str)

    @property
    def builder_version(self) -> str:
        return self.m_data.get("gen", {}).get("builderVersion", "")

    @builder_version.setter
    def builder_version(self, version: str):
        if self.builder_version == version:
            return
        self.m_data.setdefault("gen", {})["builderVersion"] = version
        self.sig_builder_version_changed.emit(version)
        self.save_tmp()

    # gen/toolchainsVersion
    sig_toolchains_version_changed = Signal(str)

    @property
    def toolchainsVersion(self) -> str:
        return self.m_data.get("gen", {}).get("toolchainsVersion", "")

    @toolchainsVersion.setter
    def toolchainsVersion(self, version: str):
        if self.toolchainsVersion == version:
            return
        self.m_data.setdefault("gen", {})["toolchainsVersion"] = version
        self.sig_toolchains_version_changed.emit(version)
        self.save_tmp()

    # gen/halVersion
    sig_hal_version_changed = Signal(str)

    @property
    def hal_version(self) -> str:
        return self.m_data.get("gen", {}).get("halVersion", "")

    @hal_version.setter
    def hal_version(self, version: str):
        if self.hal_version == version:
            return
        self.m_data.setdefault("gen", {})["halVersion"] = version
        self.sig_hal_version_changed.emit(version)
        self.save_tmp()

    def is_gen_valid(self) -> bool:
        pass

    sig_reloaded = Signal()

    @property
    def path(self) -> str:
        return self.m_path

    @path.setter
    def path(self, path: str):
        if self.m_path != path:
            self.load(path)
            self.sig_reloaded.emit()
        self.m_path = path

    @property
    def dir(self) -> str:
        return os.path.dirname(self.m_path)

    @property
    def modules(self) -> list:
        return self.m_data.setdefault("modules", [])

    @property
    def hal_path(self) -> str:
        return PACKAGE.path("hal", self.summary.hal, self.hal_version)

    @property
    def toolchains_path(self) -> str:
        return PACKAGE.path("toolchains", self.toolchains, self.toolchainsVersion)

    def load(self, path: str):
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                map = yaml.load(f.read(), Loader=yaml.FullLoader)
            with open("resource/database/schema/project.yml", 'r', encoding='utf-8') as f:
                schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            try:
                jsonschema.validate(instance=map, schema=schema)
                self.m_data = map
            except jsonschema.exceptions.ValidationError as exception:
                print(f"invalid yaml {path}")
                print(exception)

            self.summary.origin = Database.get_summary(self.vendor, self.target_chip)

            ip = {}
            for _, module_group in self.summary.modules.items():
                for name, module in module_group.items():
                    if "ip" in module:
                        ip[name] = Database.get_ip(self.vendor, module["ip"])
            self.ip.origin = ip

        else:
            print(f"{path} is not file!")

    def dump(self):
        return yaml.dump(self.m_data)

    def save_tmp(self):
        if self.m_path != "":
            path = f"{self.m_path}.tmp" if self.m_path.endswith(".csp") else self.m_path
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.dump())

    sig_pin_config_changed = Signal(list, object, object)
    sig_config_changed = Signal(list, object, object)
    sig_modules_changed = Signal()

    def config(self, path: str, default=None):
        map = self.m_data.get("config", {})
        keys = path.split("/")
        for key in keys:
            if key not in map:
                return default
            map = map[key]
        return map

    def set_config(self, path: str, value: object):
        map = self.m_data.setdefault("config", {})
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
                    self.sig_pin_config_changed.emit(keys, old, value)
                else:
                    self.sig_config_changed.emit(keys, old, value)

            modules = set()
            for name, cfg in self.m_data["config"].items():
                if name in self.summary.m_modules_list and cfg != None and len(cfg) > 0:
                    modules.add(name)
            if set(self.modules) != modules:
                self.m_data["modules"] = list(modules)
                self.sig_modules_changed.emit()

            self.save_tmp()

    sig_grid_property_ip_triggered = Signal(str, str)

    def trigger_grid_property_ip(self, instance: str, name: str):
        self.sig_grid_property_ip_triggered.emit(instance, name)

    sig_grid_mode_triggered = Signal(str, str)

    def trigger_grid_mode(self, module: str, widget: str):
        self.sig_grid_mode_triggered.emit(module, widget)


PROJECT = Project()
