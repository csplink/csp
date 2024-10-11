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
# @file        coder.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-11     xqyjlj       initial version
#

import copy
import glob
import hashlib
import importlib.util
import os
import re
import time
import xml.etree.ElementTree as etree

import jinja2
from PySide6.QtCore import QObject, Signal

from .project import PROJECT
from .settings import SETTINGS


class Coder(QObject):
    __data = {}

    dumped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def generate(self, packageDir: str):
        """
        generate
        """

        outputDir = os.path.dirname(PROJECT.path)

        if not os.path.isdir(f"{outputDir}/core/src/"):
            os.makedirs(f"{outputDir}/core/src/")
        if not os.path.isdir(f"{outputDir}/core/inc/csplink"):
            os.makedirs(f"{outputDir}/core/inc/csplink")

        data = self.dump(packageDir)
        for path, context in data.items():
            timePattern = r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b'  # YYYY-MM-DD HH:MM:SS
            genMd5 = hashlib.md5(re.sub(timePattern, '', context).encode('utf-8')).hexdigest()
            path = f"{outputDir}/{path}"
            if os.path.isfile(path):
                with open(path, "r", encoding='utf-8') as file:
                    fileContext = file.read()
                    fileMd5 = hashlib.md5(re.sub(timePattern, '', fileContext).encode('utf-8')).hexdigest()
            else:
                fileMd5 = ""
            if genMd5 != fileMd5:
                with open(path, "w", encoding='utf-8') as file:
                    file.write(context)

    def dump(self, packageDir: str) -> dict:
        """
        dump
        """

        hal = PROJECT.hal
        modules = PROJECT.modules

        if not os.path.isdir(packageDir):
            print(f"error: {packageDir} is not directory! maybe package({hal}) not yet installed.")
            return {}

        data = {
            "author": "csplink coder",
            "version": SETTINGS.VERSION,
            "project": PROJECT.origin,
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "year": time.strftime('%Y', time.localtime())
        }

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            [f'{os.getcwd()}/resource/templates', f'{packageDir}/tools/coder/templates']), line_comment_prefix="//")

        files = glob.glob(f"{packageDir}/tools/coder/filters/*.py")
        for file in files:
            spec = importlib.util.spec_from_file_location(os.path.basename(file).split(".")[0], file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            functions = [name for name in dir(module) if callable(getattr(module, name))]
            for fun in functions:
                if not fun.startswith("_"):
                    function = getattr(module, fun)
                    env.filters[fun] = function

        self.__dumpC(env, "main", data)
        for module in modules:
            self.__dumpC(env, str.lower(module), data)

        return self.__data

    def filesList(self) -> list[str]:
        files = [
            "core/inc/main.h",
            "core/src/main.c"
        ]

        modules = PROJECT.modules
        for module in modules:
            files.append(f"core/inc/csplink/{module}.h")
            files.append(f"core/inc/csplink/{module}.h")

        return files

    def __matchUser(self, path: str, prefix1: str, suffix1: str, prefix2: str, suffix2: str) -> dict:
        """
        match user code
        """
        code = {}
        if os.path.isfile(path):
            with open(path, "r", encoding='utf-8') as f:
                data = f.read()
                for s in re.findall(f"{prefix1} add user code begin (.*), do not change this comment!{suffix1}", data):
                    matcher = f"{prefix1} add user code begin {s}, do not change this comment!{suffix1}\n(.*){prefix2} add user code end {s}, do not change this comment!{suffix2}"
                    result = str.rstrip(re.findall(matcher, data, re.S)[0])
                    if result:
                        code[s] = str.rstrip(result)
                        if code[s] != "":
                            code[s] = code[s] + "\n"
                    else:
                        code[s] = ""
        return code

    def __matchXmakeUser(self, path: str) -> dict:
        """
        match user code in xmake.lua
        """
        return self.__matchUser(path, "----<", "\n", "----<", "\n")

    def __matchCmakeUser(self, path: str) -> dict:
        """
        match user code in CMakeLists.txt
        """
        return self.__matchUser(path, "##==<", "\n", "##==>", "\n")

    def __matchCUser(self, path: str) -> dict:
        """
        match user code in c file
        """
        return self.__matchUser(path, "/\*\*<", " \*/", "/\*\*>", " \*/")

    def __render(self, path: str, brief: str, env: jinja2.Environment, args: dict) -> str:
        absPath = f"{PROJECT.folder}/{path}"
        template = env.get_template(f'{os.path.basename(path)}.j2')
        args["userCode"] = self.__matchCUser(absPath)
        context = template.render(args, file=os.path.basename(path), brief=brief)
        context = context.strip() + "\n"

        timePattern = r'\b\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\b'  # YYYY-MM-DD HH:MM:SS
        genMd5 = hashlib.md5(re.sub(timePattern, '', context).encode('utf-8')).hexdigest()
        fileContext = ''
        if os.path.isfile(absPath):
            with open(absPath, "r", encoding='utf-8') as file:
                fileContext = file.read()
                fileMd5 = hashlib.md5(re.sub(timePattern, '', fileContext).encode('utf-8')).hexdigest()
        else:
            fileMd5 = ""

        if genMd5 == fileMd5:
            context = fileContext

        return context

    def __dumpC(self, env: jinja2.Environment, module: str, args: dict):
        """
        generate c file
        """
        if module == "main":
            path = "core/inc/main.h"
            self.__data[path] = self.__render(path, "main program body", env, args)
            self.dumped.emit(path)

            path = "core/src/main.c"
            self.__data[path] = self.__render(path, "main program body", env, args)
            self.dumped.emit(path)
        else:
            path = f"core/inc/csplink/{module}.h"
            self.__data[path] = self.__render(path, f"this file provides code for the {module} initialization", env,
                                              args)
            self.dumped.emit(path)

            path = f"core/src/{module}.c"
            self.__data[path] = self.__render(path, f"this file provides code for the {module} initialization", env,
                                              args)
            self.dumped.emit(path)

    def __generateMdkArmProject(self, project: dict, path: str, minVersion: str) -> str:
        """
        generate mdk arm
        """
        spec = importlib.util.spec_from_file_location("coder", f'{package_dir}/tools/coder/gen_mdk_arm.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if os.path.isfile(path):
            tree = etree.parse(path)
        else:
            tree = None

        return module.main(copy.deepcopy(project), copy.deepcopy(minVersion), copy.deepcopy(tree))

    def __generateProject(self, env: jinja2.Environment, folder: str, args: dict):
        """
        generate project file
        """
        if args["Project"]["TargetProject"] == "XMake":
            path = f"{folder}/xmake.lua"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__matchXmakeUser(path)
            output = tpl.render(args, file=os.path.basename(path), brief="file automatically-generated by tool: [csp]")
            self.__data[path] = output
        elif args["Project"]["TargetProject"] == "CMake":
            path = f"{folder}/CMakeLists.txt"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__matchCmakeUser(path)
            output = tpl.render(args, file=os.path.basename(path), brief="file automatically-generated by tool: [csp]")
            self.__data[path] = output
        elif args["Project"]["TargetProject"] == "MDK-Arm":
            if "TargetProjectMinVersion" in args["Project"].keys():
                minVersion = args["Project"]["TargetProjectMinVersion"]
            else:
                minVersion = "v5"
            if minVersion.lower().startswith("v5"):
                path = f"{folder}/mdk-arm/{args['Project']['Name']}.uvprojx"
            elif minVersion.lower().startswith("v4"):
                path = f"{folder}/mdk-arm/{args['Project']['Name']}.uvproj"
            else:
                path = f"{folder}/mdk-arm/{args['Project']['Name']}.uvprojx"
            if not os.path.isdir(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            output = self.__generateMdkArmProject(args["Project"], path, minVersion)
            self.__data[path] = output
        else:
            pass

    def __deploy(self, folder: str, project: dict, outputFolder: str) -> dict:
        """
        deploy
        """
        spec = importlib.util.spec_from_file_location("coder", f'{folder}/tools/coder/deploy.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        data = module.main(copy.deepcopy(project), copy.deepcopy(outputFolder))
        return data
