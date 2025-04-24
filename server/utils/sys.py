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
# @file        sys.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-07     xqyjlj       initial version
#

import copy
import os
from pathlib import Path
import sys


class SysUtils:
    def __init__(self):
        self._sys_path = copy.deepcopy(sys.path)
        self._sys_path.append(f"{self.exe_folder()}/public")

    def sys_path(self) -> list[str]:
        return self._sys_path

    @staticmethod
    def exe_folder() -> str:
        """
        @brief      Get the folder of the executable file.
        @return     The folder of the executable file.
        @note       It is a static method.
        """
        return str(Path(sys.argv[0]).parent)

    @staticmethod
    def version() -> str:
        return "0.0.6"

    @staticmethod
    def resource_folder() -> str:
        return str(Path(SysUtils.exe_folder()).parent / "resources")

    @staticmethod
    def database_folder() -> str:
        return str(Path(SysUtils.resource_folder()) / "database")

    @staticmethod
    def templates_folder() -> str:
        return str(Path(SysUtils.resource_folder()) / "templates")


SYS_UTILS = SysUtils()
