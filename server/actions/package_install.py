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
# @file        package_install.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-29     xqyjlj       initial version
#

from flask_socketio import emit
from gevent.lock import Semaphore
from loguru import logger
from packages.description import PackageDescription
from packages.package import Package
from tqdm import tqdm

__lock = Semaphore()


class __Slot:
    def __init__(self):
        self.__generated_bar = None
        self.sid = ""

    def on_install_progress(self, sender, **kwargs):
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]
        if self.__generated_bar is None:
            self.__generated_bar = tqdm(total=count, desc="install", unit="file")
        self.__generated_bar.set_description(f"install {file}")
        self.__generated_bar.n = index
        self.__generated_bar.refresh()

        if index == count:
            self.__generated_bar.set_description("install")
            self.__generated_bar.close()
            self.__generated_bar = None

    def on_sio_install_progress(self, sender, **kwargs):
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]
        emit(
            "package/install.progress",
            {"count": count, "index": index, "file": file},
            to=self.sid,
        )

    def on_install(self, sender, **kwargs):
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]

        print(f"[{index}/{count}] install {file}")


def _action_package_install(
    path: str, progress: bool, verbose: bool, sid: str | None = None
) -> PackageDescription | None:
    package = Package()
    slot = __Slot()
    if sid:
        slot.sid = sid
        package.emitter["install"].connect(slot.on_sio_install_progress)
    else:
        if progress:
            package.emitter["install"].connect(slot.on_install_progress)
        if verbose:
            package.emitter["install"].connect(slot.on_install)
    package_desc = package.install(path)
    if package_desc is None:
        logger.error(f"Failed to install {path}")
        return package_desc
    else:
        logger.success(
            f"Successfully installed {package_desc.name}-{package_desc.version}"
        )
        return package_desc


def action_package_install(
    path: str, progress: bool, verbose: bool, sid: str | None = None
) -> PackageDescription | None:
    with __lock:
        return _action_package_install(path, progress, verbose, sid)
