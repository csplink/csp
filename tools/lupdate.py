#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        lupdate.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-08-18     xqyjlj       initial version
#

import glob
import os
import platform
import re
import subprocess
import sys

__languages = ["zh_CN"]

__root_dir = os.path.join(os.path.dirname(__file__), "..")


class Lupdate:
    @staticmethod
    def run(root: str, languages: list[str]):
        if platform.system() == "Windows":
            exes = glob.glob(
                f"{os.path.dirname(sys.executable)}/**/pyside6-lupdate.exe",
                recursive=True,
            )
        else:
            exes = glob.glob(
                f"{os.path.dirname(sys.executable)}/**/pyside6-lupdate", recursive=True
            )

        if len(exes) > 0:
            exe = exes[0]
            py_files = glob.glob(f"{root}/**/*.py", recursive=True)
            ui_files = glob.glob(f"{root}/**/*.ui", recursive=True)
            src_files = []

            for file in py_files:
                with open(file, "r", encoding="utf-8") as f:
                    text = f.read()
                    if re.search(r'.tr\((["\'])(.*?)\1\)', text) or re.search(
                        r'QCoreApplication.translate\((["\'])(.*?)\1\)', text
                    ):
                        src_files.append(file)

            for file in ui_files:
                src_files.append(file)

            for lang in languages:
                ts_file = os.path.join(root, "resource", "i18n", f"csplink.{lang}.ts")
                if not os.path.isdir(os.path.dirname(ts_file)):
                    os.makedirs(os.path.dirname(ts_file))
                subprocess.call(
                    [exe, "-source-language", "en_US", "-target-language", lang]
                    + src_files
                    + ["-ts", ts_file]
                )
        else:
            print("can not find lupdate")


if __name__ == "__main__":
    Lupdate.run(__root_dir, __languages)
