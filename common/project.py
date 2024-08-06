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

from .settings import SETTINGS, VERSION
from .database import Database
from .package import PACKAGE


class Summary(QObject):

    m_summary = {}
    m_modulesList = []

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
    def builder(self) -> dict[str, list[str]]:
        return self.m_summary.get("builder", {})

    @property
    def toolchains(self) -> list[str]:
        return self.m_summary.get("toolchains", [])

    @property
    def linker(self) -> dict:
        return self.m_summary.get("linker", {})

    @property
    def defaultHeapSize(self) -> str:
        return self.linker.get("defaultHeapSize", "")

    @property
    def defaultStackSize(self) -> str:
        return self.linker.get("defaultStackSize", "")

    @property
    def modulesList(self) -> list:
        return self.m_modulesList

    @property
    def origin(self) -> dict:
        return self.m_summary

    @origin.setter
    def origin(self, summary: dict):
        self.m_summary = summary

        for _, module_group in self.modules.items():
            for name, _ in module_group.items():
                self.m_modulesList.append(name)


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

    def ipTr(self, name: str) -> str:
        if name in self.m_ip_total:
            return self.m_ip_total[name]
        else:
            return name

    def ipTrR(self, name: str) -> str:
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

    pinConfigChanged = pyqtSignal(list, object, object)
    configChanged = pyqtSignal(list, object, object)
    gridPropertyIpTriggered = pyqtSignal(str, str)
    reloaded = pyqtSignal()
    modulesChanged = pyqtSignal()
    gridModeTriggered = pyqtSignal(str, str)

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
        self.saveTmp()

    @property
    def targetChip(self) -> str:
        return self.m_data.get("targetChip", "")

    @targetChip.setter
    def targetChip(self, targetChip: str):
        self.m_data["targetChip"] = targetChip
        self.saveTmp()

    @property
    def name(self) -> str:
        return self.m_data.get("name", "")

    @name.setter
    def name(self, name: str):
        self.m_data["name"] = name
        self.saveTmp()

    # gen
    @property
    def copyLibrary(self) -> bool:
        return self.m_data.get("gen", {}).get("copyLibrary", True)

    @copyLibrary.setter
    def copyLibrary(self, copyLibrary: bool):
        self.m_data.setdefault("gen", {})["copyLibrary"] = copyLibrary
        self.saveTmp()

    @property
    def defaultHeapSize(self) -> str:
        return self.m_data.get("gen", {}).get("linker", {}).get("linker", "")

    @defaultHeapSize.setter
    def defaultHeapSize(self, defaultHeapSize: str):
        self.m_data.setdefault("gen", {}).setdefault("linker", {})["defaultHeapSize"] = defaultHeapSize
        self.saveTmp()

    @property
    def defaultStackSize(self) -> str:
        return self.m_data.get("gen", {}).get("linker", {}).get("linker", "")

    @defaultStackSize.setter
    def defaultStackSize(self, defaultStackSize: str):
        self.m_data.setdefault("gen", {}).setdefault("linker", {})["defaultStackSize"] = defaultStackSize
        self.saveTmp()

    @property
    def useToolchainsPackage(self) -> bool:
        return self.m_data.get("gen", {}).get("useToolchainsPackage", False)

    @useToolchainsPackage.setter
    def useToolchainsPackage(self, useToolchainsPackage: bool):
        self.m_data.setdefault("gen", {})["useToolchainsPackage"] = useToolchainsPackage
        self.saveTmp()

    @property
    def toolchains(self) -> str:
        return self.m_data.get("gen", {}).get("toolchains", "")

    @toolchains.setter
    def toolchains(self, toolchains: str):
        self.m_data.setdefault("gen", {})["toolchains"] = toolchains
        self.saveTmp()

    @property
    def toolchainsVersion(self) -> str:
        return self.m_data.get("gen", {}).get("toolchainsVersion", "")

    @toolchainsVersion.setter
    def toolchainsVersion(self, toolchainsVersion: str):
        self.m_data.setdefault("gen", {})["toolchainsVersion"] = toolchainsVersion
        self.saveTmp()

    @property
    def halVersion(self) -> str:
        return self.m_data.get("gen", {}).get("halVersion", "")

    @halVersion.setter
    def halVersion(self, halVersion: str):
        self.m_data.setdefault("gen", {})["halVersion"] = halVersion
        self.saveTmp()

    @property
    def path(self) -> str:
        return self.m_path

    @path.setter
    def path(self, path: str):
        if self.m_path != path:
            self.load(path)
            self.reloaded.emit()
        self.m_path = path

    @property
    def dir(self) -> str:
        return os.path.dirname(self.m_path)

    @property
    def modules(self) -> list:
        return self.m_data.setdefault("modules", [])

    @property
    def halPath(self) -> str:
        return PACKAGE.path("hal", self.summary.hal, self.halVersion)

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

            self.summary.origin = Database.getSummary(self.vendor, self.targetChip)

            ip = {}
            for _, module_group in self.summary.modules.items():
                for name, module in module_group.items():
                    if "ip" in module:
                        ip[name] = Database.getIp(self.vendor, module["ip"])
            self.ip.origin = ip

        else:
            print(f"{path} is not file!")

    def dump(self):
        return yaml.dump(self.m_data)

    def saveTmp(self):
        if self.m_path != "":
            path = f"{self.m_path}.tmp" if self.m_path.endswith(".csp") else self.m_path
            with open(path, 'w', encoding='utf-8') as f:
                f.write(self.dump())

    def config(self, path: str, default=None):
        map = self.m_data.get("config", {})
        keys = path.split("/")
        for key in keys:
            if key not in map:
                return default
            map = map[key]
        return map

    def setConfig(self, path: str, value: object):
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
                    self.pinConfigChanged.emit(keys, old, value)
                else:
                    self.configChanged.emit(keys, old, value)

            modules = set()
            for name, cfg in self.m_data["config"].items():
                if name in self.summary.m_modulesList and cfg != None and len(cfg) > 0:
                    modules.add(name)
            if set(self.modules) != modules:
                self.m_data["modules"] = list(modules)
                self.modulesChanged.emit()

            self.saveTmp()

    def triggerGridPropertyIp(self, instance: str, name: str):
        self.gridPropertyIpTriggered.emit(instance, name)

    def triggerGridMode(self, module: str, widget: str):
        self.gridModeTriggered.emit(module, widget)


PROJECT = Project()
