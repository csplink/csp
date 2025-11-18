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
import platform
import shutil
import tarfile
import zipfile
from io import StringIO
from pathlib import Path

import jsonschema
from blinker import Signal
from loguru import logger
from ruamel.yaml import YAML
from utils.sys import SysUtils

from .description import PackageDescription
from .index import PackageIndex


class Package:

    def __init__(self):
        super().__init__()
        self.__index = self.get_package_index()
        self.__pdscs = {}

        self.__emitter = {
            "install": Signal("install"),
            "make": Signal("make"),
        }

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
        file_dir = str(Path(file_path).parent)

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
            os.makedirs(str(Path(file).parent), exist_ok=True)
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

    def dump(self) -> str:
        yaml = YAML()
        stream = StringIO()
        yaml.dump(self.__index.origin, stream)
        return stream.getvalue()

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
        if os.path.isfile(tmp_folder):
            os.remove(tmp_folder)
        os.makedirs(tmp_folder)

        if os.path.isfile(path):
            status = self._install_from_file(path, tmp_folder)
        elif os.path.isdir(path):
            status = self._install_from_dir(path, tmp_folder)
        else:
            logger.error(f"invalid package {path!r}")
            status = False
        if not status:
            return None

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
            folder, str(Path(SysUtils.packages_index_file()).parent)
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

    def _detect_file_type(self, file: str) -> str:
        """Detect file type by reading file header, not extension"""
        try:
            with open(file, "rb") as f:
                header = f.read(10)  # Read first 10 bytes

                # ZIP file magic numbers: PK (0x50 0x4B)
                if len(header) >= 2 and header[0] == 0x50 and header[1] == 0x4B:
                    return "zip"

                # TAR.GZ file magic numbers: 1F 8B 08 00
                if (
                    len(header) >= 4
                    and header[0] == 0x1F
                    and header[1] == 0x8B
                    and header[2] == 0x08
                ):
                    return "tar.gz"

        except Exception as e:
            logger.error(f"Failed to detect file type: {e}")

        return "unknown"

    def _install_from_file(self, file: str, tmp_folder: str) -> bool:
        file_type = self._detect_file_type(file)

        try:
            if file_type == "zip":
                return self._install_from_zip(file, tmp_folder)
            elif file_type == "tar.gz":
                return self._install_from_tar_gz(file, tmp_folder)
            else:
                logger.error(f"Unsupported file type: {file_type}")
                return False
        except Exception as e:
            logger.error(e)
            return False

    def _install_from_zip(self, file: str, tmp_folder: str) -> bool:
        """Install from ZIP file"""
        with zipfile.ZipFile(file, "r") as archive:
            members = archive.infolist()
            count = len(members)
            for index, member in enumerate(members, start=1):
                archive.extract(member, path=tmp_folder)
                self.__emitter["install"].send(
                    "package",
                    index=index,
                    count=count,
                    file=member.filename,
                )

        self._normalize_extracted_structure(tmp_folder)
        return True

    def _install_from_tar_gz(self, file: str, tmp_folder: str) -> bool:
        """Install from TAR.GZ file"""
        with tarfile.open(file, "r:gz") as archive:
            members = archive.getmembers()
            count = len(members)
            for index, member in enumerate(members, start=1):
                archive.extract(member, path=tmp_folder)
                self.__emitter["install"].send(
                    "package",
                    index=index,
                    count=count,
                    file=member.name,
                )

        self._normalize_extracted_structure(tmp_folder)
        return True

    def _normalize_extracted_structure(self, tmp_folder: str):
        """Normalize extracted structure - if only one directory exists, move it up one level"""
        dirs = os.listdir(tmp_folder)
        count = len(dirs)

        if count == 1 and os.path.isdir(os.path.join(tmp_folder, dirs[0])):
            d = os.path.join(tmp_folder, dirs[0])
            tmp_tmp_folder = os.path.join(str(Path(tmp_folder).parent), "tmp.tmp")
            shutil.move(d, tmp_tmp_folder)
            shutil.rmtree(tmp_folder)
            shutil.move(tmp_tmp_folder, tmp_folder)

    def _install_from_dir(self, path: str, tmp_folder: str) -> bool:
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
                    if not self.__is_ignored(os.path.join(root, d), path, gitignore_map)
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
            os.makedirs(str(Path(target_file).parent), exist_ok=True)
            shutil.copy2(source_file, target_file)
            _file = os.path.relpath(target_file, tmp_folder).replace("\\", "/")
            self.__emitter["install"].send(
                "package", index=index, count=count, file=_file
            )

        return True

    def make(self, path: str) -> PackageDescription | None:
        package_desc = self.get_package_description(path)
        if package_desc is None:
            return None

        if package_desc.type == "toolchains":
            plat = platform.system().lower()
            name = f"{package_desc.name}-{package_desc.version}.{plat}.csppack"
        else:
            name = f"{package_desc.name}-{package_desc.version}.csppack"

        self.compress_directory(path, str(Path(path).parent / name))

        return package_desc

    def __collect_files_for_compression(
        self, directory_path: str
    ) -> list[tuple[str, str]]:
        """
        Collect all files for compression, filtering by .gitignore patterns

        Args:
            directory_path: Path to directory to collect files from

        Returns:
            list of tuples: (source_file_path, relative_path_for_archive)
        """
        # Collect all .gitignore files and their patterns from the directory tree
        gitignore_map = self.__collect_gitignore_patterns(directory_path)

        items = []
        for root, dirs, files in os.walk(directory_path):
            # Filter out .git directory
            dirs[:] = [d for d in dirs if d not in [".git"]]

            # Filter out ignored directories based on .gitignore
            if gitignore_map:
                dirs[:] = [
                    d
                    for d in dirs
                    if not self.__is_ignored(
                        os.path.join(root, d), directory_path, gitignore_map
                    )
                ]

            for file in files:
                source_file = os.path.join(root, file)

                # Skip files that match .gitignore patterns
                if gitignore_map and self.__is_ignored(
                    source_file, directory_path, gitignore_map
                ):
                    continue

                rel_path = os.path.relpath(source_file, directory_path)
                items.append((source_file, rel_path))

        return items

    def compress_directory(self, directory_path: str, output_path: str) -> str:
        """
        Compress directory to zip on Windows or tar.gz on Linux

        Args:
            directory_path: Path to directory to compress (must be a directory)
            output_path: Output path for the compressed file

        Returns:
            str: Path to the compressed file

        Raises:
            ValueError: If directory_path is not a directory
            Exception: If compression fails
        """
        if not os.path.isdir(directory_path):
            raise ValueError(f"{directory_path} is not a directory")

        # Collect all files for compression
        files_to_compress = self.__collect_files_for_compression(directory_path)

        try:
            current_platform = platform.system().lower()

            if current_platform == "windows":
                return self._compress_to_zip(files_to_compress, output_path)
            else:  # Linux and other Unix-like systems
                return self._compress_to_tar_gz(files_to_compress, output_path)

        except Exception as e:
            logger.error(f"Failed to compress directory {directory_path}: {e}")
            raise

    def _compress_to_zip(
        self, files_to_compress: list[tuple[str, str]], output_path: str
    ) -> str:
        """Compress files to ZIP format"""
        with zipfile.ZipFile(
            output_path, "w", zipfile.ZIP_DEFLATED, compresslevel=9
        ) as zipf:
            count = len(files_to_compress)
            for index, (source_file, arcname) in enumerate(files_to_compress, start=1):
                zipf.write(source_file, arcname)

                # Send progress signal with count, index, and file
                self.__emitter["make"].send(
                    "package", index=index, count=count, file=arcname
                )

        logger.info(f"Successfully compressed to {output_path}")
        return output_path

    def _compress_to_tar_gz(
        self, files_to_compress: list[tuple[str, str]], output_path: str
    ) -> str:
        """Compress files to TAR.GZ format"""
        with tarfile.open(output_path, "w:gz") as tarf:
            count = len(files_to_compress)
            for index, (source_file, arcname) in enumerate(files_to_compress, start=1):
                tarf.add(source_file, arcname=arcname)

                # Send progress signal with count, index, and file
                self.__emitter["make"].send(
                    "package", index=index, count=count, file=arcname
                )

        logger.info(f"Successfully compressed to {output_path}")
        return output_path
