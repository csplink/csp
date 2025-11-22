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
# @file        package_uninstall.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-22     xqyjlj       initial version
#

from gevent.lock import Semaphore
from loguru import logger
from packages.package import Package

__lock = Semaphore()


def _action_package_uninstall(kind: str, name: str, version: str) -> bool:
    package = Package()
    result = package.uninstall(kind, name, version)
    if result:
        logger.success(f"Uninstall {kind}:{name}@{version} successfully")
    return result


def action_package_uninstall(kind: str, name: str, version: str) -> bool:
    with __lock:
        return _action_package_uninstall(kind, name, version)
