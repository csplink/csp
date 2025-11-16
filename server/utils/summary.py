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
# @file        summary.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-21     xqyjlj       initial version
#

import os

import jsonschema
from loguru import logger
from public.csp.summary import Summary
from ruamel.yaml import YAML

from .sys import SysUtils


class SummaryUtils:

    def __init__(self):
        pass

    @staticmethod
    @logger.catch(default=False)
    def __check_summary(summary: dict) -> bool:
        with open(
            os.path.join(SysUtils.database_folder(), "schema", "summary.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            yaml = YAML()
            schema = yaml.load(f.read())
            jsonschema.validate(instance=summary, schema=schema)
        return True

    @staticmethod
    @logger.catch(default=Summary({}))
    def load_summary(vendor: str, name: str) -> Summary:
        file = os.path.join(
            SysUtils.database_folder(), "summary", vendor, f"{name}.yml"
        )
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                yaml = YAML()
                summary = yaml.load(f.read())
                succeed = SummaryUtils.__check_summary(summary)
            if succeed:
                return Summary(summary)
            else:
                return Summary({})
        else:
            logger.error(f"{file} is not file!")
            return Summary({})
