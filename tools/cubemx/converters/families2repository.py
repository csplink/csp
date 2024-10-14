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
# @file        families2repository.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-14     xqyjlj       initial version
#

import getopt
import os
import sys
import xml.etree.ElementTree as etree


def families2repository(path: str) -> dict[str, dict]:
    items = {}
    tree = etree.parse(path)
    root = tree.getroot()
    for familyNode in root:
        for subFamilyNode in familyNode:
            for mcuNode in subFamilyNode:
                print(mcuNode.tag, mcuNode.attrib)
    return {"soc": {'STMicroelectronics': items}}


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:", ["help", "src="])
    except getopt.GetoptError:
        # help()
        sys.exit(2)

    src = ''
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            # help()
            sys.exit()
        elif opt in ("-s", "--src"):
            src = arg

    if not os.path.isfile(src):
        print(f'"{src}" is not a file')
        sys.exit(2)

    repo = families2repository(src)
    print(repo)
