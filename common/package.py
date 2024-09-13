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

import py7zr, os, shutil, glob

from typing import Callable

from .database import Database
from .settings import SETTINGS


class Package():
    __data = {}

    def __init__(self) -> None:
        index = Database.getPackageIndex()
        if index is None:
            self.__data = {}
        else:
            self.__data = index

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

    def install(self, file: str, callback: Callable[[str, float], None]) -> bool:
        if not os.path.isfile(file):
            return False

        tmpFolder = os.path.join(SETTINGS.repositoryFolder.value, "tmp")
        if os.path.isdir(tmpFolder):
            shutil.rmtree(tmpFolder)
        os.makedirs(tmpFolder)

        with py7zr.SevenZipFile(file, 'r') as archive:
            info = archive.archiveinfo()
            cbk = Callback(info.uncompressed, callback)
            archive.extractall(path=tmpFolder, callback=cbk)

        dirs = os.listdir(tmpFolder)
        count = len(dirs)

        if count == 1:
            dir = os.path.join(tmpFolder, dirs[0])
            tmpTmpFolder = os.path.join(SETTINGS.repositoryFolder.value, "tmp.tmp")
            shutil.move(dir, tmpTmpFolder)
            shutil.rmtree(tmpFolder)
            shutil.move(tmpTmpFolder, tmpFolder)

        return True


class Callback(py7zr.callbacks.ExtractCallback):

    __archiveTotal = 0
    __totalBytes = 0
    __callback = None

    def __init__(self, totalBytes, callback: Callable[[str, float], None]):
        self.__archiveTotal = totalBytes
        self.__callback = callback

    def report_start_preparation(self):
        pass

    def report_start(self, processingFilePath, processingBytes):
        pass

    def report_update(self, decompressedBytes):
        pass

    def report_end(self, processingFilePath, wroteBytes):
        if self.__archiveTotal == 0:
            self.__callback(processingFilePath, 1.0)
            return

        self.__totalBytes += int(wroteBytes)
        progress = self.__totalBytes / self.__archiveTotal
        self.__callback(processingFilePath, progress)

    def report_warning(self, message):
        pass

    def report_postprocess(self):
        pass


PACKAGE = Package()
