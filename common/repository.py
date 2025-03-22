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
# @file        repository.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-07     xqyjlj       initial version
#

import json
import os

import jsonschema
import yaml
from loguru import logger

from .settings import SETTINGS


class RepositorySocType:
    class CurrentType:

        def __init__(self, data: dict):
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def lowest(self) -> float:
            return self.__data.get("lowest", 0)

        @property
        def run(self) -> float:
            return self.__data.get("run", 0)

    # ------------------------------------------------------------------------------------------------------------------
    class TemperatureType:

        def __init__(self, data: dict):
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def max(self) -> float:
            return self.__data.get("max", 0)

        @property
        def min(self) -> float:
            return self.__data.get("min", 0)

    # ------------------------------------------------------------------------------------------------------------------
    class VoltageType:

        def __init__(self, data: dict):
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def max(self) -> float:
            return self.__data.get("max", 0)

        @property
        def min(self) -> float:
            return self.__data.get("min", 0)

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(
        self, data: dict, kind: str, vendor: str, series: str, line: str, name: str
    ):
        self.__data = data
        self.__current = None
        self.__temperature = None
        self.__voltage = None
        self.__kind = kind
        self.__vendor = vendor
        self.__series = series
        self.__line = line
        self.__name = name

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def kind(self) -> str:
        return self.__kind

    @property
    def vendor(self) -> str:
        return self.__vendor

    @property
    def series(self) -> str:
        return self.__series

    @property
    def line(self) -> str:
        return self.__line

    @property
    def name(self) -> str:
        return self.__name

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def core(self) -> str:
        return self.__data.get("core", "")

    @property
    def current(self) -> CurrentType:
        if self.__current is None:
            self.__current = RepositorySocType.CurrentType(
                self.__data.get("current", {})
            )
        return self.__current

    @property
    def flash(self) -> float:
        return self.__data.get("flash", 0)

    @property
    def frequency(self) -> float:
        return self.__data.get("frequency", 0)

    @property
    def io(self) -> int:
        return self.__data.get("io", 0)

    @property
    def package(self) -> str:
        return self.__data.get("package", "")

    @property
    def peripherals(self) -> dict[str, int]:
        return self.__data.get("peripherals", {})

    @property
    def ram(self) -> float:
        return self.__data.get("ram", 0)

    @property
    def temperature(self) -> TemperatureType:
        if self.__temperature is None:
            self.__temperature = RepositorySocType.TemperatureType(
                self.__data.get("temperature", {})
            )
        return self.__temperature

    @property
    def voltage(self) -> VoltageType:
        if self.__voltage is None:
            self.__voltage = RepositorySocType.VoltageType(
                self.__data.get("voltage", {})
            )
        return self.__voltage


class RepositoryType:
    def __init__(self, data: dict):
        self.__data = data
        self.__all_types = []
        self.__all_vendors = []
        self.__all_series = []
        self.__all_lines = []
        self.__all_soc = []
        self.__all_cores = []
        self.__all_package = []

        for kind, kind_item in self.__data.items():
            self.__all_types.append(kind)
            for vendor, vendor_item in kind_item.items():
                self.__all_vendors.append(vendor)
                for series, series_item in vendor_item.items():
                    self.__all_series.append(series)
                    for line, line_item in series_item.items():
                        self.__all_lines.append(line)
                        for soc, soc_item in line_item.items():
                            if kind == "soc":
                                item = RepositorySocType(
                                    soc_item, kind, vendor, series, line, soc
                                )
                                self.__all_soc.append(item)
                                self.__all_cores.append(item.core)
                                self.__all_package.append(item.package)

        self.__all_cores = list(set(self.__all_cores))
        self.__all_package = list(set(self.__all_package))

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict[str, dict[str, dict[str, dict[str, dict[str, dict]]]]]:
        return self.__data

    def types(self) -> list[str]:
        return self.__all_types

    def all_types(self) -> list[str]:
        return self.types()

    def vendors(self, kind: str) -> list[str]:
        return list(self.__data.get(kind, {}).keys())

    def all_vendors(self) -> list[str]:
        return self.__all_vendors

    def series(self, kind: str, vendor: str) -> list[str]:
        return list(self.__data.get(kind, {}).get(vendor, {}).keys())

    def all_series(self) -> list[str]:
        return self.__all_series

    def lines(self, kind: str, vendor: str, series: str) -> list[str]:
        return list(self.__data.get(kind, {}).get(vendor, {}).get(series, {}).keys())

    def all_lines(self) -> list[str]:
        return self.__all_lines

    def names(self, kind: str, vendor: str, series: str, line: str) -> list[str]:
        return list(
            self.__data.get(kind, {})
            .get(vendor, {})
            .get(series, {})
            .get(line, {})
            .keys()
        )

    def __info(self, kind: str, vendor: str, series: str, line: str, name: str) -> dict:
        return (
            self.__data.get(kind, {})
            .get(vendor, {})
            .get(series, {})
            .get(line, {})
            .get(name, {})
        )

    def soc(
        self, kind: str, vendor: str, series: str, line: str, name: str
    ) -> RepositorySocType:
        return RepositorySocType(
            self.__info(kind, vendor, series, line, name),
            kind,
            vendor,
            series,
            line,
            name,
        )

    def all_soc(self) -> list[RepositorySocType]:
        return self.__all_soc

    def all_cores(self) -> list[str]:
        return self.__all_cores

    def all_package(self) -> list[str]:
        return self.__all_package


class Repository:

    def __init__(self):
        self.__repository = self.get_repository()

    @logger.catch(default=False)
    def __check_repository(self, repository: dict) -> bool:
        with open(
            os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "repository.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=repository, schema=schema)
        return True

    @logger.catch(default=RepositoryType({}))
    def __get_repository(self) -> RepositoryType:
        file = os.path.join(SETTINGS.DATABASE_FOLDER, "repository.yml")
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                repository = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__check_repository(repository)
            if succeed:
                return RepositoryType(repository)
            else:
                return RepositoryType({})
        else:
            logger.error(f"{file} is not file!")
            return RepositoryType({})

    def get_repository(self) -> RepositoryType:
        return self.__get_repository()

    def repository(self) -> RepositoryType:
        return self.__repository
