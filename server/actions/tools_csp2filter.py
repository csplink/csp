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
# @file        tools_csp2filter.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-08     xqyjlj       initial version
#


import time

import jinja2
from coder.coder import Coder
from loguru import logger
from public.csp.ip import Ip
from utils.sys import SYS_UTILS

TYPE_MAP = {
    "boolean": "bool",
    "integer": "int",
    "string": "str",
}


def convert_type(name: str, t: str) -> str:
    """Convert raw type to Python type name."""
    if t == "enum":
        return f"_{name}_return_type"
    return TYPE_MAP.get(t, t)


def build_path(name: str, channel: bool) -> str:
    if channel:
        return f'f"{{instance}}.{{channel}}.{name}"'
    return f'f"{{instance}}.{name}"'


def merge_types(name: str, raw_types: list[str]) -> list[str] | str:
    """Merge multiple types into a final type list / single type."""
    unique = sorted(set(raw_types))
    mapped = [convert_type(name, t) for t in unique]
    return mapped if len(mapped) > 1 else mapped[0]


def process_parameter(name: str, parameter, channel: bool):
    """Process one parameter (may be conditional or direct)."""

    # --- Normalize conditional-list and non-list into a list of items ---
    items = parameter if isinstance(parameter, list) else [parameter]

    raw_types = []
    enum_values = []
    default = ""

    # --- Collect info from all items ---
    for item in items:
        t = item.content.type if isinstance(parameter, list) else item.type
        d = item.content.default if isinstance(parameter, list) else item.default

        raw_types.append(t)
        if not default:
            default = d

        if t == "enum":
            values = (
                item.content.values.keys()
                if isinstance(parameter, list)
                else item.values.keys()
            )
            enum_values.extend(values)

    # --- Build result ---
    result = {
        "default": default,
        "path": build_path(name, channel),
    }

    result_type = merge_types(name, raw_types)
    result["type"] = result_type

    # --- If type contains enum, add enum values ---
    if ("_" + name + "_return_type") in (
        result_type if isinstance(result_type, list) else [result_type]
    ):
        result["values"] = sorted(set(enum_values))

    return result


def generate(ip: Ip, channel: bool, pin: bool, output: str):
    parameters = {}

    for name, parameter in ip.parameters.items():
        parameters[name] = process_parameter(name, parameter, channel)

    data = {
        "instance": ip.name,
        "author": "csplink coder",
        "file": f"{ip.name.lower()}.py",
        "version": SYS_UTILS.version(),
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "year": time.strftime("%Y", time.localtime()),
        "parameters": parameters,
        "channel": channel,
        "pin": pin,
    }

    path = f"{output}/{ip.name.lower()}.py".replace("\\", "/")
    data["user_code"] = Coder.match_user(path, "# --<", "", "# -->", "")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(SYS_UTILS.templates_folder()),
    )

    env.add_extension("jinja2.ext.debug")
    env.add_extension("jinja2.ext.do")
    env.add_extension("jinja2.ext.loopcontrols")

    template = env.get_template("filter.py.j2")
    context = template.render({"CSP": data})

    logger.success(f"generate {path!r}.")

    with open(path, "w", encoding="utf-8") as f:
        f.write(context)


def action_tools_csp2filter(ip: Ip, channel: bool, pin: bool, output: str):
    generate(ip, channel, pin, output)
