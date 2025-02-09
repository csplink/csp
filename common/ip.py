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
# @file        ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-11-02     xqyjlj       initial version
#

from __future__ import annotations

import json
import os

import jsonschema
import yaml
from PySide6.QtCore import Signal, QObject
from loguru import logger

from utils import Express
from .i18n_type import I18nType
from .settings import SETTINGS
from .value_hub import VALUE_HUB


class IpType(QObject):
    parameterItemUpdated = Signal(list)
    totalChanged = Signal(str, str, str, str)
    total2Changed = Signal(str, str, str, str)

    class ParameterUnitType:
        class ExpressionType:
            def __init__(self, data: dict):
                self.__data = data

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def display(self) -> str:
                return self.__data.get("display", "")

            @property
            def real(self) -> str:
                return self.__data.get("real", "")

        class ValueUnitType:
            class ExpressionType:
                def __init__(self, data: dict):
                    self.__data = data

                def __str__(self) -> str:
                    return json.dumps(self.__data, indent=2, ensure_ascii=False)

                @property
                def origin(self) -> dict:
                    return self.__data

                @property
                def display(self) -> str:
                    return self.__data.get("display", "")

                @property
                def real(self) -> str:
                    return self.__data.get("real", "")

            def __init__(self, data: dict):
                self.__data = data

                self.__comment = None
                self.__expression = None

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def expression(self) -> ExpressionType:
                if self.__expression is None:
                    self.__expression = self.ExpressionType(
                        self.__data.get("expression", {})
                    )
                return self.__expression

            @property
            def comment(self) -> I18nType:
                if self.__comment is None:
                    self.__comment = I18nType(self.__data.get("comment", {}))
                return self.__comment

        def __init__(self, data: dict):
            self.__data = data

            self.__display = None
            self.__description = None
            self.__values = None
            self.__expression = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def display(self) -> I18nType:
            if self.__display is None:
                self.__display = I18nType(self.__data.get("display", {}))
            return self.__display

        @property
        def description(self) -> I18nType:
            if self.__description is None:
                self.__description = I18nType(self.__data.get("description", {}))
            return self.__description

        @property
        def readonly(self) -> bool:
            return self.__data.get("readonly", True)

        @property
        def type(self) -> str:
            return self.__data.get("type", "")

        @property
        def values(self) -> dict[str, ValueUnitType]:
            if self.__values is None:
                self.__values = {}
                for name, value in self.__data.get("values", {}).items():
                    self.__values[name] = self.ValueUnitType(value)
            return self.__values

        @property
        def group(self) -> str:
            return self.__data.get("group", "")

        @property
        def default(self) -> str | float | int | bool | None:
            return self.__data.get("default", None)

        @property
        def expression(self) -> ExpressionType:
            if self.__expression is None:
                self.__expression = self.ExpressionType(
                    self.__data.get("expression", {})
                )
            return self.__expression

        @property
        def visible(self) -> bool:
            return self.__data.get("visible", True)

        @property
        def max(self) -> float:
            return self.__data.get("max", -1)

        @property
        def min(self) -> float:
            return self.__data.get("min", -1)

    class ControlModeUnitType:
        class PinUnitType:
            def __init__(self, data: dict):
                self.__data = data
                self.__dependencies = None

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def mode(self) -> str:
                return self.__data.get("mode", "")

            @property
            def condition(self) -> str:
                return self.__data.get("condition", "")

            def dependencies(self) -> list[str]:
                if self.__dependencies is None:
                    self.__dependencies = Express.variables(self.condition)
                return self.__dependencies

        def __init__(
            self, data: dict, name: str, parameters: dict[str, IpType.ParameterUnitType]
        ):
            self.__data = data
            self.__name = name
            self.__parameters = parameters
            self.__pins = None
            self.__dependencies = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def values(self) -> list[str]:
            values = self.__data.get("values")
            if values is None:
                values = list(self.__parameters[self.__name].values.keys())
            return values

        @property
        def default(self) -> str | float | int | bool | None:
            default = self.__data.get("default")
            if default is None:
                default = self.__parameters[self.__name].default
            return default

        @property
        def pins(self) -> dict[str, PinUnitType]:
            if self.__pins is None:
                self.__pins = {}
                for name, value in self.__data.get("pins", {}).items():
                    self.__pins[name] = self.PinUnitType(value)
            return self.__pins

        def dependencies(self) -> list[str]:
            if self.__dependencies is None:
                self.__dependencies = []
                for name, pin in self.pins.items():
                    self.__dependencies += pin.dependencies()
                self.__dependencies = sorted(set(self.__dependencies))
            return self.__dependencies

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.__data = data
        self.__parameters = None
        self.__controls = None
        self.__pinModes = None
        self.__modes = None

        # ----------------------------------------------------------------------

        self.__conditions = {}

        self.__total = None
        self.__total2 = None

        VALUE_HUB.changed.connect(self.__on_valueHub_changed)

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def parameters(self) -> dict[str, ParameterUnitType]:
        if self.__parameters is None:
            self.__parameters = {}
            for name, param in self.__data.get("parameters", {}).items():
                param: dict
                if param.get("(default)") is None:
                    self.__parameters[name] = IpType.ParameterUnitType(param)
                else:
                    tmp = None
                    express = ""
                    for expression, value in param.items():
                        if expression == "(default)":
                            continue
                        if Express.boolExpr(expression, VALUE_HUB.values()):
                            tmp = value
                            express = expression
                            break
                    if tmp is None:
                        express = "(default)"
                        tmp = param.get("(default)", {})
                    self.__parameters[name] = IpType.ParameterUnitType(tmp)
                    self.__conditions[name] = express
        return self.__parameters

    @property
    def controls(self) -> dict[str, ControlModeUnitType]:
        if self.__controls is None:
            self.__controls = {}
            for name, item in self.__data.get("controls", {}).items():
                self.__controls[name] = IpType.ControlModeUnitType(
                    item, name, self.parameters
                )
        return self.__controls

    @property
    def pinModes(self) -> dict[str, dict[str, ControlModeUnitType]]:
        if self.__pinModes is None:
            self.__pinModes = {}
            for name, modeItem in self.__data.get("pinModes", {}).items():
                self.__pinModes[name] = {}
                for modeName, mode in modeItem.items():
                    self.__pinModes[name][modeName] = IpType.ControlModeUnitType(
                        mode, modeName, self.parameters
                    )
        return self.__pinModes

    @property
    def modes(self) -> dict[str, ControlModeUnitType]:
        if self.__modes is None:
            self.__modes = {}
            for name, item in self.__data.get("modes", {}).items():
                self.__modes[name] = IpType.ControlModeUnitType(
                    item, name, self.parameters
                )
        return self.__modes

    # ------------------------------------------------------------------------------------------------------------------

    def total(self) -> dict[str, dict[str, str]]:
        if self.__total is None:
            self.__total = {}
            locale = SETTINGS.get(SETTINGS.language).value.name()
            for name, parameter in self.parameters.items():
                self.__total[name] = {}
                for key, value in parameter.values.items():
                    self.__total[name][key] = value.comment.get(locale)
        return self.__total

    def total2(self) -> dict[str, dict[str, str]]:
        if self.__total2 is None:
            self.__total2 = {}
            locale = SETTINGS.get(SETTINGS.language).value.name()
            for name, parameter in self.parameters.items():
                self.__total2[name] = {}
                for key, value in parameter.values.items():
                    self.__total2[name][value.comment.get(locale)] = key
        return self.__total2

    def __on_valueHub_changed(self):
        li = []
        for name, condition in self.__conditions.items():
            param = self.__data["parameters"][name]
            tmp = None
            express = ""
            for expression, value in param.items():
                if expression == "(default)":
                    continue
                if Express.boolExpr(expression, VALUE_HUB.values()):
                    tmp = value
                    express = expression
                    break
            if tmp is None:
                express = "(default)"
                tmp = param.get("(default)")

            if condition != express:
                li.append(name)
                self.parameters[name] = IpType.ParameterUnitType(tmp)
                self.__conditions[name] = express
        if len(li) > 0:
            self.__flushI18n(li)
            self.parameterItemUpdated.emit(li)

    def __flushI18n(self, names: list[str]):
        locale = SETTINGS.get(SETTINGS.language).value.name()
        for name in names:
            parameter = self.parameters[name]
            for key, value in parameter.values.items():
                val = value.comment.get(locale)
                if self.total()[name].get(key, "") != val:
                    old = self.total()[name].get(key, "")
                    self.total()[name][key] = val
                    self.totalChanged.emit(name, key, old, val)

                if self.total2()[name].get(val, "") != key:
                    old = self.total2()[name].get(val, "")
                    self.total2()[name][val] = key
                    self.total2Changed.emit(name, val, old, key)


