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

import subprocess, sys, os, glob, platform

languages = ['zh_CN']

root_dir = os.path.join(os.path.dirname(__file__), "..")

if platform.system() == 'Windows':
    lrelease_exes = glob.glob(f"{os.path.dirname(sys.executable)}/**/lrelease.exe", recursive=True)
else:
    lrelease_exes = glob.glob(f"{os.path.dirname(sys.executable)}/**/lrelease", recursive=True)

if len(lrelease_exes) > 0:
    lrelease_exe = lrelease_exes[0]
    for lang in languages:
        ts_files = glob.glob(f"{root_dir}/**/*.{lang}.ts", recursive=True)
        qm_file = os.path.join(root_dir, "resource", "i18n", f"csplink.{lang}.qm")
        if not os.path.isdir(os.path.dirname(qm_file)):
            os.makedirs(os.path.dirname(qm_file))
        subprocess.call([lrelease_exe] + ts_files + ['-qm', qm_file])
else:
    print("can not find lrelease")
