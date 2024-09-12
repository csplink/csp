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
# @file        package.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-28     xqyjlj       initial version
#

import py7zr, os

from .database import Database
from .settings import SETTINGS


class Package():
    __data = {}
    __tmpFolder = ""

    def __init__(self) -> None:
        index = Database.getPackageIndex()
        if index is None:
            self.__data = {}
        else:
            self.__data = index

        self._tmpFolder = os.path.join(SETTINGS.repositoryFolder.value, "tmp")

    @property
    def hal(self) -> dict:
        return self.__data.get("hal", {})

    @property
    def toolchains(self) -> dict:
        return self.__data.get("toolchains", {})

    @property
    def origin(self) -> dict:
        return self.__data

    def path(self, type: str, name: str, version: str) -> str:
        return self.__data.get(type, {}).get(name, {}).get(version, "")

    class callback(py7zr.callbacks.ExtractCallback):

        __archiveTotal = 0
        __totalBytes = 0

        def __init__(self, totalBytes):
            self.__archiveTotal = totalBytes

        def report_start_preparation(self):
            print("report_start_preparation")

        def report_start(self, processingFilePath, processingBytes):
            pass

        def report_update(self, decompressedBytes):
            pass

        def report_end(self, processingFilePath, wroteBytes):
            self.__totalBytes += int(wroteBytes)
            progress = self.__totalBytes / self.__archiveTotal
            print(progress, self.__totalBytes, self.__archiveTotal)

        def report_warning(self, message):
            pass

        def report_postprocess(self):
            pass

    def install(self, file):
        with py7zr.SevenZipFile(file, 'r') as archive:
            info = archive.archiveinfo()
            callback = Package.callback(info.uncompressed)
            archive.extractall(path=self._tmpFolder, callback=callback)


PACKAGE = Package()
