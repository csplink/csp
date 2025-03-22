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
# @file        lrelease.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-08-18     xqyjlj       initial version
#

import glob
import os
import platform
import subprocess
import sys

__languages = ["zh_CN"]

__root_dir = os.path.join(os.path.dirname(__file__), "..")


class Lrelease:
    @staticmethod
    def run(root: str, languages: list[str]):
        if platform.system() == "Windows":
            exes = glob.glob(
                f"{os.path.dirname(sys.executable)}/**/pyside6-lrelease.exe",
                recursive=True,
            )
        else:
            exes = glob.glob(
                f"{os.path.dirname(sys.executable)}/**/pyside6-lrelease", recursive=True
            )

        if len(exes) > 0:
            exe = exes[0]
            for lang in languages:
                ts_file = os.path.join(root, "resource", "i18n", f"csplink.{lang}.ts")
                assert os.path.isfile(ts_file), f"{ts_file} is not exists"
                qm_file = os.path.join(root, "resource", "i18n", f"csplink.{lang}.qm")
                if not os.path.isdir(os.path.dirname(qm_file)):
                    os.makedirs(os.path.dirname(qm_file))
                subprocess.call([exe, ts_file, "-qm", qm_file])
        else:
            print("can not find lrelease")
            sys.exit(1)


if __name__ == "__main__":
    Lrelease.run(__root_dir, __languages)
