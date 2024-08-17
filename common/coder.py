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

import xml.etree.ElementTree as etree
import re, copy, time, json, jinja2, importlib.util, glob
import os, sys

from common.project import PROJECT

from .settings import VERSION


class Coder():

    m_data = {}

    def __match_user(self, path: str, prefix1: str, suffix1: str, prefix2: str, suffix2: str) -> dict:
        """
        match user code
        """
        user_code = {}
        if os.path.isfile(path):
            with open(path, "r", encoding='utf-8') as f:
                data = f.read()
                for s in re.findall(f"{prefix1} add user code begin (.*), do not change this comment!{suffix1}", data):
                    matcher = f"{prefix1} add user code begin {s}, do not change this comment!{suffix1}\n(.*){prefix2} add user code end {s}, do not change this comment!{suffix2}"
                    result = str.rstrip(re.findall(matcher, data, re.S)[0])
                    if result:
                        user_code[s] = str.rstrip(result)
                        if user_code[s] != "":
                            user_code[s] = user_code[s] + "\n"
                    else:
                        user_code[s] = ""
        return user_code

    def __match_xmake_user(self, path: str) -> dict:
        """
        match user code in xmake.lua
        """
        return self.__match_user(path, "----<", "\n", "----<", "\n")

    def __match_cmake_user(self, path: str) -> dict:
        """
        match user code in CMakeLists.txt
        """
        return self.__match_user(path, "##==<", "\n", "##==>", "\n")

    def __match_c_user(self, path: str) -> dict:
        """
        match user code in c file
        """
        return self.__match_user(path, "/\*\*<", " \*/", "/\*\*>", " \*/")

    def __generate_c(self, env: jinja2.Environment, module: str, args: dict):
        """
        generate c file
        """
        if module == "main":
            path = f"core/inc/main.h"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__match_c_user(f"{PROJECT.dir}/{path}")
            main_h = tpl.render(args, file=os.path.basename(path), brief="main program body")
            self.m_data[path] = main_h.strip() + "\n"

            path = f"core/src/main.c"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__match_c_user(f"{PROJECT.dir}/{path}")
            main_c = tpl.render(args, file=os.path.basename(path), brief="main program body")
            self.m_data[path] = main_c.strip() + "\n"
        else:
            path = f"core/inc/csplink/{module}.h"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__match_c_user(f"{PROJECT.dir}/{path}")
            module_h = tpl.render(args,
                                  file=os.path.basename(path),
                                  brief=f"this file provides code for the {module} initialization")
            self.m_data[path] = module_h.strip() + "\n"

            path = f"core/src/{module}.c"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__match_c_user(f"{PROJECT.dir}/{path}")
            module_c = tpl.render(args,
                                  file=os.path.basename(path),
                                  brief=f"this file provides code for the {module} initialization")
            self.m_data[path] = module_c.strip() + "\n"

    def __generate_mdk_arm_project(self, project: dict, path: str, minVersion: str) -> str:
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

    def __generate_project(self, env: jinja2.Environment, dir: str, args: dict):
        """
        generate project file
        """
        if args["Project"]["TargetProject"] == "XMake":
            path = f"{dir}/xmake.lua"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__match_xmake_user(path)
            output = tpl.render(args, file=os.path.basename(path), brief="file automatically-generated by tool: [csp]")
            self.__file_write(path, output)
        elif args["Project"]["TargetProject"] == "CMake":
            path = f"{dir}/CMakeLists.txt"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["userCode"] = self.__match_cmake_user(path)
            output = tpl.render(args, file=os.path.basename(path), brief="file automatically-generated by tool: [csp]")
            self.__file_write(path, output)
        elif args["Project"]["TargetProject"] == "MDK-Arm":
            if "TargetProjectMinVersion" in args["Project"].keys():
                min_version = args["Project"]["TargetProjectMinVersion"]
            else:
                min_version = "v5"
            if min_version.lower().startswith("v5"):
                path = f"{dir}/mdk-arm/{args['Project']['Name']}.uvprojx"
            elif min_version.lower().startswith("v4"):
                path = f"{dir}/mdk-arm/{args['Project']['Name']}.uvproj"
            else:
                path = f"{dir}/mdk-arm/{args['Project']['Name']}.uvprojx"
            if not os.path.isdir(os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            output = self.__generate_mdk_arm_project(args["Project"], path, min_version)
            self.__file_write(path, output)
        else:
            pass

    def __deploy(self, dir: str, project: dict, output_dir: str) -> dict:
        """
        deploy
        """
        spec = importlib.util.spec_from_file_location("coder", f'{dir}/tools/coder/deploy.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        data = module.main(copy.deepcopy(project), copy.deepcopy(output_dir))
        return data

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
            with open(f"{outputDir}/{path}", "w", encoding='utf-8') as file:
                file.write(context)

    def dump(self, packageDir: str) -> dict:
        """
        dump
        """

        hal = PROJECT.summary.hal
        modules = PROJECT.modules

        if not os.path.isdir(packageDir):
            print(f"error: {packageDir} is not directory! maybe package({hal}) not yet installed.")
            return {}

        data = {
            "author": "csplink coder",
            "version": VERSION,
            "project": PROJECT.origin,
            "time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "year": time.strftime('%Y', time.localtime())
        }

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            [f'{os.getcwd()}/resource/templates', f'{packageDir}/tools/coder/templates']),
                                 line_comment_prefix="//")

        filter_files = glob.glob(f"{packageDir}/tools/coder/filters/*.py")
        for file in filter_files:
            spec = importlib.util.spec_from_file_location(os.path.basename(file).split(".")[0], file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            functions = [name for name in dir(module) if callable(getattr(module, name))]
            for fun in functions:
                if not fun.startswith("_"):
                    function = getattr(module, fun)
                    env.filters[fun] = function

        self.__generate_c(env, "main", data)
        for module in modules:
            self.__generate_c(env, str.lower(module), data)

        return self.m_data
