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
# @file        generator_loader.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-07     xqyjlj       initial version
#

import importlib.util
import sys
from pathlib import Path
from types import ModuleType
from typing import Dict, Optional

from loguru import logger
from utils.io import IO_UTILS


class GeneratorLoader:

    def __init__(self, name: str, folder: Path):
        self._package_name = name
        self._folder = folder
        self._filters_folder = self._folder / "filters"
        self._filters_package_name = f"{name}.filters"
        self._file_sha1_cache: Dict[str, str] = {}

    def load(self) -> Optional[ModuleType]:
        self._create_packages()
        self._load_filters()
        return self._load_generator()

    def _create_packages(self) -> None:
        if self._package_name not in sys.modules:
            pkg = ModuleType(self._package_name)
            pkg.__path__ = [str(self._folder)]
            sys.modules[self._package_name] = pkg

        if self._filters_package_name not in sys.modules:
            filters_pkg = ModuleType(self._filters_package_name)
            filters_pkg.__path__ = [str(self._filters_folder)]
            sys.modules[self._filters_package_name] = filters_pkg

    def _load_filters(self) -> None:
        if not self._filters_folder.exists():
            return
        for file in self._filters_folder.glob("*.py"):
            stem = file.stem
            full_name = f"{self._filters_package_name}.{stem}"
            try:
                if full_name in sys.modules and not self._is_file_changed(file):
                    continue

                if full_name in sys.modules:
                    del sys.modules[full_name]

                self._load_module(full_name, file, [str(self._filters_folder)])
            except Exception as e:
                logger.warning(f"Failed to load filter {file}: {e}")

    def _load_generator(self) -> Optional[ModuleType]:
        gen_file = self._folder / "generator.py"
        if not gen_file.exists():
            return None

        try:
            if self._package_name in sys.modules and not self._is_file_changed(
                gen_file
            ):
                return sys.modules[self._package_name]

            if self._package_name in sys.modules:
                del sys.modules[self._package_name]

            return self._load_module(self._package_name, gen_file, [str(self._folder)])
        except Exception as e:
            logger.error(f"Failed to load generator: {e}")
            return None

    def _load_module(self, name: str, file: Path, search_paths: list) -> ModuleType:
        spec = importlib.util.spec_from_file_location(
            name, file, submodule_search_locations=search_paths
        )
        if spec is None or spec.loader is None:
            raise ImportError(f"Could not create spec for {file}")

        module = importlib.util.module_from_spec(spec)
        sys.modules[name] = module
        spec.loader.exec_module(module)
        return module

    def _is_file_changed(self, file_path: Path) -> bool:
        file_key = str(file_path.absolute())
        current_sha1 = IO_UTILS.sha1(file_path)

        if file_key not in self._file_sha1_cache:
            self._file_sha1_cache[file_key] = current_sha1
            return True

        if self._file_sha1_cache[file_key] != current_sha1:
            self._file_sha1_cache[file_key] = current_sha1
            return True

        return False

    @property
    def filters_package_name(self) -> str:
        return self._filters_package_name
