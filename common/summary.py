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
# @file        summary.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-12     xqyjlj       initial version
#

import json
import os

import jsonschema
import yaml
from loguru import logger

from .i18n_type import I18nType
from .settings import SETTINGS


class SummaryType:
    class DocumentType:
        class DocumentUnitType:
            def __init__(self, data: dict):
                self.__data = data
                self.__url = None

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def url(self) -> I18nType:
                if self.__url is None:
                    self.__url = I18nType(self.__data.get("url", {}))
                return self.__url

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
        def datasheets(self) -> dict[str, DocumentUnitType]:
            if self.__datasheets is None:
                self.__datasheets = {}
                datasheets = self.__data.get("datasheets", {})
                for name, unit in datasheets.items():
                    self.__datasheets[name] = SummaryType.DocumentType.DocumentUnitType(
                        unit if unit is not None else {}
                    )
            return self.__datasheets

        @property
        def errata(self) -> dict[str, DocumentUnitType]:
            if self.__errata is None:
                self.__errata = {}
                errata = self.__data.get("errata", {})
                for name, unit in errata.items():
                    self.__errata[name] = SummaryType.DocumentType.DocumentUnitType(
                        unit if unit is not None else {}
                    )
            return self.__errata

        @property
        def references(self) -> dict[str, DocumentUnitType]:
            if self.__references is None:
                self.__references = {}
                references = self.__data.get("references", {})
                for name, unit in references.items():
                    self.__references[name] = SummaryType.DocumentType.DocumentUnitType(
                        unit if unit is not None else {}
                    )
            return self.__references

    class ModuleType:
        def __init__(self, data: dict):
            self.__data = data

            self.__description = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def description(self) -> I18nType:
            if self.__description is None:
                self.__description = I18nType(self.__data.get("description", {}))
            return self.__description

        @property
        def ip(self) -> str:
            return self.__data.get("ip", "")

    class LinkerType:
        def __init__(self, data: dict):
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def defaultHeapSize(self) -> int:
            size = self.__data.get("defaultHeapSize", -1)
            if isinstance(size, str):
                size = int(size, 16)
            return size

        @property
        def defaultStackSize(self) -> int:
            size = self.__data.get("defaultStackSize", -1)
            if isinstance(size, str):
                size = int(size, 16)
            return size

    class PinType:
        def __init__(self, data: dict):
            self.__data = data
            self.__functions = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def position(self) -> int:
            return self.__data.get("position", -1)

        @property
        def type(self) -> str:
            return self.__data.get("type", "")

        @property
        def signals(self) -> list[str]:
            return self.__data.get("signals", [])

        @property
        def modes(self) -> list[str]:
            return self.__data.get("modes", [])

        # ----------------------------------------------------------------------

        def functions(self) -> list[str]:
            if self.__functions is None:
                self.__functions = self.signals + self.modes
            return self.__functions

    def __init__(self, data: dict):
        self.__data = data

        self.__vendorUrl = None
        self.__documents = None
        self.__illustrate = None
        self.__introduction = None
        self.__modules = None
        self.__url = None
        self.__linker = None
        self.__pins = None

        # ----------------------------------------------------------------------

        self.__moduleList = None
        self.__pinInstance = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @property
    def clockTree(self) -> str:
        return self.__data.get("clockTree", "")

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

    @property
    def vendorUrl(self) -> I18nType:
        if self.__vendorUrl is None:
            self.__vendorUrl = I18nType(self.__data.get("vendorUrl", {}))
        return self.__vendorUrl

    @property
    def documents(self) -> DocumentType:
        if self.__documents is None:
            self.__documents = SummaryType.DocumentType(
                self.__data.get("documents", {})
            )
        return self.__documents

    @property
    def hals(self) -> list[str]:
        return self.__data.get("hals", [])

    @property
    def hasPowerPad(self) -> bool:
        return self.__data.get("hasPowerPad", False)

    @property
    def illustrate(self) -> I18nType:
        if self.__illustrate is None:
            self.__illustrate = I18nType(self.__data.get("illustrate", {}))
        return self.__illustrate

    @property
    def introduction(self) -> I18nType:
        if self.__introduction is None:
            self.__introduction = I18nType(self.__data.get("introduction", {}))
        return self.__introduction

    @property
    def modules(self) -> dict[str, dict[str, ModuleType]]:
        if self.__modules is None:
            self.__modules = {}
            modules = self.__data.get("modules", {})
            for groupName, group in modules.items():
                groupUnit = {}
                for name, unit in group.items():
                    groupUnit[name] = SummaryType.ModuleType(
                        unit if unit is not None else {}
                    )
                self.__modules[groupName] = groupUnit
        return self.__modules

    @property
    def package(self) -> str:
        return self.__data.get("package", "")

    @property
    def url(self) -> I18nType:
        if self.__url is None:
            self.__url = I18nType(self.__data.get("url", {}))
        return self.__url

    @property
    def builder(self) -> dict[str, dict[str, list[str]]]:
        return self.__data.get("builder", {})

    @property
    def linker(self) -> LinkerType:
        if self.__linker is None:
            self.__linker = SummaryType.LinkerType(self.__data.get("linker", {}))
        return self.__linker

    @property
    def pins(self) -> dict[str, PinType]:
        if self.__pins is None:
            self.__pins = {}
            pins = self.__data.get("pins", {})
            for name, unit in pins.items():
                self.__pins[name] = SummaryType.PinType(
                    unit if unit is not None else {}
                )
        return self.__pins

    # ----------------------------------------------------------------------------------------------------------------------

    def moduleList(self) -> dict[str, ModuleType]:
        if self.__moduleList is None:
            self.__moduleList = {}
            modules = self.modules
            for groupName, group in modules.items():
                for name, module in group.items():
                    self.__moduleList[name] = module
        return self.__moduleList

    def pinInstance(self) -> str:
        if self.__pinInstance is None:
            for _, pin in self.pins.items():
                if len(pin.modes) > 0:
                    self.__pinInstance = pin.modes[0].split(":")[0]
                    break
        return self.__pinInstance or ""


