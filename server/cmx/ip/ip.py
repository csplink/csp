#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import re
import xml.etree.ElementTree as etree

from loguru import logger
from utils.express import Express

from ..mcu import CmxMcu
from .base import Base
from .mode_logic_operator1 import ModeLogicOperator1
from .parameter import Parameter
from .ref_mode import RefMode
from .ref_parameter import RefParameter
from .ref_signal import RefSignal
from .share import Share


class Ip(Base):

    def __init__(self, path: str, alias: str, mcu: CmxMcu):
        tree = etree.parse(path)
        root = tree.getroot()

        namespace = {"ns": root.tag.split("}")[0][1:] if "}" in root.tag else ""}
        tag = root.tag.split("}")[-1]

        assert tag == "IP", "invalid ip xml file"

        super().__init__(root, namespace)

        self.__alias = alias
        self.__mcu = mcu

        self.__ref_signals: dict[str, RefSignal] = {}
        for node in self._root.findall("ns:RefSignal", self._namespace):
            ref = RefSignal(node, namespace)
            self.__ref_signals[ref.name] = ref

        virtual_signals = []
        for ref in self.__ref_signals.values():
            if ref.virtual:
                virtual_signals.append(ref.name)

        share = Share(self.name, alias, mcu, virtual_signals)

        self.__ref_parameters: dict[str, list[RefParameter]] = {}
        for node in self._root.findall("ns:RefParameter", self._namespace):
            name = node.attrib.get("Name", "")
            ref = RefParameter(node, self._namespace, share)
            if name not in self.__ref_parameters:
                self.__ref_parameters[name] = [ref]
            else:
                self.__ref_parameters[name].append(ref)

        self.__ref_modes: dict[str, list[RefMode]] = {}
        for node in self._root.findall("ns:RefMode", self._namespace):
            name = node.attrib.get("Name", "")
            ref = RefMode(node, self._namespace, share)
            if ref.always_false:  # 永远为假，代表预处理阶段就可以舍弃了
                logger.trace(f"ref mode {ref.id!r} is always false, so ignore it")
                continue
            if name not in self.__ref_modes:
                self.__ref_modes[name] = [ref]
            else:
                current = self.__ref_modes[name][0]

                # 永远为真，代表预处理阶段就可以只选用这个节点了
                if current.always_true:
                    logger.trace(
                        f"ref mode {current.id!r} is always true, so ignore {ref.id!r}"
                    )
                    continue
                if ref.always_true:
                    logger.trace(
                        f"ref mode {ref.id!r} is always true, so ignore {current.id!r} and use {ref.id!r} instead"
                    )
                    self.__ref_modes[name] = [ref]
                    continue
                self.__ref_modes[name].append(ref)

        self.__mode_logic_operators: list[ModeLogicOperator1] = []
        for node in self._root.findall("ns:ModeLogicOperator", self._namespace):
            self.__mode_logic_operators.append(
                ModeLogicOperator1(node, self._namespace, share)
            )

        self._check_mode_logic_operator()
        self._inherit_ref_modes()
        self.__used_parameter_names = self._build_used_parameter_names()
        self.__semaphore_dictionary = self._build_semaphore_dictionary()
        self.__parameter_dictionary = self._build_parameter_dictionary()

    @property
    def alias(self) -> str:
        return self.__alias

    @property
    def mcu(self) -> CmxMcu:
        return self.__mcu

    @property
    def db_version(self) -> str:
        return self._root.attrib["DBVersion"]

    @property
    def name(self) -> str:
        return self._root.attrib["Name"]

    @property
    def label(self) -> str:
        return self.alias or self.name

    @property
    def version(self) -> str:
        return self._root.attrib["Version"]

    @property
    def ip_type(self) -> str:
        return self._get_str_attr("IPType")

    @property
    def ip_group(self) -> str:
        return self._get_str_attr("IpGroup")

    @property
    def ref_parameters(self) -> dict[str, list[RefParameter]]:
        return self.__ref_parameters

    @property
    def ref_modes(self) -> dict[str, list[RefMode]]:
        return self.__ref_modes

    @property
    def mode_logic_operators(self) -> list[ModeLogicOperator1]:
        return self.__mode_logic_operators

    @property
    def used_parameter_names(self) -> list[str]:
        return self.__used_parameter_names

    @property
    def ref_signals(self) -> dict[str, RefSignal]:
        return self.__ref_signals

    @property
    def semaphore_dictionary(self) -> dict[str, dict[str, str]]:
        return self.__semaphore_dictionary

    @property
    def parameter_dictionary(self) -> dict[str, dict[str, str]]:
        return self.__parameter_dictionary

    def _check_mode_logic_operator(self):
        if len(self.mode_logic_operators) == 0:
            return  # 适用于GPIO, NVIC 等 IP
        assert (
            len(self.mode_logic_operators) == 1
        ), "only support one mode logic operator"
        mode_logic_operator = self.mode_logic_operators[0]
        assert mode_logic_operator.name == "OR", "only support OR mode logic operator"

        for mode1 in mode_logic_operator.modes.values():
            if len(mode1.mode_logic_operator) == 0:
                continue
            assert (
                len(mode1.mode_logic_operator) == 1
            ), "only support one mode logic operator"
            assert mode_logic_operator.name in [
                "OR",
                "XOR",
            ], "only support OR or XOR mode logic operator"

            for mode2 in mode1.mode_logic_operator[0].modes.values():
                assert (
                    len(mode2.signal_logical_ops) <= 1
                ), "only support one signal logical op"

    def _inherit_ref_modes(self):
        for name, ref_modes in self.ref_modes.items():
            for ref_mode in ref_modes:
                if ref_mode.base_mode:
                    ref = self.ref_modes[ref_mode.base_mode]
                    assert len(ref) == 1, "only support one ref mode."
                    ref_mode.set_base_mode_obj(ref[0])

    def _build_used_parameter_names(self) -> list[str]:
        used_parameter_names: list[str] = []
        for _, ref_modes in self.ref_modes.items():
            for ref_mode in ref_modes:
                used_parameter_names += ref_mode.parameters.keys()

        used_parameter_names = sorted(set(used_parameter_names))
        result: list[str] = []
        if self.name == "GPIO":
            exclude = ["GPIOx", "GPIO_Pin"]
            result = [n for n in used_parameter_names if n not in exclude]
        else:
            result = used_parameter_names

        return result

    def _build_semaphore_dictionary(self) -> dict[str, dict[str, str]]:
        """
        用于从 ref_mode 的 semaphores 生成 提取表达式，semaphores表现为bool
        """
        temp = {}
        if len(self.mode_logic_operators) == 0:
            return temp  # 适用于GPIO, NVIC 等 IP
        mode_logic_operator = self.mode_logic_operators[0]
        for name1, mode1 in mode_logic_operator.modes.items():
            label = self._converter_parameter_name(name1, self.label)
            for name2, mode2 in mode1.mode_logic_operator[0].modes.items():
                for semaphore in mode2.semaphores:
                    if mode1.type == "boolean":  # boolean
                        expression = f"configs.${{IP_INSTANCE}}.{label}"
                    else:
                        name = self._converter_value_name(name2)
                        expression = f"configs.${{IP_INSTANCE}}.{label} == '{name}'"
                    if semaphore not in temp:
                        should_remove = mode1.should_remove or mode2.should_remove
                        temp[semaphore] = {
                            "should_remove": should_remove,
                            "expression": [expression],
                        }
                    else:
                        temp[semaphore]["expression"].append(expression)
            for semaphore in mode1.semaphores:
                logger.warning(f"TODO: semaphore {semaphore!r}")

        result = {}
        for semaphore, item in temp.items():
            expressions = [f"({expression})" for expression in item["expression"]]
            result[semaphore] = {
                "should_remove": item["should_remove"],
                "expression": " or ".join(expressions),
            }

        return result

    def _build_parameter_dictionary(self) -> dict[str, dict[str, str]]:
        """
        用于从 parameter 和 values 提取表达式
        """
        result = {}

        for name, ref_parameters in self.ref_parameters.items():
            assert name not in result, f"name conflict: {name}"

            p_name = self._converter_parameter_name(name, self.label)
            if self.name == "GPIO":
                if name == "PinState":
                    p_name = self._converter_parameter_name("GPIO_State", self.label)
                elif name == "GPIO_PuPd":
                    p_name = self._converter_parameter_name("GPIO_Pull", self.label)

            result[name] = {
                "name": p_name,
                "expression": f"configs.${{IP_INSTANCE}}.{p_name}",
            }
            map = {}
            for ref_parameter in ref_parameters:
                for n, possible_value in ref_parameter.possible_values.items():
                    key = self._converter_value_name(n)
                    if n in map:
                        assert key == map[n], "The name should remain the same."
                    else:
                        map[n] = key
            keys = [f"{n}" for n in map.values()]
            prefix = Express.find_common_prefix(keys)
            for k, v in map.items():
                map[k] = v.replace(prefix, "", 1)
            map = self._beautify_prescaler_values(name, map)

            for k, v in map.items():
                if k in result:
                    assert (
                        v == result[k]["name"]
                    ), f"The name {k!r} should remain the same."
                else:
                    result[k] = {"name": v, "expression": f"'{v}'"}
        if len(self.mode_logic_operators) == 0:
            return result  # 适用于GPIO, NVIC 等 IP
        mode_logic_operator = self.mode_logic_operators[0]
        for name1, mode1 in mode_logic_operator.modes.items():
            if name1.startswith(f"Ctrl_{self.name}_"):
                key = name1.replace(f"{self.name}_", "", 1)
            else:
                key = name1
            label = self._converter_parameter_name(key, self.label)
            assert name1 not in result, f"name conflict: {name1}"
            result[name1] = {
                "name": label,
                "expression": f"configs.${{IP_INSTANCE}}.{label}",
            }
            if mode1.type == "boolean":  # boolean
                continue
            for name2, mode2 in mode1.mode_logic_operator[0].modes.items():
                v = self._converter_value_name(name2)
                if name2 in result:
                    assert (
                        v == result[name2]["name"]
                    ), f"The name {name2!r} should remain the same."
                else:
                    result[name2] = {"name": v, "expression": f"'{v}'"}

        return result

    def _beautify_prescaler_values(
        self, name: str, values: dict[str, str]
    ) -> dict[str, str]:
        """
        用于格式化 prescaler类型的values，加上前缀 "/"
        """
        name = self._converter_value_name(name)
        if "prescaler" not in name:
            return values

        for k, v in values.items():
            if not v.isdigit():
                return values

        for k, v in values.items():
            v = f"/{v}"
            values[k] = v

        return values

    def _converter_parameter_name(self, name: str, prefix: str) -> str:
        prefix = prefix.lower()
        name = re.sub(r"[^a-zA-Z0-9]", "_", name).replace("__", "_").strip().strip("_")
        name = Express.camel_to_snake(name)
        if not name.startswith(f"{prefix}_"):
            return f"{prefix}_{name}_t"
        else:
            return f"{name}_t"

    def _converter_value_name(self, name: str) -> str:
        name = re.sub(r"[^a-zA-Z0-9]", "_", name).replace("__", "_").strip().strip("_")
        name = Express.camel_to_snake(name)
        return name

    def _build_i18n_object(self, string: str) -> dict:
        return {"zh-cn": string, "en": string}

    def _converter_symbol(self, symbol: str, name: str) -> str:
        symbol = symbol.replace("=#", "")
        symbol = self._converter_parameter_name(symbol, name)
        return f"configs.${{IP_INSTANCE}}.{symbol}"

    def _is_gpio_child_parameter(self, ref: RefParameter, name: str) -> bool:
        if name == "GPIO_Pu":
            if ref.name == "GPIO_PuPd":
                return False
            elif ref.name == "GPIO_Pu":
                return True

        if ref.name.startswith(name) and ref.name != name:
            parent = self.ref_parameters[name][0]
            assert all(
                x in parent.possible_values.keys() for x in ref.possible_values.keys()
            ), "The possible values of the child parameter should be a subset of the possible values of the parent parameter."
            return True

        return False

    def _build_ref_parameters(self, ref_parameter: RefParameter) -> list | dict:
        result = {}

        if self.name == "GPIO":
            if self._is_gpio_child_parameter(ref_parameter, "GPIO_Mode"):
                return result
            elif self._is_gpio_child_parameter(ref_parameter, "GPIO_Speed"):
                return result
            elif self._is_gpio_child_parameter(ref_parameter, "GPIO_Pu"):
                return result

        if ref_parameter.type in ["integer", "double"]:
            if ref_parameter.type == "integer":
                result["type"] = "integer"
            else:
                result["type"] = "float"
            default = ref_parameter.default_value
            if not default.isdigit():
                default = "0"
            result["default"] = int(default)
            if ref_parameter.max is not None:
                result["max"] = (
                    self._converter_symbol(ref_parameter.max, self.label)
                    if isinstance(ref_parameter.max, str)
                    else int(ref_parameter.max)
                )
            if ref_parameter.min is not None:
                result["min"] = (
                    self._converter_symbol(ref_parameter.min, self.label)
                    if isinstance(ref_parameter.min, str)
                    else int(ref_parameter.min)
                )
        elif ref_parameter.type == "string":
            result["type"] = "string"
            result["default"] = ref_parameter.default_value
        elif ref_parameter.type in ["list", "uniqueElementList"]:
            result["type"] = "enum"
            values = {}
            for name, possible_value in ref_parameter.possible_values.items():
                comment = possible_value.comment
                label = self.parameter_dictionary[name]["name"]
                if label.startswith("/"):
                    comment = label
                values[label] = {"comment": {"zh-cn": comment, "en": comment}}
            result["values"] = values
            if len(values) == 0:
                return {}
            result["default"] = list(values.keys())[ref_parameter.default_value_index()]
        else:
            logger.warning(f"unknown type: {ref_parameter.type}")

        if "type" in result:
            result["display"] = self._build_i18n_object(ref_parameter.comment)
            result["description"] = self._build_i18n_object(
                ref_parameter.description or ref_parameter.comment
            )
            result["visible"] = ref_parameter.visible
            if "readonly" not in result:
                result["readonly"] = False

        return result

    def _build_ref_parameters_boolean(
        self, default: bool, display: str, description: str
    ) -> dict:
        result = {}

        result["type"] = "boolean"
        result["default"] = default
        result["display"] = self._build_i18n_object(display)
        result["description"] = self._build_i18n_object(description)
        result["visible"] = True
        result["readonly"] = False

        return result

    def _build_ref_parameters_enum(
        self, default: str, display: str, description: str, values: dict
    ) -> dict:
        result = {}

        result["type"] = "enum"
        result["values"] = values
        result["default"] = default
        result["display"] = self._build_i18n_object(display)
        result["description"] = self._build_i18n_object(description)
        result["visible"] = True
        result["readonly"] = False

        return result

    def _build_ref_modes_refs(self, parameter: Parameter) -> dict:
        result = {}
        if parameter.possible_values:
            values = []
            for name in parameter.possible_values:
                values.append(self.parameter_dictionary[name]["name"])
            result["values"] = values
            ref_parameters = self.ref_parameters[parameter.name]
            assert (
                len(ref_parameters) == 1
            ), "the ref parameters of the modes should be a single one."
            ref_parameter = ref_parameters[0]
            if ref_parameter.default_value in parameter.possible_values:
                default_value = ref_parameter.default_value
                default = self.parameter_dictionary[default_value]["name"]
            else:
                default = values[0]
            result["default"] = default
        return result

    def _build_expression(self, expression: str):
        expr = expression
        variables = Express.variables(expr)
        un_matched = []
        is_prebuilt = True
        for variable, props in variables.items():
            assert len(props) == 1, f"unknown expression: {expr}"
            prop = props[0]
            if prop == "lhs" or prop == "rhs":
                is_prebuilt = False
                if variable not in self.parameter_dictionary:
                    un_matched.append(variable)
                else:
                    v = self.parameter_dictionary[variable]["expression"]
                    expr = expr.replace(variable, v)
            elif prop == "bool":
                if variable not in self.semaphore_dictionary:
                    if Express.is_prebuilt_variable(variable):
                        if variable in self.mcu.context:
                            v = "(true)"
                        else:
                            v = "(false)"
                        expr = expr.replace(variable, v)
                    else:
                        is_prebuilt = False
                        un_matched.append(variable)
                else:
                    item = self.semaphore_dictionary[variable]
                    v = item["expression"]
                    if item["should_remove"]:
                        logger.trace(
                            f"variable {variable!r}({v!r}) is always false, so replace with false"
                        )
                        v = "(false)"
                    else:
                        is_prebuilt = False
                    expr = expr.replace(variable, v)
            else:
                un_matched.append(variable)
        if len(un_matched) > 0:
            logger.warning(
                f"unknown variables: {un_matched} in expression: {expression!r} -> {expr!r}"
            )
            condition = expression
        else:
            if is_prebuilt:
                status = Express.get_expression_status(
                    expr, {"false": False, "true": True}
                )
                if status == Express.Status.ALWAYS_TRUE:
                    expr = "true"
                elif status == Express.Status.ALWAYS_FALSE:
                    expr = "false"
            condition = expr
        return condition

    def _convert_parameters(self) -> dict:
        result = {}
        for name in self.used_parameter_names:
            key = self.parameter_dictionary[name]["name"]
            ref_parameters = self.ref_parameters[name]
            if len(ref_parameters) == 0:
                logger.warning(f"unknown parameter: {name}")
                continue
            elif len(ref_parameters) == 1:
                ref_parameters = ref_parameters[0]
                ref = self._build_ref_parameters(ref_parameters)
                if len(ref) > 0:  #
                    result[key] = ref
            elif len(ref_parameters) > 1:
                conditions = []
                force_content = None
                for ref_parameter in ref_parameters:
                    if ref_parameter.expression not in self.semaphore_dictionary:
                        if ref_parameter.expression not in ["default"]:
                            expression = self._build_expression(
                                ref_parameter.expression
                            )
                            # 值永远为真，那么其他值就没有意义了
                            if expression == "true":
                                logger.trace(
                                    f"ref parameter {ref_parameter.id!r} is always true, so ignore other values"
                                )
                                force_content = self._build_ref_parameters(
                                    ref_parameter
                                )
                            # 值永远为假，没有意义
                            elif expression == "false":
                                logger.trace(
                                    f"ref parameter {ref_parameter.id!r} is always false, so ignore"
                                )
                                continue
                            condition = expression
                        else:
                            condition = ref_parameter.expression
                    else:
                        item = self.semaphore_dictionary[ref_parameter.expression]
                        if item["should_remove"]:
                            logger.trace(
                                f"ref parameter {ref_parameter.id!r} is always false, so ignore"
                            )
                            continue
                        condition = item["expression"]
                    condition = Express.convert_expr_op(condition)
                    ref = self._build_ref_parameters(ref_parameter)
                    if ref:
                        conditions.append(
                            {
                                "condition": condition,
                                "content": ref,
                            }
                        )

                if force_content:
                    result[key] = force_content
                else:
                    if len(conditions) == 0:
                        logger.warning(f"unknown parameter: {name}")
                        continue
                    elif len(conditions) == 1:
                        result[key] = conditions[0]["content"]
                    else:
                        result[key] = conditions
        if len(self.mode_logic_operators) == 0:
            return result  # 适用于GPIO, NVIC 等 IP
        mode_logic_operator = self.mode_logic_operators[0]

        for name1, mode1 in mode_logic_operator.modes.items():
            if len(mode1.mode_logic_operator) == 0:
                continue
            if mode1.should_remove:
                continue
            operator = mode1.mode_logic_operator[0]
            name = self.parameter_dictionary[name1]["name"]
            if mode1.type == "boolean":  # boolean
                result[name] = self._build_ref_parameters_boolean(
                    False, mode1.label.upper(), mode1.label.upper()
                )
            else:  # enum
                values = {}
                for name2, mode2 in operator.modes.items():
                    label = name1[len("Ctrl_") :]
                    if mode2.should_remove:
                        logger.trace(
                            f"mode '{label}@{name2}' is always invalid, so ignore"
                        )
                        continue
                    elif not mode2.valid:
                        logger.trace(
                            f"mode '{label}@{name2}' signals is always invalid, so ignore"
                        )
                        continue
                    n = self.parameter_dictionary[name2]["name"]
                    values[n] = {"comment": self._build_i18n_object(mode2.label)}
                    if len(mode2.signal_logical_ops) > 0:
                        signals = {}
                        signal_logical_op = mode2.signal_logical_ops[0]
                        for signal_name in signal_logical_op.signals:
                            ref_signal = self.ref_signals[signal_name]
                            if not ref_signal.virtual:
                                k = f"${{IP_INSTANCE}}:{signal_name}"
                                signals[k] = {"mode": f"GPIO:{ref_signal.io_mode}"}
                        if len(signals) > 0:
                            values[n]["signals"] = signals
                if len(values) == 0:
                    continue
                if not mode1.remove_disable:
                    disable = {
                        "disable": {"comment": self._build_i18n_object("Disable")}
                    }
                    disable.update(values)
                    values = disable

                default = next(iter(values.keys()))
                result[name] = self._build_ref_parameters_enum(
                    default, mode1.label.upper(), mode1.label.upper(), values
                )

        return result

    def _convert_containers(self, parameters: dict) -> dict:
        result = {}
        modes = {}

        configurations = []
        mode_refs = {}

        if self.name == "GPIO":
            overviews = {}
            overview_refs = {}
            for name in parameters.keys():
                overview_refs[name] = {}
            overviews["refParameters"] = overview_refs
            result["overview"] = overviews
            return result

        if len(self.mode_logic_operators) == 0:
            return result  # 适用于GPIO, NVIC 等 IP

        mode_logic_operator = self.mode_logic_operators[0]
        for name1, mode1 in mode_logic_operator.modes.items():
            name = self.parameter_dictionary[name1]["name"]
            if name not in parameters:
                continue
            mode_ref = {}
            if len(mode1.conditions) > 0:
                expression = self._build_expression(mode1.expression)
                # 值永远为真，那么其他值就没有意义了
                if expression == "true":
                    logger.trace(f"mode {mode1.name!r} is always true, so use it")
                # 值永远为假，没有意义
                elif expression == "false":
                    logger.trace(f"mode {mode1.name!r} is always false, so ignore")
                    continue
                else:
                    expression = Express.convert_expr_op(expression)
                    mode_ref["condition"] = expression

            mode_refs[name] = mode_ref
            if mode1.type == "boolean":  # boolean
                condition = self.parameter_dictionary[name1]["expression"]
                mode2 = next(iter(mode1.mode_logic_operator[0].modes.values()))
                name2 = mode2.name
                for mode_name, ref_modes in self.ref_modes.items():
                    ref_mode = ref_modes[0]
                    if mode2.should_remove:
                        continue
                    elif name2 != mode_name:
                        continue
                    refs = {}
                    for param, parameter in ref_mode.parameters.items():
                        l = self.parameter_dictionary[param]["name"]
                        refs[l] = self._build_ref_modes_refs(parameter)
                    configurations.append(
                        {
                            "condition": condition,
                            "content": {
                                "refParameters": refs,
                            },
                        }
                    )
            else:
                for name2, mode2 in mode1.mode_logic_operator[0].modes.items():
                    for mode_name, ref_modes in self.ref_modes.items():
                        ref_mode = ref_modes[0]
                        if len(ref_mode.parameters) == 0:
                            continue
                        elif mode2.should_remove:
                            continue
                        elif name2 != mode_name:
                            continue
                        value = self.parameter_dictionary[name2]["name"]
                        condition = f"configs.${{IP_INSTANCE}}.{name} == '{value}'"
                        refs = {}
                        for param, parameter in ref_mode.parameters.items():
                            l = self.parameter_dictionary[param]["name"]
                            refs[l] = self._build_ref_modes_refs(parameter)
                        configurations.append(
                            {
                                "condition": condition,
                                "content": {
                                    "refParameters": refs,
                                },
                            }
                        )

        modes["refParameters"] = mode_refs

        result["modes"] = modes
        result["configurations"] = configurations
        return result

    def _convert_activated(self, parameters: dict) -> str:
        result: list[str] = []
        boolean_expression = []
        enum_expression = []

        if self.name == "GPIO":
            return f"not is_empty(configs.{self.label})"

        if len(self.mode_logic_operators) == 0:
            return "true"

        mode_logic_operator = self.mode_logic_operators[0]
        for name1, mode1 in mode_logic_operator.modes.items():
            name = self.parameter_dictionary[name1]["name"]
            if name not in parameters:
                continue
            if mode1.type == "boolean":  # boolean
                boolean_expression.append(f"(configs.${{IP_INSTANCE}}.{name})")
            else:
                mode2 = next(iter(mode1.mode_logic_operator[0].modes.values()))
                value = self.parameter_dictionary[mode2.name]["name"]
                if mode2.remove_disable:
                    enum_expression.append(
                        f"(configs.${{IP_INSTANCE}}.{name} != '{value}')"
                    )
                else:
                    enum_expression.append(
                        f"(configs.${{IP_INSTANCE}}.{name} != 'disable')"
                    )

        result.extend(boolean_expression)
        result.extend(enum_expression)

        if self.name in ["SYS"]:
            return "true"

        return " or ".join(result or ["true"])

    def __convert_gpio_presets(self, parameters: dict) -> dict:
        presets = {}

        def _is_gpio_child(name: str, key: str) -> bool:
            if key == "GPIO_Pu":
                if name == "GPIO_PuPd":
                    return False
                elif name == "GPIO_Pu":
                    return True

            if name.startswith(key) and name != key:
                return True
            return False

        for mode_name, ref_modes in self.ref_modes.items():
            if mode_name in ["GPIO"]:
                continue
            ref_mode = ref_modes[0]
            refs = {}
            for parameter_name, parameter in ref_mode.parameters.items():
                parameter_key = self.parameter_dictionary[parameter_name]["name"]
                if parameter_key not in parameters:
                    if _is_gpio_child(parameter_name, "GPIO_Mode"):
                        parent_ref_parameter = self.ref_parameters["GPIO_Mode"][0]
                        parameter_key = self.parameter_dictionary["GPIO_Mode"]["name"]
                    elif _is_gpio_child(parameter_name, "GPIO_Speed"):
                        parent_ref_parameter = self.ref_parameters["GPIO_Speed"][0]
                        parameter_key = self.parameter_dictionary["GPIO_Speed"]["name"]
                    elif _is_gpio_child(parameter_name, "GPIO_Pu"):
                        parent_ref_parameter = self.ref_parameters["GPIO_PuPd"][0]
                        parameter_key = self.parameter_dictionary["GPIO_PuPd"]["name"]
                    else:
                        continue

                    ref_parameter = self.ref_parameters[parameter_name][0]
                    ref_parameter_keys = ref_parameter.possible_values.keys()
                    parent_ref_parameter_keys = (
                        parent_ref_parameter.possible_values.keys()
                    )
                    default_value = ref_parameter.default_value
                    if len(parameter.possible_values) > 0:
                        refs[parameter_key] = self._build_ref_modes_refs(parameter)
                    else:
                        if set(ref_parameter_keys) == set(parent_ref_parameter_keys):
                            if parent_ref_parameter.default_value == default_value:
                                refs[parameter_key] = {}
                            else:
                                assert (
                                    default_value in parent_ref_parameter_keys
                                ), "The default value should be in the possible values of the ref parameter."
                                default = self.parameter_dictionary[default_value][
                                    "name"
                                ]
                                refs[parameter_key] = {"default": default}
                        else:
                            values = []
                            for key in ref_parameter_keys:
                                values.append(self.parameter_dictionary[key]["name"])
                            default = self.parameter_dictionary[default_value]["name"]
                            refs[parameter_key] = {"values": values, "default": default}
                else:
                    refs[parameter_key] = self._build_ref_modes_refs(parameter)
            presets[mode_name] = {
                "refParameters": refs,
            }

        return presets

    def convert_ip(self) -> dict:
        result = {}

        parameters = self._convert_parameters()
        result["name"] = self.label.upper()
        result["parameters"] = parameters
        if self.name == "GPIO":
            result["presets"] = self.__convert_gpio_presets(parameters)

        result["containers"] = self._convert_containers(parameters)
        result["activated"] = self._convert_activated(parameters)

        logger.info(f"Find {len(result['parameters'])} parameters")

        return result
