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

import glob
import json
import os
import shutil
from typing import Callable

import jsonschema
import py7zr
import yaml
from loguru import logger
from py7zr import callbacks as py7zr_callbacks

from .settings import SETTINGS


class PackageDescriptionType:
    class AuthorType:
        class WebsiteType:
            def __init__(self, data: dict):
                self.__data = data

            def __str__(self) -> str:
                return json.dumps(self.__data, indent=2, ensure_ascii=False)

            @property
            def origin(self) -> dict:
                return self.__data

            @property
            def blog(self) -> str:
                return self.__data.get("blog", "")

            @property
            def github(self) -> str:
                return self.__data.get("github", "")

        # ----------------------------------------------------------------------
        def __init__(self, data: dict):
            self.__data = data
            self.__website = None

        def __str__(self) -> str:
            return json.dumps(self.__data, indent=2, ensure_ascii=False)

        @property
        def origin(self) -> dict:
            return self.__data

        @property
        def name(self) -> str:
            return self.__data.get("name", "")

        @property
        def email(self) -> str:
            return self.__data.get("email", "")

        @property
        def website(self) -> WebsiteType:
            if self.__website is None:
                self.__website = PackageDescriptionType.AuthorType.WebsiteType(self.__data.get("website", {}))
            return self.__website

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data: dict):
        self.__data = data
        self.__author = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def author(self) -> AuthorType:
        if self.__author is None:
            self.__author = PackageDescriptionType.AuthorType(self.__data.get("author", {}))
        return self.__author

    @property
    def name(self) -> str:
        return self.__data.get("name", "")

    @property
    def version(self) -> str:
        return self.__data.get("version", "")

    @property
    def license(self) -> str:
        return self.__data.get("license", "")

    @property
    def type(self) -> str:
        return self.__data.get("type", "")

    @property
    def vendor(self) -> str:
        return self.__data.get("vendor", "")

    @property
    def vendorUrl(self) -> dict[str, str]:
        return self.__data.get("vendorUrl", {})

    @property
    def description(self) -> dict[str, str]:
        return self.__data.get("description", {})

    @property
    def url(self) -> dict[str, str]:
        return self.__data.get("url", {})

    @property
    def support(self) -> str:
        return self.__data.get("support", "")


class PackageIndexType:
    def __init__(self, data: dict):
        self.__data = data

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict[str, dict[str, dict[str, str]]]:
        return self.__data

    def types(self) -> list[str]:
        return list(self.__data.keys())

    def items(self, kind: str) -> list[str]:
        return list(self.__data.get(kind, {}).keys())

    def versions(self, kind: str, name: str) -> list[str]:
        return list(self.__data.get(kind, {}).get(name, {}).keys())

    def path(self, kind: str, name: str, version: str) -> str:
        return self.__data.get(kind, {}).get(name, {}).get(version, "")


class Package:
    def __init__(self) -> None:
        self.__index = self.getPackageIndex()
        self.__pdscs = {}

    @logger.catch(default=False)
    def __checkYaml(self, schemaPath: str, instance: dict) -> bool:
        with open(schemaPath, 'r', encoding='utf-8') as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=instance, schema=schema)
        return True

    @logger.catch(default=None)
    def __getPackageDescription(self, path: str) -> PackageDescriptionType | None:
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as f:
                package: dict = yaml.load(f.read(), Loader=yaml.FullLoader)
                path = os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "package_description.yml")
                # noinspection PyArgumentList
                succeed = self.__checkYaml(path, package)
            if succeed:
                return PackageDescriptionType(package)
            else:
                return None
        else:
            logger.error(f"{path} is not file!")
            return None

    def __getPackageDescriptionAuto(self, path: str) -> PackageDescriptionType | None:
        if os.path.isfile(path):
            # noinspection PyTypeChecker
            return self.__getPackageDescription(path)
        elif os.path.isdir(path):
            files = glob.glob(f"{path}/*.csppdsc")
            count = len(files)
            if count != 1:
                logger.error(f"invalid package")
                return None
            packageFile = files[0]
            # noinspection PyTypeChecker
            return self.__getPackageDescription(packageFile)
        else:
            return None

    def getPackageDescription(self, path: str) -> PackageDescriptionType | None:
        if path in self.__pdscs:
            return self.__pdscs[path]
        else:
            pdsc = self.__getPackageDescriptionAuto(path)
            self.__pdscs[path] = pdsc
            return pdsc

    @logger.catch(default=PackageIndexType({}))
    def __getPackageIndex(self) -> PackageIndexType:
        file = SETTINGS.PACKAGE_INDEX_FILE
        if os.path.isfile(file):
            with open(file, 'r', encoding='utf-8') as f:
                index = yaml.load(f.read(), Loader=yaml.FullLoader)
                # noinspection PyArgumentList
                succeed = self.__checkYaml(os.path.join(SETTINGS.DATABASE_FOLDER, "schema", "package_index.yml"), index)
            if succeed:
                return PackageIndexType(index if index is not None else {})
            else:
                return PackageIndexType({})
        else:
            with open(file, 'w'):
                pass
            return PackageIndexType({})

    def getPackageIndex(self) -> PackageIndexType:
        # noinspection PyTypeChecker,PyArgumentList
        return self.__getPackageIndex()

    @property
    def index(self) -> PackageIndexType:
        return self.__index

    def dump(self):
        return yaml.dump(self.__index.origin)

    def save(self):
        with open(SETTINGS.PACKAGE_INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(self.dump())

    def install(self, file: str, callback: Callable[[str, float], None]) -> bool:
        if not os.path.isfile(file):
            return False

        repositoryFolder = SETTINGS.packageFolder.value

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
            d = os.path.join(tmpFolder, dirs[0])
            tmpTmpFolder = os.path.join(repositoryFolder, "tmp.tmp")
            shutil.move(d, tmpTmpFolder)
            shutil.rmtree(tmpFolder)
            shutil.move(tmpTmpFolder, tmpFolder)
        # --------------------------------------------------------------------------------------------------------------
        package = self.getPackageDescription(tmpFolder)
        if package is None:
            logger.error(f"invalid package {tmpFolder}")
            return False

        kind = package.type.lower()
        vendor = package.vendor
        name = package.name
        version = package.version.lower()

        vendorFolder = os.path.join(repositoryFolder, kind, vendor.lower(), name.lower())
        folder = os.path.join(vendorFolder, version).replace("\\", "/")
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

        self.__index.origin.setdefault(kind, {}).setdefault(name, {})[version] = folder
        self.save()

        return True

    def uninstall(self, kind: str, name: str, version: str) -> bool:
        path = self.index.path(kind, name, version)
        if os.path.isdir(path):
            shutil.rmtree(path)
        elif os.path.isfile(path):
            os.remove(path)
        else:
            logger.error(f"uninstall failed {kind}@{name}-{version}")
            return False
        # clear index tree
        self.__index.origin[kind][name].pop(version)
        if len(self.__index.origin[kind][name]) == 0:
            self.__index.origin[kind].pop(name)
            if len(self.__index.origin[kind]) == 0:
                self.__index.origin.pop(kind)
        self.save()
        return True


class Callback(py7zr_callbacks.ExtractCallback):
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
