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
# @file        package_make.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-17     xqyjlj       initial version
#

from flask_socketio import emit
from loguru import logger
from packages.description import PackageDescription
from packages.package import Package
from tqdm import tqdm


class __Slot:
    def __init__(self):
        self.__generated_bar = None
        self.sid = ""

    def on_make_progress(self, sender, **kwargs):
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]
        if self.__generated_bar is None:
            self.__generated_bar = tqdm(total=count, desc="make", unit="file")
        self.__generated_bar.set_description(f"make {file}")
        self.__generated_bar.n = index
        self.__generated_bar.refresh()

        if index == count:
            self.__generated_bar.set_description("make")
            self.__generated_bar.close()
            self.__generated_bar = None

    def on_sio_make_progress(self, sender, **kwargs):
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]
        emit(
            "package/make.progress",
            {"count": count, "index": index, "file": file},
            to=self.sid,
        )

    def on_make(self, sender, **kwargs):
        count = kwargs["count"]
        index = kwargs["index"]
        file = kwargs["file"]

        print(f"[{index}/{count}] make {file}")


def action_package_make(
    path: str, progress: bool, verbose: bool, sid: str | None = None
) -> PackageDescription | None:
    package = Package()
    slot = __Slot()
    if sid:
        slot.sid = sid
        package.emitter["make"].connect(slot.on_sio_make_progress)
    else:
        if progress:
            package.emitter["make"].connect(slot.on_make_progress)
        if verbose:
            package.emitter["make"].connect(slot.on_make)
    package_desc = package.make(path)
    if package_desc is None:
        logger.error(f"Failed to make {path}")
        return package_desc
    else:
        logger.success(f"Successfully make {package_desc.name}-{package_desc.version}")
        return package_desc
