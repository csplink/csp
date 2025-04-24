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
# @file        gen.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-07     xqyjlj       initial version
#


import glob
import hashlib
import importlib.util
import os
import re
import sys
import time
import xml.etree.ElementTree as etree
from pathlib import Path
from types import ModuleType

import jinja2
from loguru import logger

from .filters import FILTERS
from public.csp.project import Project
from utils.sys import SYS_UTILS
from public.csp.summary import Summary


class Coder:
    def __init__(self, project: Project, summary: Summary):
        self._project = project
        self._summary = summary
        self._files = {}
        self._generator = None

        sys.path = SYS_UTILS.sys_path() + [f"{project.hal_folder()}/tools/generator"]
        self._generator = self._load_generator()
        self._files = self._get_files_table()

    def generate(self, output: str = ""):
        if not self._check_hal_folder():
            return

        if output is None or not os.path.isdir(output):
            output = self._project.folder()

        data = self._get_loaded_data()
        env = self._get_environment()

        count = 0
        for file, info in self._files.items():
            if info.get("gen", True):
                count += 1
        index = 0
        for file, info in self._files.items():
            if info.get("gen", True):
                index += 1
                context = self._render(file, info, env, data)
                path = f"{output}/{file}".replace("\\", "/")
                if context:
                    changed = self._check_file_changed(path, context)
                    if changed:
                        with open(path, "w", encoding="utf-8") as file:
                            file.write(context)
                    else:
                        pass
                else:
                    logger.error(f"file {path!r} gen failed.")

        for file, info in self._files.items():
            if not info.get("gen", True):
                path = f"{output}/{file}".replace("\\", "/")
                if os.path.isfile(path):
                    os.remove(path)

        self._copy_library()

    def dump(self) -> dict:
        if len(self._files) == 0:
            return {}

        data = self._get_loaded_data()
        env = self._get_environment()

        context_table = {}
        count = 0
        for file, info in self._files.items():
            if info.get("gen", True):
                count += 1

        index = 0
        for file, info in self._files.items():
            if info.get("gen", True):
                index += 1
                suffix = Path(file).suffix
                context = self._render(file, info, env, data)
                if context is not None:
                    context_table[file] = context
                else:
                    logger.error(f"file {file!r} gen failed.")

            # self.dumped.emit(file)

        return context_table

    def deploy(self):
        if self._generator is None:
            return

        data = self._generator.deploy(self._project, self._project.folder())
        return data

    def files_list(self) -> list[str]:
        return list(self._files.keys())

    def _load_generator(self) -> ModuleType | None:
        if self._check_hal_folder():
            spec = importlib.util.spec_from_file_location(
                "coder", f"{self._project.hal_folder()}/tools/generator/generator.py"
            )
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return None

    def _get_files_table(self) -> dict[str, dict[str, str]]:
        if self._generator is None:
            return {}
        files = self._generator.files_table(self._project)
        return files

    def _copy_library(self):
        if self._generator is None:
            return
        output_dir = self._project.folder()
        self._generator.copy_library(
            self._project,
            output_dir,
            self._emit_copy_library_signal,
        )

    def _emit_copy_library_signal(
        self, path: str, index: int, count: int, success: bool, reason: str
    ):
        # self.copy_library_progress_updated.emit(path, index, count, success, reason) TODO:
        pass

    def _check_hal_folder(self) -> bool:
        if not os.path.isfile(
            f"{self._project.hal_folder()}/tools/generator/generator.py"
        ):
            logger.error(
                f"{self._project.hal_folder()} is not directory! maybe package({self._project.gen.hal}) not yet installed."
            )
            return False
        return True

    def _match_user(
        self, path: str, prefix1: str, suffix1: str, prefix2: str, suffix2: str
    ) -> dict:
        code = {}
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
                for s in re.findall(
                    f"{prefix1} user code begin (.*), do not change this comment!{suffix1}",
                    data,
                ):
                    matcher = f"{prefix1} user code begin {s}, do not change this comment!{suffix1}\n(.*){prefix2} user code end {s}, do not change this comment!{suffix2}"
                    result = str.rstrip(re.findall(matcher, data, re.S)[0])
                    if result:
                        code[s] = result
                        # code[s] = str.rstrip(result)
                        # # noinspection PyUnresolvedReferences
                        # if code[s] != '':
                        #     code[s] = code[s] + '\n'
                    else:
                        code[s] = ""
        return code

    def _render(
        self, path: str, info: dict, env: jinja2.Environment, args: dict
    ) -> str:
        abs_path = f"{self._project.folder()}/{path}"
        template_name = info.get("template")
        force = info.get("force", True)
        if force == False and os.path.isfile(abs_path):
            with open(abs_path, "r", encoding="utf-8") as fp:
                return fp.read()

        if template_name is None:
            template_name = f"{os.path.basename(path)}.j2"
        suffix = Path(abs_path).suffix
        context = ""
        if suffix == ".uvprojx":
            if self._generator is not None:
                mdk_cfg = self._generator.get_mdk(self._project, path)
                context = self._generate_mdk(mdk_cfg)
        else:
            try:
                template = env.get_template(template_name)
            except jinja2.exceptions.TemplateNotFound:
                return ""

            if suffix == ".h" or suffix == ".c":
                args["user_code"] = self._match_user(
                    abs_path, r"/\*\*<", r" \*/", r"/\*\*>", r" \*/"
                )
            elif Path(abs_path).name == "xmake.lua":
                args["user_code"] = self._match_user(abs_path, "----<", "", "---->", "")
            elif Path(abs_path).name == "CMakeLists.txt":
                args["user_code"] = self._match_user(abs_path, "##==<", "", "##==>", "")

            args["file"] = os.path.basename(path)
            args["brief"] = info.get(
                "brief", "file automatically-generated by tool: [csp]"
            )
            if "module" in info:
                args["module"] = info["module"]
            context = template.render({"CSP": args})
            context = context.strip() + "\n"

            time_pattern = (
                r"\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b"  # YYYY-MM-DD HH:MM:SS
            )
            gen_md5 = hashlib.md5(
                re.sub(time_pattern, "", context).encode("utf-8")
            ).hexdigest()
            file_context = ""
            if os.path.isfile(abs_path):
                with open(abs_path, "r", encoding="utf-8") as file:
                    file_context = file.read()
                    file_md5 = hashlib.md5(
                        re.sub(time_pattern, "", file_context).encode("utf-8")
                    ).hexdigest()
            else:
                file_md5 = ""

            if gen_md5 == file_md5:
                context = file_context

        return context

    def _get_environment(self) -> jinja2.Environment:
        package_folder = self._project.hal_folder()
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                [
                    SYS_UTILS.templates_folder(),
                    f"{package_folder}/tools/generator/templates",
                ]
            ),
            line_comment_prefix="//",
        )

        # env.add_extension("jinja2.ext.i18n")
        env.add_extension("jinja2.ext.debug")
        env.add_extension("jinja2.ext.do")
        env.add_extension("jinja2.ext.loopcontrols")

        files = glob.glob(f"{package_folder}/tools/generator/filters/*.py")
        for file in files:
            spec = importlib.util.spec_from_file_location(Path(file).stem, file)
            if spec is None or spec.loader is None:
                break
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            functions = [
                name for name in dir(module) if callable(getattr(module, name))
            ]
            for fun in functions:
                if not fun.startswith("_"):
                    function = getattr(module, fun)
                    env.filters[fun] = function
        env.filters.update(FILTERS)

        return env

    def _get_loaded_data(self) -> dict:
        data = {
            "author": "csplink coder",
            "version": SYS_UTILS.version(),
            "project": self._project,
            "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "year": time.strftime("%Y", time.localtime()),
            "platform": sys.platform,
            "summary": self._summary,
        }

        if self._project.gen.use_toolchains_package:
            data["toolchainsPath"] = self._project.toolchains_folder()

        return data

    def _check_file_changed(self, path: str, context: str) -> bool:
        gen_md5 = hashlib.md5(context.encode("utf-8")).hexdigest()
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as file:
                file_context = file.read()
                file_md5 = hashlib.md5(file_context.encode("utf-8")).hexdigest()
        else:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            file_md5 = ""
        if gen_md5 != file_md5:
            return True
        else:
            return False

    def _generate_mdk(self, mdk_cfg: dict):
        tree: etree.ElementTree = mdk_cfg["etree"]
        root: etree.Element = tree.getroot()  # type: ignore
        project = self._project
        project_name = project.name

        # target chip
        tree.find("Targets/Target/TargetOption/TargetCommonOption/Device").text = mdk_cfg["line"]  # type: ignore

        # vendor
        tree.find("Targets/Target/TargetOption/TargetCommonOption/Vendor").text = mdk_cfg["vendor"]  # type: ignore

        # cpu
        tree.find("Targets/Target/TargetOption/TargetCommonOption/Cpu").text = mdk_cfg["cpu"]  # type: ignore

        # project name
        tree.find("Targets/Target/TargetName").text = project_name  # type: ignore
        tree.find("Targets/Target/TargetOption/TargetCommonOption/OutputDirectory").text = "build_mdk\\"  # type: ignore
        tree.find("Targets/Target/TargetOption/TargetCommonOption/OutputName").text = project_name  # type: ignore
        tree.find("Targets/Target/TargetOption/TargetCommonOption/ListingPath").text = "./build_mdk/"  # type: ignore

        # defines
        define_node: etree.Element = tree.find(  # type: ignore
            "Targets/Target/TargetOption/TargetArmAds/Cads/VariousControls/Define"
        )
        pre_defines = define_node.text
        if pre_defines:
            pre_defines = set(pre_defines.split(","))
        else:
            pre_defines = set()
        defines = set()
        defines.update(pre_defines)
        defines.update(mdk_cfg["defines"])
        defines = sorted(defines)
        defines_content = ",".join(defines)
        define_node.text = defines_content

        # includes
        include_node: etree.Element = tree.find(  # type: ignore
            "Targets/Target/TargetOption/TargetArmAds/Cads/VariousControls/IncludePath"
        )
        pre_includes = include_node.text
        if pre_includes:
            pre_includes = set(pre_includes.split(";"))
        else:
            pre_includes = set()
        includes = set()
        includes.update(pre_includes)
        includes.update(mdk_cfg["includes"])
        includes = sorted(includes)
        includes_content = ";".join(includes)
        include_node.text = includes_content

        # files
        pre_files_group = {}
        groups_node: etree.Element = tree.find("Targets/Target/Groups")  # type: ignore
        group_nodes = groups_node.findall("Group")
        for group_node in group_nodes:
            group_name = group_node.find("GroupName").text  # type: ignore
            file_nodes = group_node.findall("Files/File")
            files = set()
            for file_node in file_nodes:
                file_name = file_node.find("FileName").text  # type: ignore
                file_type = file_node.find("FileType").text  # type: ignore
                file_path = file_node.find("FilePath").text.replace("\\", "/")  # type: ignore
                files.add(file_path)
            pre_files_group[group_name] = files
        files_group = {}
        files_group.update(pre_files_group)
        for group_name, files in mdk_cfg["files"].items():
            s = set()
            s.update(files)
            if group_name not in files_group:
                files_group[group_name] = s
            else:
                files_group[group_name].update(files)
        groups_node.clear()

        for group_name in sorted(files_group):
            self._add_mdk_group(
                groups_node, group_name, sorted(files_group[group_name])
            )
        self._mdk_xml_indent(root)
        content_bytes: bytes = etree.tostring(root, encoding="utf-8")
        content_str = (
            '<?xml version="1.0" encoding="UTF-8"?>\n' + content_bytes.decode()
        )
        return content_str

    def _get_mdk_filetype(self, file: str):
        file_type = 5

        if file.endswith(".cpp") or file.endswith(".cxx"):
            file_type = 8
        elif file.endswith(".c") or file.endswith(".C"):
            file_type = 1
        elif file.endswith(".s") or file.endswith(".S"):
            file_type = 2
        elif file.endswith(".h"):
            file_type = 5
        elif file.endswith(".lib"):
            file_type = 4
        elif file.endswith(".o"):
            file_type = 3

        return file_type

    def _add_mdk_group(self, groups_node: etree.Element, name: str, files: list):
        group = etree.SubElement(groups_node, "Group")
        group_name_node = etree.SubElement(group, "GroupName")
        group_name_node.text = name

        if len(files) == 0:
            return

        group_files_node = etree.SubElement(group, "Files")

        for file in files:
            file_name = os.path.basename(file)
            group_file_node = etree.SubElement(group_files_node, "File")

            group_file_name_node = etree.SubElement(group_file_node, "FileName")
            group_file_name_node.text = file_name

            group_file_type_node = etree.SubElement(group_file_node, "FileType")
            group_file_type_node.text = str(self._get_mdk_filetype(file_name))

            group_file_path_node = etree.SubElement(group_file_node, "FilePath")
            group_file_path_node.text = file

    def _mdk_xml_indent(self, elem: etree.Element, level=0):
        i = "\n" + level * "  "
        if len(elem):
            if not elem.text or not elem.text.strip():
                elem.text = i + "  "
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
            for elem in elem:
                self._mdk_xml_indent(elem, level + 1)
            if not elem.tail or not elem.tail.strip():
                elem.tail = i
        else:
            if level and (not elem.tail or not elem.tail.strip()):
                elem.tail = i
