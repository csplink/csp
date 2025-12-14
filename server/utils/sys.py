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


import sys
from pathlib import Path


class SysUtils:
    def __init__(self):
        if self.public_folder() not in sys.path:
            sys.path.append(self.public_folder())

    @staticmethod
    def exe_folder() -> str:
        """
        Get the directory where the program was launched from.

        This uses `sys.argv[0]`, which points to:
        - The script path when running in normal Python (`python script.py`)
        - The unpacked executable path when running a Nuitka --onefile binary

        Returns:
            str: The directory containing the launched executable or script.
        """
        return str(Path(sys.argv[0]).parent.absolute())

    @staticmethod
    def version() -> str:
        """
        @brief      Get the version of this software.
        @return     The version of this software.
        @note       It is a static method.
        """
        return "0.1.2"

    @staticmethod
    def is_dev() -> bool:
        """
        @brief      Check if the software is running in development mode.
        @return     @c true if the software is running in development mode, @c false otherwise.
        @note       It is a static method.
        """
        return not "__compiled__" in globals()

    @staticmethod
    def resource_folder() -> str:
        """
        @brief      Get the folder of the resources.
        @return     The folder of the resources.
        @details    In development mode, it is the folder of the resources under the parent folder of the executable file.
                    In production mode, it is the same as the folder of the executable file.
        @note       It is a static method.
        """
        if SysUtils.is_dev():
            return str(Path(SysUtils.exe_folder()).parent / "resources")
        else:
            app_asar = Path(SysUtils.exe_folder()).parent / "app.asar"
            if app_asar.exists():
                return str(app_asar.parent)
            else:
                return str(Path(SysUtils.exe_folder()) / "resources")

    @staticmethod
    def database_folder() -> str:
        """
        @brief      Get the folder of the database.
        @return     The folder of the database.
        @details    It is the subfolder "database" of the resource folder.
        @note       It is a static method.
        """
        return str(Path(SysUtils.resource_folder()) / "database")

    @staticmethod
    def templates_folder() -> str:
        """
        @brief      Get the folder of the templates.
        @return     The folder of the templates.
        @details    It is the subfolder "templates" of the resource folder.
        @note       It is a static method.
        """
        return str(Path(SysUtils.resource_folder()) / "templates")

    @staticmethod
    def packages_folder() -> str:
        """
        @brief      Get the folder of the packages.
        @return     The folder of the packages.
        @details    It is the subfolder "packages" of the resource folder.
        @note       It is a static method.
        """
        return str(Path.home() / ".csp" / "packages")

    @staticmethod
    def packages_index_file() -> str:
        """
        @brief      Get the file path of the package index.
        @return     The file path of the package index as a string.
        @details    It is the "packages.index" file located in the "packages" subfolder of the database folder.
        @note       It is a static method.
        """
        return str(Path(SysUtils.packages_folder()) / "packages.index")

    @staticmethod
    def public_folder() -> str:
        """
        @brief      Get the folder of the public files.
        @return     The folder of the public files.
        @details    It is the subfolder "public" of the resource folder.
        @note       It is a static method.
        """
        return str(Path(SysUtils.exe_folder()) / "public")


SYS_UTILS = SysUtils()
