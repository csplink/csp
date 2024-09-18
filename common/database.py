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

from loguru import logger

from .settings import SETTINGS


class Database():

    @logger.catch(default=False)
    def checkRepository(self, repository: dict) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "repository.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=repository, schema=schema)
        return True

    def getRepositoryByPath(self, path: str) -> dict:
        if os.path.isfile(path):
            succeed = False
            with open(path, 'r', encoding='utf-8') as f:
                repository = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.checkRepository(repository)
            if succeed:
                return repository
            else:
                return {}
        else:
            logger.error(f"{path} is not file!")
            return {}

    def getRepository(self) -> dict[str, dict[str, dict[str, dict[str, dict[str, dict]]]]]:
        return self.getRepositoryByPath(os.path.join(SETTINGS.DATABASE_FOLDER, "repository.yml"))

    @logger.catch(default=False)
    def checkSummary(self, summary: dict) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "summary.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=summary, schema=schema)
        return True

    def getSummaryByPath(self, path: str) -> dict:
        if os.path.isfile(path):
            succeed = False
            with open(path, 'r', encoding='utf-8') as f:
                summary = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.checkSummary(summary)
            if succeed:
                return summary
            else:
                return {}
        else:
            logger.error(f"{path} is not file!")
            return {}

    def getSummary(self, vendor: str, name: str) -> dict:
        return self.getSummaryByPath(
            os.path.join(SETTINGS.DATABASE_FOLDER, "summary", vendor.lower(), f"{name.lower()}.yml"))

    @logger.catch(default=False)
    def checkIp(self, ip: dict) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "ip.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=ip, schema=schema)
        return True

    def getIpByPath(self, path: str) -> dict:
        if os.path.isfile(path):
            succeed = False
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

    @logger.catch(default=False)
    def checkContributors(self, contributors: list) -> bool:
        with open(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "contributors.yml"), 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=contributors, schema=schema)
        return True

    def getContributors(self) -> dict:
        if os.path.isfile(SETTINGS.CONTRIBUTORS_FILE):
            succeed = False
            with open(SETTINGS.CONTRIBUTORS_FILE, 'r', encoding='utf-8') as f:
                contributors = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.checkContributors(contributors)
            if succeed:
                return contributors
            else:
                return {}
        else:
            return []


DATABASE = Database()
