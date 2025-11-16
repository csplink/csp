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
# @file        tools_cmx_ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-23     xqyjlj       initial version
#

import time
from pathlib import Path

from cmx.ip import CmxIp
from cmx.mcu import CmxMcu
from loguru import logger
from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import LiteralScalarString

__header = """# Licensed under the Apache License v. 2 (the "License")
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
# Copyright (C) {year}-{year} xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        {name}
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# {date}     xqyjlj       initial version
#

"""


def convert_multiline_strings(data):
    if isinstance(data, dict):
        for k, v in data.items():
            if isinstance(v, str) and "\n" in v:
                data[k] = LiteralScalarString(v)
            else:
                convert_multiline_strings(v)
    elif isinstance(data, list):
        for i, v in enumerate(data):
            if isinstance(v, str) and "\n" in v:
                data[i] = LiteralScalarString(v)
            else:
                convert_multiline_strings(v)


def action_tools_cmx_ip(src: str, mcu: str, dest: str, alias: str):
    cmx_mcu = CmxMcu(mcu)
    cmx_ip = CmxIp(src, alias, cmx_mcu)

    ip = cmx_ip.convert_ip()

    dest_file = Path(dest)
    if dest_file.exists():
        with open(dest_file, "r", encoding="utf-8") as f:
            yaml = YAML()
            config = yaml.load(f.read())
            if "diagrams" in config:
                ip["diagrams"] = config["diagrams"]
                activated = ip.pop("activated")
                ip["activated"] = activated

    with open(dest_file, "w", encoding="utf-8") as f:
        header = __header.format(
            year=time.strftime("%Y", time.localtime()),
            name=dest_file.name,
            date=time.strftime("%Y-%m-%d", time.localtime()),
        )

        f.write(header)
        yaml = YAML()
        yaml.width = 120
        yaml.indent(mapping=2, sequence=4, offset=2)
        convert_multiline_strings(ip)
        yaml.dump(ip, f)

    logger.success(f"Updating {dest_file!r}...")

    return True
