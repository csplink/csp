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
# @file        tools_schema.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-19     xqyjlj       initial version
#

import json
from pathlib import Path

from loguru import logger
from ruamel.yaml import YAML


def action_tools_yaml2json(yaml_path: Path) -> bool:
    if yaml_path.is_dir():
        files = list(yaml_path.glob("*.yml"))
    elif yaml_path.is_file():
        files = [yaml_path]
    else:
        logger.error(f"Invalid path: {yaml_path!r}")
        return False

    for yaml_file in files:
        json_file = yaml_file.parent / f"{yaml_file.stem}.json"

        with open(yaml_file, "r", encoding="utf-8") as fp:
            yaml = YAML()
            yaml_data = yaml.load(fp)

        with open(json_file, "w", encoding="utf-8") as fp:
            json.dump(yaml_data, fp, indent=4, ensure_ascii=False)

        p = json_file.absolute().as_posix()
        logger.info(f"Updating {p!r}...")  # type: ignore

    return True
