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


def _getCondition(expr: str, cls) -> str:
    expr = expr.replace("${INSTANCE}", cls.instance())
    return expr


class IpType(QObject):
    parameterItemUpdated = Signal(list)
    controlsUpdated = Signal()
    modesUpdated = Signal()
    controlsItemUpdated = Signal(str, bool)
    modesItemUpdated = Signal(str, bool)
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

            class SignalUnitType:
                def __init__(self, data: dict):
                    self.__data = data

                def __str__(self) -> str:
                    return json.dumps(self.__data, indent=2, ensure_ascii=False)

                @property
                def origin(self) -> dict:
                    return self.__data

                @property
                def mode(self) -> str:
                    return self.__data.get("mode", "")

            def __init__(self, data: dict):
                self.__data = data

                self.__comment = None
                self.__expression = None
                self.__signals = None

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

            @property
            def signals(self) -> dict[str, SignalUnitType]:
                if self.__signals is None:
                    self.__signals = {}
                    for name, value in self.__data.get("signals", {}).items():
                        self.__signals[name] = self.SignalUnitType(value)
                return self.__signals

        def __init__(self, data: dict, parent: IpType | None):
            self.__data = data

            self.__parent = parent
            self.__display = None
            self.__description = None
            self.__values = None
            self.__expression = None
            self.__signals = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        # region getter/setter

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
        def default(self) -> str | float | int | bool:
            return self.__data.get("default", "")

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
            value = self.__data.get("max", -1)
            if isinstance(value, str):
                value = Express.floatExpr(
                    value.replace("${INSTANCE}", self.instance()),
                    VALUE_HUB.values(),
                    {},
                )
            return value

        @property
        def min(self) -> float:
            value = self.__data.get("min", -1)
            if isinstance(value, str):
                value = Express.floatExpr(
                    value.replace("${INSTANCE}", self.instance()),
                    VALUE_HUB.values(),
                    {},
                )
            return value

        # endregion

        def parent(self) -> IpType | None:
            return self.__parent

        def instance(self) -> str:
            if self.__parent is None:
                return ""
            return self.__parent.instance()

        def signals(self) -> list[str]:
            if self.__signals is None:
                signals = []
                for _, value in self.values.items():
                    for name, _ in value.signals.items():
                        signals.append(_getCondition(name, self))
                self.__signals = sorted(set(signals))
            return self.__signals

    class ControlModeUnitType(QObject):
        conditionUpdated = Signal(bool)

        def __init__(
            self,
            data: dict,
            name: str,
            parameters: dict[str, IpType.ParameterUnitType],
            parent: IpType | None,
        ):
            super().__init__(parent)
            self.__data = data
            self.__name = name
            self.__parameters = parameters
            self.__parent = parent
            self.__conditionOrigin = None
            self.__condition = None
            self.__dependencies = None
            self.__enabled = False
            VALUE_HUB.itemUpdated.connect(self.__on_valueHub_itemUpdated)

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        # region getter/setter

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
        def default(self) -> str | float | int | bool:
            default = self.__data.get("default")
            if default is None:
                default = self.__parameters[self.__name].default
            return default

        @property
        def _condition(self) -> str:
            if self.__conditionOrigin is None:
                self.__conditionOrigin = self.__data.get("condition", "True")
                self.__conditionOrigin = _getCondition(self.__conditionOrigin, self)
            return self.__conditionOrigin

        @property
        def condition(self) -> bool:
            if self.__condition is None:
                self.__condition = Express.boolExpr(self._condition, VALUE_HUB.values())
            return self.__condition

        # endregion

        def instance(self) -> str:
            if self.__parent is None:
                return ""
            return self.__parent.instance()

        def dependencies(self) -> list[str]:
            if self.__dependencies is None:
                self.__dependencies = Express.variables(self._condition)
            return self.__dependencies

        def setEnabled(self, enabled: bool):
            self.__enabled = enabled

        def enabled(self) -> bool:
            return self.__enabled

        def __on_valueHub_itemUpdated(self, keys: list[str], old: object, new: object):
            key = ".".join(keys)

            if key in self.dependencies():
                self.__condition = Express.boolExpr(self._condition, VALUE_HUB.values())
                if self.enabled():
                    self.conditionUpdated.emit(self.__condition)

    class ConditionUnitType:

        def __init__(self, data: dict, parent: IpType | None):
            self.__data = data

            self.__parent = parent
            self.__condition = None
            self.__content = None
            self.__userData = None
            self.__dependencies = None

        def __str__(self) -> str:
            return json.dumps(self.__userData, indent=2, ensure_ascii=False)

        # region getter/setter

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def _condition(self) -> str:
            if self.__condition is None:
                self.__condition = self.__data.get("condition", "True")
                self.__condition = _getCondition(self.__condition, self)
            return self.__condition

        @property
        def condition(self) -> bool:
            return Express.boolExpr(self._condition, VALUE_HUB.values())

        @property
        def content(self) -> dict:
            if self.__content is None:
                self.__content = self.__data.get("content", {})
            return self.__content

        # endregion

        def parent(self) -> IpType | None:
            return self.__parent

        def instance(self) -> str:
            if self.__parent is None:
                return ""
            return self.__parent.instance()

        def dependencies(self) -> list[str]:
            if self.__dependencies is None:
                self.__dependencies = Express.variables(self._condition)
            return self.__dependencies

        def setUserData(self, data):
            self.__userData = data

        def userData(self):
            return self.__userData

    class PinGroupUnitType(QObject):
        def __init__(self, data: dict, parent: IpType | None):
            super().__init__(parent)
            self.__data = data

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        # region getter/setter

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def default(self) -> bool:
            return self.__data.get("default", False)

        # endregion

    def __init__(self, data: dict, instance="", parent=None):
        super().__init__(parent)
        self.__data = data
        self.__parameters = None
        self.__controls = None
        self.__pinModes = None
        self.__modes = None
        self.__pinGroups = None
        self.__activated = None
        self.__instance = instance

        # ----------------------------------------------------------------------

        self.__parametersConditions: dict[str, list[IpType.ConditionUnitType]] = {}
        self.__parametersDependencies: dict[str, list[str]] = {}

        self.__controlsConditions: list[IpType.ConditionUnitType] = []
        self.__controlsDependencies: list[str] = []

        self.__modesConditions: list[IpType.ConditionUnitType] = []
        self.__modesDependencies: list[str] = []

        self.__signals = []

        self.__total = None
        self.__total2 = None

        VALUE_HUB.itemUpdated.connect(self.__on_valueHub_itemUpdated)

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    # region getter/setter

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def parameters(self) -> dict[str, ParameterUnitType]:
        if self.__parameters is None:
            self.__parameters = {}
            signals = []
            for name, param in self.__data.get("parameters", {}).items():
                if isinstance(param, dict):
                    parameter = IpType.ParameterUnitType(param, self)
                    self.__parameters[name] = parameter
                    signals.extend(parameter.signals())
                elif isinstance(param, list):
                    params: list[dict] = param
                    value = None
                    default = IpType.ParameterUnitType({}, self)
                    conditions: list[IpType.ConditionUnitType] = []
                    dependencies = []
                    for v in params:
                        conditionUnit = IpType.ConditionUnitType(v, self)
                        _condition = conditionUnit._condition
                        condition = conditionUnit.condition
                        unit = IpType.ParameterUnitType(conditionUnit.content, self)
                        signals.extend(unit.signals())
                        conditionUnit.setUserData(unit)
                        if _condition == "default":
                            default = unit
                        else:
                            if condition:
                                value = unit
                        conditions.append(conditionUnit)
                        dependencies += conditionUnit.dependencies()

                    self.__parametersConditions[name] = conditions
                    self.__parametersDependencies[name] = sorted(set(dependencies))

                    if value is None:
                        value = default

                    self.__parameters[name] = value
                else:
                    logger.error(f"Invalid parameter type: {name}")
            self.__signals = sorted(set(signals))
        return self.__parameters

    @property
    def controls(self) -> dict[str, ControlModeUnitType]:
        if self.__controls is None:
            controls, conditions, dependencies = self.__converterControlModeConditions(
                "controls"
            )
            self.__controls = controls
            self.__controlsConditions = conditions
            self.__controlsDependencies = dependencies
        return self.__controls

    @property
    def pinModes(self) -> dict[str, dict[str, ControlModeUnitType]]:
        if self.__pinModes is None:
            self.__pinModes = {}
            for name, modeItem in self.__data.get("pinModes", {}).items():
                self.__pinModes[name] = {}
                for modeName, mode in modeItem.items():
                    self.__pinModes[name][modeName] = IpType.ControlModeUnitType(
                        mode, modeName, self.parameters, self
                    )
        return self.__pinModes

    @property
    def modes(self) -> dict[str, ControlModeUnitType]:
        if self.__modes is None:
            modes, conditions, dependencies = self.__converterControlModeConditions(
                "modes"
            )
            self.__modes = modes
            self.__modesConditions = conditions
            self.__modesDependencies = dependencies
        return self.__modes

    @property
    def pinGroups(self) -> dict[str, dict[str, dict[str, PinGroupUnitType]]]:
        # pin:signal:group:unit
        if self.__pinGroups is None:
            self.__pinGroups = {}
            for pinName, signalItem in self.__data.get("pinGroups", {}).items():
                pin = {}
                for signalName, groupItem in signalItem.items():
                    signal = {}
                    for groupName, unit in groupItem.items():
                        signal[groupName] = IpType.PinGroupUnitType(unit, self)
                    pin[signalName] = signal
                self.__pinGroups[pinName] = pin
        return self.__pinGroups

    @property
    def _activated(self) -> str:
        if self.__activated is None:
            self.__activated = self.__data.get("activated", "True")
            self.__activated = _getCondition(self.__activated, self)
        return self.__activated

    @property
    def activated(self) -> bool:
        return Express.boolExpr(self._activated, VALUE_HUB.values())

    # endregion

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

    def instance(self) -> str:
        return self.__instance

    def findPinGroups(self, name: str, signal: str) -> dict[str, PinGroupUnitType]:
        results = {}
        if name in self.pinGroups:
            if signal in self.pinGroups[name]:
                results = self.pinGroups[name][signal]
        return results

    def signals(self) -> list[str]:
        if not self.__signals:
            self.parameters  # initialize
        return self.__signals

    def _parametersConditions(self) -> dict[str, list[IpType.ConditionUnitType]]:
        if not self.__parametersConditions:
            self.parameters  # initialize
        return self.__parametersConditions

    def _controlsConditions(self) -> list[IpType.ConditionUnitType]:
        if not self.__controlsConditions:
            self.controls  # initialize
        return self.__controlsConditions

    def _modesConditions(self) -> list[IpType.ConditionUnitType]:
        if not self.__modesConditions:
            self.modes  # initialize
        return self.__modesConditions

    def __on_valueHub_itemUpdated(self, keys: list[str], old: object, new: object):
        key = ".".join(keys)

        # update parameters with conditions
        parametersNames = []
        for name, conditions in self._parametersConditions().items():
            default = self.parameters[name]
            value = None
            dependencies: list[str] = self.__parametersDependencies[name]
            if key not in dependencies:
                continue

            for conditionUnit in conditions:
                if conditionUnit._condition == "default":
                    default = conditionUnit.userData()
                    continue
                if conditionUnit.condition:
                    value = conditionUnit.userData()
                    break
            if value is None:
                value = default

            if self.parameters[name] != value:
                parametersNames.append(name)
                self.parameters[name] = value  # type: ignore
        if len(parametersNames) > 0:
            self.__flushI18n(parametersNames)
            self.parameterItemUpdated.emit(parametersNames)

        # update controls with conditions
        controlsChanged = False
        if key in self.__controlsDependencies:
            default = self.controls
            value = None
            for conditionUnit in self._controlsConditions():
                if conditionUnit._condition == "default":
                    default = conditionUnit.userData()
                    continue
                if conditionUnit.condition:
                    value = conditionUnit.userData()
                    break
            if value is None:
                value = default

            if self.__controls != value:
                controlsChanged = True

                for name, item in self.__controls.items():  # type: ignore
                    item.setEnabled(False)

                for name, item in value.items():  # type: ignore
                    item.setEnabled(True)

                self.__controls = value

        if controlsChanged:
            self.controlsUpdated.emit()

        # update modes with conditions
        modesChanged = False
        if key in self.__modesDependencies:
            default = self.modes
            value = None
            for conditionUnit in self._modesConditions():
                if conditionUnit._condition == "default":
                    default = conditionUnit.userData()
                    continue
                if conditionUnit.condition:
                    value = conditionUnit.userData()
                    break
            if value is None:
                value = default

            if self.__modes != value:
                modesChanged = True

                for name, item in self.__modes.items():  # type: ignore
                    item.setEnabled(False)

                for name, item in value.items():  # type: ignore
                    item.setEnabled(True)

                self.__modes = value
        if modesChanged:
            self.modesUpdated.emit()

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

    def __converterControlModeConditions(self, property: str) -> tuple[
        dict[str, IpType.ControlModeUnitType],
        list[IpType.ConditionUnitType],
        list[str],
    ]:
        results: dict[str, IpType.ControlModeUnitType] = {}
        conditions: list[IpType.ConditionUnitType] = []
        dependencies: list[str] = []
        content = self.__data.get(property, {})
        if isinstance(content, dict):
            for name, item in content.items():
                results[name] = IpType.ControlModeUnitType(
                    item, name, self.parameters, self
                )
                if property == "controls":
                    results[name].conditionUpdated.connect(
                        lambda x: self.controlsItemUpdated.emit(name, x)
                    )
                else:
                    results[name].conditionUpdated.connect(
                        lambda x: self.modesItemUpdated.emit(name, x)
                    )
        elif isinstance(content, list):
            params: list[dict[str, dict]] = content
            value = None
            default = {}
            for v in params:
                conditionUnit = IpType.ConditionUnitType(v, self)
                _condition = conditionUnit._condition
                condition = conditionUnit.condition

                unit = {}
                for name, item in conditionUnit.content.items():
                    i = IpType.ControlModeUnitType(item, name, self.parameters, self)
                    if property == "controls":
                        i.conditionUpdated.connect(
                            lambda x: self.controlsItemUpdated.emit(name, x)
                        )
                    else:
                        i.conditionUpdated.connect(
                            lambda x: self.modesItemUpdated.emit(name, x)
                        )
                    unit[name] = i

                conditionUnit.setUserData(unit)
                if _condition == "default":
                    default = unit
                else:
                    if condition:
                        value = unit
                conditions.append(conditionUnit)
                dependencies += conditionUnit.dependencies()

            dependencies = sorted(set(dependencies))

            if value is None:
                value = default

            results = value
        else:
            logger.error(f"Invalid {property!r} type: {type(content)!r}")

        for name, item in results.items():
            item.setEnabled(True)

        return results, conditions, dependencies


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
    def __getIp(self, vendor: str, instance: str, name: str) -> IpType:
        file = os.path.join(
            SETTINGS.DATABASE_FOLDER, "ip", vendor.lower(), f"{name.lower()}.yml"
        )
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                ip = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkIp(ip)
            if succeed:
                return IpType(ip, instance, self)
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
        ip = self.__getIp(vendor, instance, name)
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
