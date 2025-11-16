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
# @file        tools_check_ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-09     xqyjlj       initial version
#

from dataclasses import dataclass
from typing import Optional

from loguru import logger
from public.csp.ip import Ip, Parameter, ParameterCondition


@dataclass
class CheckIssue:
    """检查问题（错误或警告）"""

    id: str  # 错误ID，如 "enum_default_not_in_values"
    name: str  # 参数/容器名称
    message: str  # 错误描述
    expected: Optional[str] = None  # 期望值
    actual: Optional[str] = None  # 实际值
    details: Optional[dict] = None  # 其他详细信息

    def __str__(self) -> str:
        """格式化输出"""
        parts = [f"'{self.name}'"]
        parts.append(self.message)

        if self.expected:
            parts.append(f"Expected: {self.expected}")
        if self.actual:
            parts.append(f"Actual: {self.actual}")

        return ": ".join(parts)


class IpChecker:
    """IP 配置检查器，提供详细的验证功能"""

    def __init__(self, ip: Ip):
        self.ip = ip
        self.errors: list[CheckIssue] = []
        self.warnings: list[CheckIssue] = []

    def check_parameter(self, param_name: str, param: Parameter) -> bool:
        """
        检查单个参数的有效性。

        Args:
            param_name: 参数名称
            param: 参数对象

        Returns:
            有效返回 True，否则返回 False
        """
        is_valid = True
        param_type = param.type
        default_value = param.default

        # 检查枚举类型
        if param_type == "enum":
            if param.values:
                # 检查默认值是否在 values 中
                if default_value not in param.values:
                    self.errors.append(
                        CheckIssue(
                            id="enum_default_not_in_values",
                            name=param_name,
                            message="default value not found in values",
                            expected=f"one of {list(param.values.keys())}",
                            actual=str(default_value),
                        )
                    )
                    is_valid = False
                else:
                    logger.trace(
                        f"[OK] Parameter '{param_name}': enum default '{default_value}' is valid"
                    )
            else:
                self.warnings.append(
                    CheckIssue(
                        id="enum_no_values_defined",
                        name=param_name,
                        message="enum type but no values defined",
                    )
                )

        # 检查整数类型
        elif param_type == "integer":
            try:
                default_int = int(default_value)
                max_val = param.max if param.max is not None else float("inf")
                min_val = param.min if param.min is not None else float("-inf")

                # 如果是字符串，将 max/min 转换为整数
                if isinstance(max_val, str):
                    max_val = int(max_val)
                if isinstance(min_val, str):
                    min_val = int(min_val)

                if not (min_val <= default_int <= max_val):
                    self.errors.append(
                        CheckIssue(
                            id="integer_out_of_range",
                            name=param_name,
                            message="default value out of range",
                            expected=f"[{min_val}, {max_val}]",
                            actual=str(default_int),
                        )
                    )
                    is_valid = False
                else:
                    logger.trace(
                        f"[OK] Parameter '{param_name}': integer default {default_int} "
                        f"is in range [{min_val}, {max_val}]"
                    )
            except (ValueError, TypeError) as e:
                self.errors.append(
                    CheckIssue(
                        id="integer_invalid_value",
                        name=param_name,
                        message="invalid integer default value",
                        actual=str(default_value),
                        details={"error": str(e)},
                    )
                )
                is_valid = False

        # 检查浮点数类型
        elif param_type == "float":
            try:
                default_float = float(default_value)
                max_val = param.max if param.max is not None else float("inf")
                min_val = param.min if param.min is not None else float("-inf")

                # 如果是字符串，将 max/min 转换为浮点数
                if isinstance(max_val, str):
                    max_val = float(max_val)
                if isinstance(min_val, str):
                    min_val = float(min_val)

                if not (min_val <= default_float <= max_val):
                    self.errors.append(
                        CheckIssue(
                            id="float_out_of_range",
                            name=param_name,
                            message="default value out of range",
                            expected=f"[{min_val}, {max_val}]",
                            actual=str(default_float),
                        )
                    )
                    is_valid = False
                else:
                    logger.trace(
                        f"[OK] Parameter '{param_name}': float default {default_float} "
                        f"is in range [{min_val}, {max_val}]"
                    )
            except (ValueError, TypeError) as e:
                self.errors.append(
                    CheckIssue(
                        id="float_invalid_value",
                        name=param_name,
                        message="invalid float default value",
                        actual=str(default_value),
                        details={"error": str(e)},
                    )
                )
                is_valid = False

        # 检查布尔类型
        elif param_type == "boolean":
            if not isinstance(default_value, bool):
                if default_value not in ("true", "false", "True", "False", 0, 1):
                    self.errors.append(
                        CheckIssue(
                            id="boolean_invalid_value",
                            name=param_name,
                            message="invalid boolean default value",
                            expected="true, false, True, False, 0, or 1",
                            actual=str(default_value),
                        )
                    )
                    is_valid = False

        return is_valid

    def check_parameters(self) -> bool:
        """检查 IP 配置中的所有参数"""
        is_valid = True

        if not self.ip.parameters:
            self.warnings.append(
                CheckIssue(
                    id="no_parameters_defined",
                    name="IP",
                    message="No parameters defined in IP configuration",
                )
            )
            return True

        logger.info(f"Checking {len(self.ip.parameters)} parameters...")

        for param_name, param_data in self.ip.parameters.items():
            # 处理条件参数（列表）
            if isinstance(param_data, list):
                logger.trace(f"Checking conditional parameter '{param_name}'...")
                for idx, param_condition in enumerate(param_data):
                    if isinstance(param_condition, ParameterCondition):
                        if not self.check_parameter(
                            f"{param_name}[condition {idx}]", param_condition.content
                        ):
                            is_valid = False
            # 处理常规参数
            elif isinstance(param_data, Parameter):
                if not self.check_parameter(param_name, param_data):
                    is_valid = False

        return is_valid

    def check_containers(self) -> bool:
        """检查 containers 及其 refParameters"""
        is_valid = True

        if not self.ip.containers:
            return True

        # 获取所有参数名称用于验证
        param_names = set(self.ip.parameters.keys())

        containers_data = self.ip.containers.origin
        if not containers_data:
            return True

        logger.info("Checking containers refParameters...")

        # 检查每个容器类型
        for container_name in ["overview", "modes", "configurations", "clockTree"]:
            container = containers_data.get(container_name)
            if not container:
                continue

            # 处理列表（条件容器）
            if isinstance(container, list):
                for idx, item in enumerate(container):
                    ref_params = item.get("content", {}).get("refParameters", {})
                    for ref_param_name in ref_params.keys():
                        if ref_param_name not in param_names:
                            self.errors.append(
                                CheckIssue(
                                    id="ref_parameter_not_found",
                                    name=f"{container_name}[{idx}].refParameters",
                                    message=f"parameter '{ref_param_name}' not found in parameters",
                                    expected=f"parameter '{ref_param_name}' should be defined in parameters",
                                    actual=f"not found",
                                )
                            )
                            is_valid = False
                        else:
                            logger.trace(
                                f"[OK] Container '{container_name}[{idx}].refParameters': "
                                f"parameter '{ref_param_name}' exists"
                            )

            # 处理字典（普通容器）
            elif isinstance(container, dict):
                ref_params = container.get("refParameters", {})
                for ref_param_name in ref_params.keys():
                    if ref_param_name not in param_names:
                        self.errors.append(
                            CheckIssue(
                                id="ref_parameter_not_found",
                                name=f"{container_name}.refParameters",
                                message=f"parameter '{ref_param_name}' not found in parameters",
                                expected=f"parameter '{ref_param_name}' should be defined in parameters",
                                actual=f"not found",
                            )
                        )
                        is_valid = False
                    else:
                        logger.trace(
                            f"[OK] Container '{container_name}.refParameters': "
                            f"parameter '{ref_param_name}' exists"
                        )

        return is_valid

    def print_results(self):
        """打印详细的检查结果"""
        if self.warnings:
            logger.warning("[!] Warnings:")
            for warning in self.warnings:
                logger.warning(f"  - [{warning.id}] {warning}")

        if self.errors:
            logger.error("[x] Errors:")
            for error in self.errors:
                logger.error(f"  - [{error.id}] {error}")
        else:
            logger.success("[OK] All checks passed!")

        # 汇总
        if self.errors:
            logger.error(
                f"Summary: {len(self.errors)} error(s), {len(self.warnings)} warning(s)"
            )
        elif self.warnings:
            logger.warning(f"Summary: {len(self.warnings)} warning(s)")
        else:
            logger.success("Summary: No issues found")


def action_tools_check_ip(ip: Ip) -> bool:
    """
    检查 IP 配置的有效性。

    Args:
        ip: 要检查的 IP 对象

    Returns:
        所有检查通过返回 True，否则返回 False
    """
    if not ip.origin:
        return False

    checker = IpChecker(ip)

    # 运行所有检查
    param_valid = checker.check_parameters()
    container_valid = checker.check_containers()

    # 打印详细结果
    checker.print_results()

    return param_valid and container_valid
