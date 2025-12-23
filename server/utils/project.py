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
# @file        project.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-07     xqyjlj       initial version
#

import os
from pathlib import Path

import jsonschema
from loguru import logger
from packages.package import Package
from public.csp.project import Project, ProjectUserData
from ruamel.yaml import YAML

from .sys import SysUtils


class ProjectUtils:
    def __init__(self):
        pass

    @staticmethod
    def check_project(project: dict) -> bool:
        with open(
            SysUtils.database_folder() / "schema" / "project.yml",
            "r",
            encoding="utf-8",
        ) as f:
            yaml = YAML(typ="safe")
            schema = yaml.load(f.read())
            validator = jsonschema.Draft7Validator(schema)
            errors = sorted(validator.iter_errors(project), key=lambda e: e.path)
            if not errors:
                return True
            for e in errors:
                logger.error(
                    f"Project validation failed: {e.message!r} in {list(e.path)!r} with {list(e.schema_path)!r}"
                )
            return False

    @staticmethod
    def load_project_from_file(file: Path) -> Project:
        if file.is_file():
            with open(file, "r", encoding="utf-8") as f:
                yaml = YAML(typ="safe")
                try:
                    project: dict = yaml.load(f.read())
                except Exception as e:
                    logger.error(f"Failed to load project: {e}")
                    return Project({})
                return ProjectUtils.load_project(project, file)
        else:
            logger.error(f"{file} is not file!")
            return Project({})

    @staticmethod
    def load_project(project: dict, file: Path) -> Project:
        succeed = ProjectUtils.check_project(project)
        if succeed:
            p = Project(project)
            index = Package().index()
            hal_folder = index.path("hal", p.gen.hal, p.gen.halVersion)
            toolchains_folder = index.path(
                "toolchains", p.gen.toolchains, p.gen.toolchainsVersion
            )
            user_data = ProjectUserData(
                hal_folder,
                toolchains_folder,
                Path(file),
            )
            return Project(project, user_data)
        else:
            return Project({})

    @staticmethod
    def check_generate_setting_valid(project: Project) -> tuple[bool, str]:
        toolchains_folder = project.toolchains_folder()
        hal_folder = project.hal_folder()

        if toolchains_folder is None or (
            project.gen.useToolchainsPackage and not toolchains_folder.is_dir()
        ):
            if project.gen.toolchains != "default":
                return (
                    False,
                    f"the toolchains folder does not exist! maybe the toolchains '{project.gen.toolchains}:{project.gen.toolchainsVersion}' is not installed yet",
                )
        elif hal_folder is None or not hal_folder.is_dir():
            return (
                False,
                f"the hal folder does not exist! maybe the hal '{project.gen.hal}:{project.gen.halVersion}' is not installed yet",
            )
        elif project.gen.builder == "":
            return False, "the builder is not set"
        elif project.gen.builderVersion == "":
            return (
                False,
                f"the builder {project.gen.builder!r} version is not set",
            )

        return True, ""