class Summary:

    def __init__(self):
        self.__summaries = {}

        # ----------------------------------------------------------------------

        self.__vendor = ""
        self.__name = ""

    @logger.catch(default=False)
    def __checkSummary(self, summary: dict) -> bool:
        with open(
            os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "summary.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=summary, schema=schema)
        return True

    @logger.catch(default=SummaryType({}))
    def __getSummary(self, vendor: str, name: str) -> SummaryType:
        file = os.path.join(
            SETTINGS.DATABASE_FOLDER, "summary", vendor.lower(), f"{name.lower()}.yml"
        )
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                summary = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkSummary(summary)
            if succeed:
                return SummaryType(summary)
            else:
                return SummaryType({})
        else:
            logger.error(f"{file} is not file!")
            return SummaryType({})

    def getSummary(self, vendor: str, name: str) -> SummaryType:
        if vendor in self.__summaries and name in self.__summaries[vendor]:
            return self.__summaries[vendor][name]
        else:
            # noinspection PyTypeChecker,PyArgumentList
            summary = self.__getSummary(vendor, name)
            if vendor not in self.__summaries:
                self.__summaries[vendor] = {}
            self.__summaries[vendor][name] = summary
            # noinspection PyTypeChecker
            return summary

    def summaries(self) -> dict[str, dict[str, SummaryType]]:
        return self.__summaries

    def setProjectSummary(self, vendor: str, name: str) -> SummaryType:
        self.__vendor = vendor
        self.__name = name
        return self.projectSummary()

    def projectSummary(self) -> SummaryType:
        return self.getSummary(self.__vendor, self.__name)

    def findPinBySignal(self, signal: str, summary: SummaryType = None) -> list[str]:
        if summary is None:
            summary = self.projectSummary()
        pins = []
        for name, pin in summary.pins.items():
            if signal in pin.signals:
                pins.append(name)
        return pins


SUMMARY = Summary()
