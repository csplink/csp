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

import jsonschema
import yaml, os
import py7zr, os, shutil, glob

from loguru import logger
from typing import Callable

from .settings import SETTINGS


class Package():
    __data = {}

    def __init__(self) -> None:
        index = self.__getPackageIndex()
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

    @logger.catch(default=False)
    def __checkYaml(self, schemaPath: str, instance: dict) -> bool:
        with open(schemaPath, 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=instance, schema=schema)
        return True

    def __getPackage(self, path: str) -> dict:
        if os.path.isfile(path):
            succeed = False
            with open(path, 'r', encoding='utf-8') as f:
                package = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkYaml(os.path.join(SETTINGS.databaseFolder.value, "schema", "package.yml"),
                                           package)
            if succeed:
                return package
            else:
                return {}
        else:
            logger.error(f"{path} is not file!")
            return {}

    def __getPackageIndex(self) -> dict:
        file = SETTINGS.REPOSITORY_INDEX_FILE
        if os.path.isfile(file):
            succeed = False
            with open(file, 'r', encoding='utf-8') as f:
                index = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = self.__checkYaml(os.path.join(SETTINGS.databaseFolder.value, "schema", "package_index.yml"),
                                           index)
            if succeed:
                return index
            else:
                return {}
        else:
            with open(file, 'w') as f:
                pass
            return {}

    def dump(self):
        return yaml.dump(self.__data)

    def save(self):
        with open(SETTINGS.REPOSITORY_INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(self.dump())

    def path(self, type: str, name: str, version: str) -> str:
        return self.__data.get(type, {}).get(name, {}).get(version, "")

    def install(self, file: str, callback: Callable[[str, float], None]) -> bool:
        if not os.path.isfile(file):
            return False

        repositoryFolder = SETTINGS.repositoryFolder.value

        tmpFolder = os.path.join(repositoryFolder, "tmp")
        if os.path.isdir(tmpFolder):
            shutil.rmtree(tmpFolder)
        elif os.path.isfile(tmpFolder):
            os.remove(tmpFolder)
        os.makedirs(tmpFolder)

        with py7zr.SevenZipFile(file, 'r') as archive:
            info = archive.archiveinfo()
            cbk = Callback(info.uncompressed, callback)
            archive.extractall(path=tmpFolder, callback=cbk)

        # --------------------------------------------------------------------------------------------------------------
        dirs = os.listdir(tmpFolder)
        count = len(dirs)

        if count == 1 and os.path.isdir(os.path.join(tmpFolder, dirs[0])):
            dir = os.path.join(tmpFolder, dirs[0])
            tmpTmpFolder = os.path.join(repositoryFolder, "tmp.tmp")
            shutil.move(dir, tmpTmpFolder)
            shutil.rmtree(tmpFolder)
            shutil.move(tmpTmpFolder, tmpFolder)
        # --------------------------------------------------------------------------------------------------------------
        files = glob.glob(f"{tmpFolder}/*.csppack")
        count = len(files)
        if count != 1:
            logger.error(f"invalid package {file}")
            return False

        packageFile = files[0]
        package = self.__getPackage(packageFile)
        if len(package) == 0:
            logger.error(f"invalid package file {packageFile}")
            return False

        type = package["type"].lower()
        vendor = package["vendor"]
        name = package["name"]
        version = package["version"].lower()

        vendorFolder = os.path.join(repositoryFolder, type, vendor.lower(), name.lower())
        folder = os.path.join(vendorFolder, version)
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        elif os.path.isfile(folder):
            os.remove(folder)

        if not os.path.isdir(vendorFolder):
            os.makedirs(vendorFolder)
        elif os.path.isfile(vendorFolder):
            os.remove(vendorFolder)
            os.makedirs(vendorFolder)

        shutil.move(tmpFolder, folder)

        self.__data.setdefault(type, {}).setdefault(vendor, {}).setdefault(name, {})[version] = folder
        self.save()

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
