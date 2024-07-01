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

import jsonschema
import yaml, os


class Database():

    @staticmethod
    def checkRepository(repository: dict, path: str) -> bool:
        with open("resource/database/schema/repository.yml", 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            jsonschema.validate(instance=repository, schema=schema)
        except jsonschema.exceptions.ValidationError as exception:
            print(f"invalid yaml {path}")
            print(exception)
            raise exception

    @staticmethod
    def getRepositoryByPath(path: str) -> dict:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                repository = yaml.load(f.read(), Loader=yaml.FullLoader)

            Database.checkRepository(repository, path)
            return repository
        else:
            print(f"{path} is not file!")
            return {}

    @staticmethod
    def getRepository() -> dict:
        return Database.getRepositoryByPath(f"resource/database/repository.yml")

    @staticmethod
    def checkSummary(summary: dict, path: str) -> bool:
        with open("resource/database/schema/summary.yml", 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            jsonschema.validate(instance=summary, schema=schema)
        except jsonschema.exceptions.ValidationError as exception:
            print(f"invalid yaml {path}")
            print(exception)
            raise exception

    @staticmethod
    def getSummaryByPath(path: str) -> dict:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                summary = yaml.load(f.read(), Loader=yaml.FullLoader)

            Database.checkSummary(summary, path)
            return summary
        else:
            print(f"{path} is not file!")
            return {}

    @staticmethod
    def getSummary(vendor: str, name: str) -> dict:
        return Database.getSummaryByPath(f"resource/database/summary/{vendor.lower()}/{name.lower()}.yml")

    @staticmethod
    def checkIp(ip: dict, path: str) -> bool:
        with open("resource/database/schema/ip.yml", 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            jsonschema.validate(instance=ip, schema=schema)
        except jsonschema.exceptions.ValidationError as exception:
            print(f"invalid yaml {path}")
            print(exception)
            raise exception

    @staticmethod
    def getIpByPath(path: str) -> dict:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                ip = yaml.load(f.read(), Loader=yaml.FullLoader)

            Database.checkIp(ip, path)
            return ip
        else:
            print(f"{path} is not file!")
            return {}

    @staticmethod
    def getIp(vendor: str, name: str) -> dict:
        return Database.getIpByPath(f"resource/database/ip/{vendor.lower()}/{name.lower()}.yml")


if __name__ == '__main__':
    Database.getRepository()
    Database.getSummary("geehy", "apm32f103zet6")
    Database.getIp("geehy", "apm32f103_gpio")
