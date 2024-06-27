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
    def checkPinout(pinout: dict, path: str) -> bool:
        with open("resource/database/schema/pinout.yml", 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            jsonschema.validate(instance=pinout, schema=schema)
        except jsonschema.exceptions.ValidationError as exception:
            print(f"invalid yaml {path}")
            print(exception)

    @staticmethod
    def getPinoutByPath(path: str) -> dict:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                pinout = yaml.load(f.read(), Loader=yaml.FullLoader)

            Database.checkPinout(pinout, path)
            return pinout
        else:
            print(path)

    @staticmethod
    def getPinout(vendor: str, hal: str, name: str) -> dict:
        return Database.getPinoutByPath(f"resource/database/hal/{vendor}/{hal}/{name}/pinout.yml")

    @staticmethod
    def checkRepository(repository: dict, path: str) -> bool:
        with open("resource/database/schema/repository.yml", 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
        try:
            jsonschema.validate(instance=repository, schema=schema)
        except jsonschema.exceptions.ValidationError as exception:
            print(f"invalid yaml {path}")
            print(exception)

    @staticmethod
    def getRepositoryByPath(path: str) -> dict:
        with open(path, 'r', encoding='utf-8') as f:
            repository = yaml.load(f.read(), Loader=yaml.FullLoader)

        Database.checkRepository(repository, path)
        return repository

    @staticmethod
    def getRepository() -> dict:
        return Database.getRepositoryByPath(f"resource/database/repository.yml")


if __name__ == '__main__':
    Database.getPinout("geehy", "csp_hal_apm32f1", "apm32f103zet6")
    Database.getRepository()
