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
from pathlib import Path
from typing import Callable

import jsonschema
import py7zr
import yaml
from PySide6.QtCore import QMutex, QMutexLocker, QObject, Signal
from loguru import logger
from py7zr import callbacks as py7zr_callbacks
from tqdm import tqdm

from .i18n_type import I18nType
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
                self.__website = PackageDescriptionType.AuthorType.WebsiteType(
                    self.__data.get("website", {})
                )
            return self.__website

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, data: dict):
        self.__data = data

        self.__author = None
        self.__vendorUrl = None
        self.__description = None
        self.__url = None

    def __str__(self) -> str:
        return json.dumps(self.__data, indent=2, ensure_ascii=False)

    @property
    def origin(self) -> dict:
        return self.__data

    @property
    def author(self) -> AuthorType:
        if self.__author is None:
            self.__author = PackageDescriptionType.AuthorType(
                self.__data.get("author", {})
            )
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
    def vendorUrl(self) -> I18nType:
        if self.__vendorUrl is None:
            self.__vendorUrl = I18nType(self.__data.get("vendorUrl", {}))
        return self.__vendorUrl

    @property
    def description(self) -> I18nType:
        if self.__description is None:
            self.__description = I18nType(self.__data.get("description", {}))
        return self.__description

    @property
    def url(self) -> I18nType:
        if self.__url is None:
            self.__url = I18nType(self.__data.get("url", {}))
        return self.__url

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
        path = self.__data.get(kind, {}).get(name, {}).get(version, "")
        if not path:
            return path
        path = Path(path)
        if path.is_absolute():
            return str(path)
        return str((SETTINGS.EXE_FOLDER / path).resolve())


class Package(QObject):
    installed = Signal(str, str, str, str)
    uninstalled = Signal(str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.__index = self.getPackageIndex()
        self.__pdscs = {}
        self.__mutex = QMutex()

    @logger.catch(default=False)
    def __checkYaml(self, schemaPath: str, instance: dict) -> bool:
        with open(schemaPath, "r", encoding="utf-8") as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=instance, schema=schema)
        return True

    @logger.catch(default=None)
    def __getPackageDescription(self, path: str) -> PackageDescriptionType | None:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                package: dict = yaml.load(f.read(), Loader=yaml.FullLoader)
                path = os.path.join(
                    SETTINGS.DATABASE_FOLDER, "schema", "package_description.yml"
                )
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
            with open(file, "r", encoding="utf-8") as f:
                index = yaml.load(f.read(), Loader=yaml.FullLoader)
                # noinspection PyArgumentList
                succeed = self.__checkYaml(
                    os.path.join(
                        SETTINGS.DATABASE_FOLDER, "schema", "package_index.yml"
                    ),
                    index,
                )
            if succeed:
                return PackageIndexType(index if index is not None else {})
            else:
                return PackageIndexType({})
        else:
            with open(file, "w"):
                pass
            return PackageIndexType({})

    def getPackageIndex(self) -> PackageIndexType:
        # noinspection PyTypeChecker,PyArgumentList
        return self.__getPackageIndex()

    def index(self) -> PackageIndexType:
        return self.__index

    def dump(self):
        return yaml.dump(self.__index.origin)

    def save(self):
        with open(SETTINGS.PACKAGE_INDEX_FILE, "w", encoding="utf-8") as f:
            f.write(self.dump())

    def install(self, path: str, callback: Callable[[str, float], None]) -> bool:
        if not os.path.exists(path):
            return False

        repositoryFolder = SETTINGS.packageFolder.value
        tmpFolder = os.path.join(repositoryFolder, "tmp")

        with QMutexLocker(self.__mutex):
            if os.path.isdir(tmpFolder):
                shutil.rmtree(tmpFolder)
            if os.path.isfile(path):
                if os.path.isfile(tmpFolder):
                    os.remove(tmpFolder)
                os.makedirs(tmpFolder)

                # noinspection PyBroadException
                try:
                    with py7zr.SevenZipFile(path, "r") as archive:
                        info = archive.archiveinfo()
                        cbk = Callback(info.uncompressed, callback)
                        archive.extractall(path=tmpFolder, callback=cbk)
                except Exception as e:
                    logger.error(e)
                    return False

                dirs = os.listdir(tmpFolder)
                count = len(dirs)

                if count == 1 and os.path.isdir(os.path.join(tmpFolder, dirs[0])):
                    d = os.path.join(tmpFolder, dirs[0])
                    tmpTmpFolder = os.path.join(repositoryFolder, "tmp.tmp")
                    shutil.move(d, tmpTmpFolder)
                    shutil.rmtree(tmpFolder)
                    shutil.move(tmpTmpFolder, tmpFolder)
            elif os.path.isdir(path):
                items = []
                for root, dirs, files in os.walk(path):
                    dirs[:] = [d for d in dirs if d not in [".git"]]
                    for file in files:
                        sourceFile = os.path.join(root, file)
                        relPath = os.path.relpath(sourceFile, path)
                        targetFile = os.path.join(tmpFolder, relPath)
                        items.append((sourceFile, targetFile))
                count = len(items)
                for index, (sourceFile, targetFile) in enumerate(items, start=1):
                    os.makedirs(os.path.dirname(targetFile), exist_ok=True)
                    shutil.copy2(sourceFile, targetFile)
                    callback(targetFile, (index / count) * 100)

            # ----------------------------------------------------------------------------------------------------------
            package = self.getPackageDescription(tmpFolder)
            if package is None:
                logger.error(f"invalid package {tmpFolder}")
                return False

            kind = package.type.lower()
            vendor = package.vendor
            name = package.name
            version = package.version.lower()

            vendorFolder = os.path.join(
                repositoryFolder, kind, vendor.lower(), name.lower()
            )
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
            self.__index.origin.setdefault(kind, {}).setdefault(name, {})[version] = (
                os.path.relpath(folder, SETTINGS.EXE_FOLDER)
            )
            self.save()
            self.installed.emit(
                kind, name, version, self.__index.path(kind, name, version)
            )

        return True

    def uninstall(self, kind: str, name: str, version: str) -> bool:
        path = self.index().path(kind, name, version)
        with QMutexLocker(self.__mutex):
            if os.path.isdir(path):
                shutil.rmtree(path)
            elif os.path.isfile(path):
                os.remove(path)
            else:
                logger.error(f"uninstall failed {kind}@{name}:{version}")
                return False
            # clear index tree
            self.__index.origin[kind][name].pop(version)
            if len(self.__index.origin[kind][name]) == 0:
                self.__index.origin[kind].pop(name)
                if len(self.__index.origin[kind]) == 0:
                    self.__index.origin.pop(kind)
            self.save()
            self.uninstalled.emit(kind, name, version, path)
        return True


