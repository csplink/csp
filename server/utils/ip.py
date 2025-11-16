#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
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
# @file        ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-09     xqyjlj       initial version
#
import os

import jsonschema
from loguru import logger
from public.csp.ip import Ip
from ruamel.yaml import YAML

from .sys import SysUtils


class IpUtils:

    def __init__(self):
        pass

    @staticmethod
    @logger.catch(default=False)
    def __check_ip(ip: dict) -> bool:
        with open(
            os.path.join(SysUtils.database_folder(), "schema", "ip.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            yaml = YAML()
            schema = yaml.load(f.read())
            validator = jsonschema.Draft7Validator(schema)
            errors = sorted(validator.iter_errors(ip), key=lambda e: e.path)
            if not errors:
                return True
            for e in errors:
                print("Validation error:", e.message)
                print("Error path:", list(e.path))
                print("Error schema path:", list(e.schema_path))
                logger.error(f"IP validation failed: {e}")
            return False
        return True

    @staticmethod
    @logger.catch(default=Ip({}))
    def load_ip(vendor: str, ip_type: str, name: str) -> Ip:
        file = os.path.join(
            SysUtils.database_folder(), "ip", ip_type, vendor, f"{name}.yml"
        )
        return IpUtils.load_ip_from_file(file)

    @staticmethod
    @logger.catch(default=Ip({}))
    def load_ip_from_file(file: str) -> Ip:
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                yaml = YAML()
                ip = yaml.load(f.read())
                succeed = IpUtils.__check_ip(ip)
            if succeed:
                logger.info(f"Successfully loaded IP: {file}")
                return Ip(ip)
            else:
                logger.error(f"IP validation failed for {file}")
                return Ip({})
        else:
            logger.error(f"{file} is not file!")
            return Ip({})
