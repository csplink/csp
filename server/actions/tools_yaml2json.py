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

import glob
import json
import os
from pathlib import Path

from loguru import logger
from ruamel.yaml import YAML


def action_tools_yaml2json(path: str) -> bool:
    if os.path.isdir(path):
        files = glob.glob(f"{path}/*.yml", recursive=False)
    elif os.path.isfile(path):
        files = [path]
    else:
        logger.error(f"Invalid path: {path!r}")
        return False

    for yaml_file in files:
        file = Path(yaml_file)
        json_file = file.parent / f"{file.stem}.json"

        with open(yaml_file, "r", encoding="utf-8") as fp:
            yaml = YAML()
            yaml_data = yaml.load(fp)

        with open(json_file, "w", encoding="utf-8") as fp:
            json.dump(yaml_data, fp, indent=4, ensure_ascii=False)

        p = str(json_file.absolute()).replace("\\", "/")
        logger.info(f"Updating {p!r}...")  # type: ignore

    return True