class Callback(py7zr_callbacks.ExtractCallback):

    def __init__(self, totalBytes, callback: Callable[[str, float], None]):
        self.__archiveTotal = totalBytes
        self.__callback = callback
        self.__totalBytes = 0

    def report_start_preparation(self):
        pass

    def report_start(self, processingFilePath, processingBytes):
        pass

    def report_update(self, decompressedBytes):
        pass

    def report_end(self, processingFilePath, wroteBytes):
        if self.__archiveTotal == 0:
            self.__callback(processingFilePath, 100)
            return

        self.__totalBytes += int(wroteBytes)
        progress = (self.__totalBytes / self.__archiveTotal) * 100
        self.__callback(processingFilePath, progress)

    def report_warning(self, message):
        pass

    def report_postprocess(self):
        pass


class PackageCmd(QObject):

    def __init__(self, progress: bool, verbose: bool, parent=None):
        super().__init__(parent=parent)

        self.progress = progress
        self.verbose = verbose
        self.installBar = None

        PACKAGE.installed.connect(self.__on_x_installed)
        PACKAGE.uninstalled.connect(self.__on_x_uninstalled)

    def install(self, path: str) -> bool:
        return PACKAGE.install(path, self.__package_install_callback)

    def uninstall(self, kind: str, name: str, version: str) -> bool:
        return PACKAGE.uninstall(kind, name, version)

    def __on_x_installed(self, kind: str, name: str, version: str, path: str):
        print(
            f"successfully installed the package ‘{kind}@{name}:{version}’ to: {path!r}"
        )

    def __on_x_uninstalled(self, kind: str, name: str, version: str, path: str):
        print(
            f"successfully uninstalled the package ‘{kind}@{name}:{version}’ from: {path!r}"
        )

    def __package_install_callback(self, file: str, progress: float):
        if self.progress:
            if self.installBar is None:
                self.installBar = tqdm(total=100, desc="install", unit="file")
            self.installBar.set_description(f"install {file}")
            self.installBar.n = progress
            self.installBar.refresh()
            if progress == 100:
                self.installBar.set_description("install")
                self.installBar.close()
        else:
            if self.verbose:
                print(f"install {file}")


PACKAGE = Package()
