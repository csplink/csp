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

import jsonschema
import yaml
from loguru import logger

from .sys import SysUtils
from public.csp.project import Project


class ProjectUtils:
    def __init__(self):
        pass

    @staticmethod
    @logger.catch(default=False)
    def check_project(project: dict) -> bool:
        with open(
            os.path.join(SysUtils.database_folder(), "schema", "project.yml"),
            "r",
            encoding="utf-8",
        ) as f:
            schema = yaml.load(f.read(), Loader=yaml.FullLoader)
            jsonschema.validate(instance=project, schema=schema)
        return True

    @staticmethod
    @logger.catch(default=Project({}, ""))
    def load_project(file: str) -> Project:
        if os.path.isfile(file):
            with open(file, "r", encoding="utf-8") as f:
                project = yaml.load(f.read(), Loader=yaml.FullLoader)
                succeed = ProjectUtils.check_project(project)
            if succeed:
                return Project(project, file)
            else:
                return Project({}, "")
        else:
            logger.error(f"{file} is not file!")
            return Project({}, "")

    @staticmethod
    def check_generate_setting_valid(project: Project) -> tuple[bool, str]:
        if project.gen.use_toolchains_package and not os.path.isdir(
            project.toolchains_folder()
        ):
            if project.gen.toolchains != "default":
                return (
                    False,
                    f"the toolchains folder does not exist! maybe the toolchains '{project.gen.toolchains}:{project.gen.toolchains_version}' is not installed yet",
                )
        elif not os.path.isdir(project.hal_folder()):
            return (
                False,
                f"the hal folder does not exist! maybe the hal '{project.gen.hal}:{project.gen.hal_version}' is not installed yet",
            )
        elif project.gen.builder == "":
            return False, "the builder is not set"
        elif project.gen.builder_version == "":
            return (
                False,
                f"the builder {project.gen.builder!r} version is not set",
            )

        return True, ""
