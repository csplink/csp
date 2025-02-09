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
# @file        pyuic.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-29     xqyjlj       initial version
#

import glob
import os
import platform
import subprocess
import sys

from pathlib import Path

__rootDir = os.path.join(os.path.dirname(__file__), "..")


class Pyuic:
    @staticmethod
    def run(root: str):
        if platform.system() == "Windows":
            exes = glob.glob(
                f"{os.path.dirname(sys.executable)}/**/pyside6-uic.exe", recursive=True
            )
        else:
            exes = glob.glob(
                f"{os.path.dirname(sys.executable)}/**/pyside6-uic", recursive=True
            )

        if len(exes) > 0:
            exe = exes[0]
            uiFiles = glob.glob(f"{root}/**/*.ui", recursive=True)
            for uiFile in uiFiles:
                uiFile = Path(uiFile)
                targetFile = uiFile.parent / f"{uiFile.stem}_ui.py"
                print(f"Updating '{targetFile}'...")
                subprocess.call([exe, uiFile, "-o", targetFile])
        else:
            print("can not find pyside6-uic")


if __name__ == "__main__":
    Pyuic.run(__rootDir)
