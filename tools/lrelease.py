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

rootDir = os.path.join(os.path.dirname(__file__), "..")

if platform.system() == 'Windows':
    exes = glob.glob(f"{os.path.dirname(sys.executable)}/**/lrelease.exe", recursive=True)
else:
    exes = glob.glob(f"{os.path.dirname(sys.executable)}/**/lrelease", recursive=True)

if len(exes) > 0:
    exe = exes[0]
    for lang in languages:
        tsFiles = glob.glob(f"{rootDir}/**/*.{lang}.ts", recursive=True)
        qmFile = os.path.join(rootDir, "resource", "i18n", f"csplink.{lang}.qm")
        if not os.path.isdir(os.path.dirname(qmFile)):
            os.makedirs(os.path.dirname(qmFile))
        subprocess.call([exe] + tsFiles + ['-qm', qmFile])
else:
    print("can not find lrelease")
