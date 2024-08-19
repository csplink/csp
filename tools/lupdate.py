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

import subprocess, sys, os, glob, re, platform

languages = ['zh_CN']

root_dir = os.path.join(os.path.dirname(__file__), "..")

if platform.system() == 'Windows':
    lupdate_exes = glob.glob(f"{os.path.dirname(sys.executable)}/**/lupdate.exe", recursive=True)
else:
    lupdate_exes = glob.glob(f"{os.path.dirname(sys.executable)}/**/lupdate", recursive=True)

if len(lupdate_exes) > 0:
    lupdate_exe = lupdate_exes[0]
    py_files = glob.glob(f"{root_dir}/**/*.py", recursive=True)
    ui_files = glob.glob(f"{root_dir}/**/*.ui", recursive=True)
    src_files = []

    for file in py_files:
        with open(file, "r", encoding="utf-8") as f:
            text = f.read()
            pattern = r'tr\((["\'])(.*?)\1\)'
            if re.search(pattern, text):
                src_files.append(file)

    for file in ui_files:
        src_files.append(file)

    for lang in languages:
        for file in src_files:
            name = os.path.basename(file)
            if name.endswith(".ui"):
                folder = os.path.dirname(os.path.dirname(file))
            else:
                folder = os.path.dirname(file)
            folder = os.path.join(folder, "i18n")
            if not os.path.isdir(folder):
                os.makedirs(folder)
            ts_file = os.path.join(folder, f"{os.path.basename(file)}.{lang}.ts")
            subprocess.call([lupdate_exe, file, '-ts', ts_file])
else:
    print("can not find lupdate")
