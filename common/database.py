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
# @file        database.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-24     xqyjlj       initial version
#

import os

import jsonschema
import yaml
from loguru import logger

from .settings import SETTINGS


class Database:
    @logger.catch(default=False)
    def checkIp(self, ip: dict) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "ip.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=ip, schema=schema)
        return True

    def getIpByPath(self, path: str) -> dict:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                ip = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.checkIp(ip)
            if succeed:
                return ip
            else:
                return {}
        else:
            logger.error(f"{path} is not file!")
            return {}

    def getIp(self, vendor: str, name: str) -> dict:
        return self.getIpByPath(os.path.join(SETTINGS.DATABASE_FOLDER, "ip", vendor.lower(), f"{name.lower()}.yml"))


DATABASE = Database()
