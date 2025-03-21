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
# @file        contributors.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-14     xqyjlj       initial version
#

import json
import os

import jsonschema
import yaml
from loguru import logger

from .settings import SETTINGS


class ContributorType:
    def __init__(self, data: dict):
        self.__data = data

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def avatar(self) -> str:
        return self.__data.get("avatar", "")

    @property
    def contributions(self) -> int:
        return self.__data.get("contributions", 0)

    @property
    def html_url(self) -> str:
        return self.__data.get("htmlUrl", "")

    @property
    def name(self) -> str:
        return self.__data.get("name", "")


class Contributor:
    def __init__(self):
        self.__contributors = self.get_contributors()

    @logger.catch(default=False)
    def check_contributors(self, contributors: list) -> bool:
        with open(
            os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "contributors.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=contributors, schema=schema)
        return True

    @logger.catch(default=[])
    def __get_contributors(self) -> list[dict]:
        if os.path.isfile(SETTINGS.CONTRIBUTORS_FILE):
            with open(SETTINGS.CONTRIBUTORS_FILE, "r", encoding="utf-8") as f:
                contributors = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.check_contributors(contributors)
            if succeed:
                return contributors
            else:
                return []
        else:
            return []

    def get_contributors(self) -> list[ContributorType]:
        l = []
        contributors = self.__get_contributors()
        for contributor in contributors:
            l.append(ContributorType(contributor))
        return l

    def contributors(self) -> list[ContributorType]:
        return self.__contributors
