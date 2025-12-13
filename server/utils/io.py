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
# @file        io.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-10     xqyjlj       initial version
#


import hashlib
import os
from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


class IoUtils:
    @staticmethod
    def readlines(path: str) -> list[str]:
        if not os.path.exists(path):
            return []
        with open(path, "r") as f:
            return f.readlines()

    @staticmethod
    def read_yaml(file: str) -> Any:
        with open(file, "r", encoding="utf-8") as f:
            yaml = YAML()
            return yaml.load(f.read())

    @staticmethod
    def sha1(file: Path) -> str:
        hash_sha1 = hashlib.sha1()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_sha1.update(chunk)
        return hash_sha1.hexdigest()


IO_UTILS = IoUtils()