class Ip(QObject):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__ips = {}

        # ----------------------------------------------------------------------
        self.__projectIps = {}

        self.__flushTotal = False
        self.__total = None
        self.__flushTotal2 = False
        self.__total2 = None

    @logger.catch(default=False)
    def __checkIp(self, ip: dict) -> bool:
        with open(
            os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "ip.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=ip, schema=schema)
        return True

    @logger.catch(default=IpType({}))
    def __getIp(self, vendor: str, name: str) -> IpType:
        file = os.path.join(
            SETTINGS.DATABASE_FOLDER, "ip", vendor.lower(), f"{name.lower()}.yml"
        )
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                ip = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkIp(ip)
            if succeed:
                return IpType(ip, self)
            else:
                return IpType({})
        else:
            logger.error(f"{file} is not file!")
            return IpType({})

    def getIp(self, vendor: str, instance: str, name: str) -> IpType:
        if (
            vendor in self.__ips
            and instance in self.__ips[vendor]
            and name in self.__ips[vendor][instance]
        ):
            return self.__ips[vendor][instance][name]
        # noinspection PyTypeChecker,PyArgumentList
        ip = self.__getIp(vendor, name)
        if vendor not in self.__ips:
            self.__ips[vendor] = {}
        if instance not in self.__ips[vendor]:
            self.__ips[vendor][instance] = {}
        self.__ips[vendor][instance][name] = ip
        # noinspection PyTypeChecker
        return ip

    def ips(self) -> dict[str, dict[str, dict[str, IpType]]]:
        return self.__ips

    def setProjectIp(self, vendor: str, instance: str, name: str) -> IpType:
        self.__flushTotal = True
        self.__flushTotal2 = True
        ip = self.getIp(vendor, instance, name)
        self.__projectIps[instance] = ip
        ip.totalChanged.connect(self.__on_ip_totalChanged)
        ip.total2Changed.connect(self.__on_ip_total2Changed)

        return ip

    def projectIps(self) -> dict[str, IpType]:
        return self.__projectIps

    def total(self) -> dict[str, dict[str, str]]:
        if self.__total is None or self.__flushTotal:
            self.__total = {}
            self.__flushTotal = False
            for _, ip in self.projectIps().items():
                self.__total.update(ip.total())
        return self.__total

    def total2(self) -> dict[str, dict[str, str]]:
        if self.__total2 is None or self.__flushTotal2:
            self.__total2 = {}
            self.__flushTotal2 = False
            for _, ip in self.projectIps().items():
                self.__total2.update(ip.total2())
        return self.__total2

    def iptr(self, name: str, key: str) -> str:
        if name in self.total():
            if key in self.total()[name]:
                return self.total()[name][key]
        return key

    def iptr2(self, name: str, key: str) -> str:
        if name in self.total2():
            if key in self.total2()[name]:
                return self.total2()[name][key]
        return key

    # noinspection PyUnusedLocal
    def __on_ip_totalChanged(self, name: str, key: str, old: str, new: str):
        self.total()[name][key] = new

    # noinspection PyUnusedLocal
    def __on_ip_total2Changed(self, name: str, key: str, old: str, new: str):
        self.total2()[name][key] = new


IP = Ip()
