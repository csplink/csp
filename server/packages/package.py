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
# @file        package.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-29     xqyjlj       initial version
#

import fnmatch
import glob
import os
import shutil
import zipfile

import jsonschema
from blinker import Signal
from loguru import logger
from ruamel.yaml import YAML
from utils.sys import SysUtils

from .description import PackageDescription
from .index import PackageIndex


class Package:
    __emitter = {
        "install": Signal("install"),
    }

    def __init__(self):
        super().__init__()
        self.__index = self.get_package_index()
        self.__pdscs = {}

    @logger.catch(default=False)
    def __check_yaml(self, schema_path: str, instance: dict) -> bool:
        with open(schema_path, "r", encoding="utf-8") as f:
            yaml = YAML()
            schema = yaml.load(f.read())
            jsonschema.validate(instance=instance, schema=schema)
        return True

    @logger.catch(default=None)
    def __get_package_description(self, path: str) -> PackageDescription | None:
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                yaml = YAML()
                package: dict = yaml.load(f.read())
                path = os.path.join(
                    SysUtils.database_folder(), "schema", "packageDescription.yml"
                )
                succeed = self.__check_yaml(path, package)
            if succeed:
                return PackageDescription(package)
            else:
                return None
        else:
            logger.error(f"{path} is not file!")
            return None

    def get_package_description_auto(self, path: str) -> PackageDescription | None:
        if os.path.isfile(path):
            return self.__get_package_description(path)
        elif os.path.isdir(path):
            files = glob.glob(f"{path}/*.csppdsc")
            count = len(files)
            if count != 1:
                logger.error(f"invalid package")
                return None
            package_file = files[0]
            return self.__get_package_description(package_file)
        else:
            return None

    def __collect_gitignore_patterns(self, base_path: str) -> dict[str, list[str]]:
        """Collect all .gitignore files and their patterns from the directory tree"""
        gitignore_map = {}

        for root, dirs, files in os.walk(base_path):
            # Skip .git directories
            dirs[:] = [d for d in dirs if d != ".git"]

            gitignore_file = os.path.join(root, ".gitignore")
            if os.path.isfile(gitignore_file):
                patterns = []
                try:
                    with open(gitignore_file, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            # Skip empty lines and comments
                            if line and not line.startswith("#"):
                                patterns.append(line)
                    if patterns:
                        gitignore_map[root] = patterns
                except Exception as e:
                    logger.warning(
                        f"Failed to read .gitignore at {gitignore_file}: {e}"
                    )

        return gitignore_map

    def __is_ignored(
        self, file_path: str, base_path: str, gitignore_map: dict[str, list[str]]
    ) -> bool:
        """Check if a file should be ignored based on hierarchical .gitignore patterns"""
        if not gitignore_map:
            return False

        # Get relative path from base directory
        rel_path = os.path.relpath(file_path, base_path).replace("\\", "/")
        file_dir = os.path.dirname(file_path)

        # Collect applicable patterns from all .gitignore files
        # Process from most general (base) to most specific (closest to file)
        applicable_patterns = []

        # Find all .gitignore files that could affect this file
        for gitignore_dir, patterns in gitignore_map.items():
            # Check if this .gitignore file is in a parent directory of the file
            try:
                rel_gitignore_path = os.path.relpath(gitignore_dir, base_path)
                if file_dir.startswith(gitignore_dir) or gitignore_dir == base_path:
                    # Calculate relative path from this .gitignore's directory
                    if gitignore_dir == base_path:
                        check_path = rel_path
                    else:
                        check_path = os.path.relpath(file_path, gitignore_dir).replace(
                            "\\", "/"
                        )

                    applicable_patterns.append((gitignore_dir, patterns, check_path))
            except ValueError:
                # Skip if paths are not related
                continue

        # Sort by directory depth (deeper directories have higher precedence)
        applicable_patterns.sort(key=lambda x: x[0].count(os.sep))

        is_ignored = False

        # Apply patterns in order (general to specific)
        for gitignore_dir, patterns, check_path in applicable_patterns:
            for pattern in patterns:
                # Handle negation patterns (starting with !)
                negate = pattern.startswith("!")
                if negate:
                    pattern = pattern[1:]

                # Handle directory patterns (ending with /)
                if pattern.endswith("/"):
                    pattern = pattern[:-1]
                    # Check if any parent directory matches
                    path_parts = check_path.split("/")
                    for i in range(len(path_parts)):
                        dir_path = "/".join(path_parts[: i + 1])
                        if fnmatch.fnmatch(dir_path, pattern):
                            is_ignored = not negate
                            break
                else:
                    # Check file pattern
                    if fnmatch.fnmatch(check_path, pattern) or fnmatch.fnmatch(
                        os.path.basename(check_path), pattern
                    ):
                        is_ignored = not negate

        return is_ignored

    def get_package_description(self, path: str) -> PackageDescription | None:
        if path in self.__pdscs:
            return self.__pdscs[path]
        else:
            pdsc = self.get_package_description_auto(path)
            self.__pdscs[path] = pdsc
            return pdsc

    @logger.catch(default=PackageIndex({}))
    def __get_package_index(self) -> PackageIndex:
        file = SysUtils.packages_index_file()
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                yaml = YAML()
                index = yaml.load(f.read())
                # noinspection PyArgumentList
                succeed = self.__check_yaml(
                    os.path.join(
                        SysUtils.database_folder(), "schema", "packageIndex.yml"
                    ),
                    index,
                )
            if succeed:
                return PackageIndex(index if index is not None else {})
            else:
                return PackageIndex({})
        else:
            os.makedirs(os.path.dirname(file), exist_ok=True)
            with open(file, "w"):
                pass
            return PackageIndex({})

    @property
    def emitter(self):
        return self.__emitter

    def get_package_index(self) -> PackageIndex:
        return self.__get_package_index()

    def index(self) -> PackageIndex:
        return self.__index

    def dump(self):
        yaml = YAML()
        return yaml.dump(self.__index.origin)

    def save(self):
        with open(SysUtils.packages_index_file(), "w", encoding="utf-8") as f:
            f.write(self.dump())

    def install(self, path: str) -> PackageDescription | None:
        if not os.path.exists(path):
            return None

        repository_folder = SysUtils.packages_folder()
        tmp_folder = os.path.join(repository_folder, "tmp")

        if os.path.isdir(tmp_folder):
            shutil.rmtree(tmp_folder)
        if os.path.isfile(path):
            if os.path.isfile(tmp_folder):
                os.remove(tmp_folder)
            os.makedirs(tmp_folder)

            try:
                with zipfile.ZipFile(path, "r") as archive:
                    members = archive.infolist()
                    extracted = 0
                    count = len(members)
                    for index, member in enumerate(members, start=1):
                        archive.extract(member, path=tmp_folder)
                        extracted += member.file_size
                        self.__emitter["install"].send(
                            "package",
                            index=index,
                            count=count,
                            file=member.filename,
                        )
            except Exception as e:
                logger.error(e)
                return None

            dirs = os.listdir(tmp_folder)
            count = len(dirs)

            if count == 1 and os.path.isdir(os.path.join(tmp_folder, dirs[0])):
                d = os.path.join(tmp_folder, dirs[0])
                tmp_tmp_folder = os.path.join(repository_folder, "tmp.tmp")
                shutil.move(d, tmp_tmp_folder)
                shutil.rmtree(tmp_folder)
                shutil.move(tmp_tmp_folder, tmp_folder)
        elif os.path.isdir(path):
            # Collect all .gitignore files and their patterns from the directory tree
            gitignore_map = self.__collect_gitignore_patterns(path)

            items = []
            for root, dirs, files in os.walk(path):
                # Filter out .git directory
                dirs[:] = [d for d in dirs if d not in [".git"]]

                # Filter out ignored directories based on .gitignore
                if gitignore_map:
                    dirs[:] = [
                        d
                        for d in dirs
                        if not self.__is_ignored(
                            os.path.join(root, d), path, gitignore_map
                        )
                    ]

                for file in files:
                    source_file = os.path.join(root, file)

                    # Skip files that match .gitignore patterns
                    if gitignore_map and self.__is_ignored(
                        source_file, path, gitignore_map
                    ):
                        continue

                    rel_path = os.path.relpath(source_file, path)
                    target_file = os.path.join(tmp_folder, rel_path)
                    items.append((source_file, target_file))

            count = len(items)
            for index, (source_file, target_file) in enumerate(items, start=1):
                os.makedirs(os.path.dirname(target_file), exist_ok=True)
                shutil.copy2(source_file, target_file)
                _file = os.path.relpath(target_file, tmp_folder).replace("\\", "/")
                self.__emitter["install"].send(
                    "package", index=index, count=count, file=_file
                )

        # ----------------------------------------------------------------------------------------------------------
        package_desc = self.get_package_description(tmp_folder)
        if package_desc is None:
            logger.error(f"invalid package {tmp_folder}")
            return None

        kind = package_desc.type.lower()
        vendor = package_desc.vendor
        name = package_desc.name
        version = package_desc.version.lower()

        vendor_folder = os.path.join(
            repository_folder, kind, vendor.lower(), name.lower()
        )
        folder = os.path.join(vendor_folder, version).replace("\\", "/")
        if os.path.isdir(folder):
            shutil.rmtree(folder)
        elif os.path.isfile(folder):
            os.remove(folder)

        if not os.path.isdir(vendor_folder):
            os.makedirs(vendor_folder)
        elif os.path.isfile(vendor_folder):
            os.remove(vendor_folder)
            os.makedirs(vendor_folder)

        shutil.move(tmp_folder, folder)
        package_path = os.path.relpath(
            folder, os.path.dirname(SysUtils.packages_index_file())
        ).replace("\\", "/")
        self.__index.origin.setdefault(kind, {}).setdefault(name, {})[
            version
        ] = package_path
        self.save()

        return package_desc

    def uninstall(self, kind: str, name: str, version: str) -> bool:
        path = self.index().path(kind, name, version)

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

        return True
