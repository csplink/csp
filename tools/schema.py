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
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        schema.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-02-09     xqyjlj       initial version
#

import glob
import json
import os

from pathlib import Path

import yaml

__rootDir = os.path.join(os.path.dirname(__file__), "..")


class Schema:
    @staticmethod
    def run(root: str):
        files = glob.glob(f"{root}/resource/database/schema/*.yml", recursive=False)
        for yamlFile in files:
            file = Path(yamlFile)
            jsonFile = file.parent / f"{file.stem}.json"

            with open(yamlFile, "r", encoding="utf-8") as fp:
                yaml_data = yaml.safe_load(fp)

            with open(jsonFile, "w", encoding="utf-8") as fp:
                json.dump(yaml_data, fp, indent=4, ensure_ascii=False)

            print(f"Updating {jsonFile!r}...")


if __name__ == "__main__":
    Schema.run(__rootDir)
