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

from .settings import VERSION, ROOT_DIR


class Coder():

    def match_user(self, path: str, prefix1: str, suffix1: str, prefix2: str, suffix2: str) -> dict:
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

    def match_xmake_user(self, path: str) -> dict:
        """
        match user code in xmake.lua
        """
        return self.match_user(path, "----<", "\n", "----<", "\n")

    def match_cmake_user(self, path: str) -> dict:
        """
        match user code in CMakeLists.txt
        """
        return self.match_user(path, "##==<", "\n", "##==>", "\n")

    def match_c_user(self, path: str) -> dict:
        """
        match user code in c file
        """
        return self.match_user(path, "/\*\*<", " \*/", "/\*\*>", " \*/")

    def file_write(self, file_path: str, data: str):
        """
        write file
        """
        print(f"Create file {file_path} success!")
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(data.strip())
            file.write("\n")
        pass

    def generate_c(self, env: jinja2.Environment, module: str, dir: str, args: dict):
        """
        generate c file
        """
        if module == "main":
            path = f"{dir}/core/inc/main.h"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["UserCode"] = self.match_c_user(path)
            output = tpl.render(args, File=os.path.basename(path), Brief="main program body")
            self.file_write(path, output)

            path = f"{dir}/core/src/main.c"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["UserCode"] = self.match_c_user(path)
            output = tpl.render(args, File=os.path.basename(path), Brief="main program body")
            self.file_write(path, output)
        else:
            path = f"{dir}/core/inc/csplink/{module}.h"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["UserCode"] = self.match_c_user(path)
            output = tpl.render(args,
                                File=os.path.basename(path),
                                Brief=f"this file provides code for the {module} initialization")
            self.file_write(path, output)

            path = f"{dir}/core/src/{module}.c"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["UserCode"] = self.match_c_user(path)
            output = tpl.render(args,
                                File=os.path.basename(path),
                                Brief=f"this file provides code for the {module} initialization")
            self.file_write(path, output)

    def generate_mdk_arm_project(self, project: dict, path: str, minVersion: str) -> str:
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

    def generate_project(self, env: jinja2.Environment, dir: str, args: dict):
        """
        generate project file
        """
        if args["Project"]["TargetProject"] == "XMake":
            path = f"{dir}/xmake.lua"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["UserCode"] = self.match_xmake_user(path)
            output = tpl.render(args, File=os.path.basename(path), Brief="file automatically-generated by tool: [csp]")
            self.file_write(path, output)
        elif args["Project"]["TargetProject"] == "CMake":
            path = f"{dir}/CMakeLists.txt"
            tpl = env.get_template(f'{os.path.basename(path)}.j2')
            args["UserCode"] = self.match_cmake_user(path)
            output = tpl.render(args, File=os.path.basename(path), Brief="file automatically-generated by tool: [csp]")
            self.file_write(path, output)
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
            output = self.generate_mdk_arm_project(args["Project"], path, min_version)
            self.file_write(path, output)
        else:
            pass

    def deploy(self, package_dir: str, project: dict, output_dir: str) -> dict:
        """
        deploy
        """
        spec = importlib.util.spec_from_file_location("coder", f'{package_dir}/tools/coder/deploy.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        data = module.main(copy.deepcopy(project), copy.deepcopy(output_dir))
        return data

    def main(z, project_file: str, output_dir: str, repository_dir: str, package_dir, toolchains_dir: str):
        """
        main
        """
        project_json = {}
        with open(project_file, "r", encoding='utf-8') as file:
            project_json = json.loads(file.read())

        hal = project_json["Hal"]
        modules = project_json["Modules"]

        if package_dir == "":
            package_dir = f'{repository_dir}/library/{hal}/{project_json["HalVersion"]}'

        if not os.path.isdir(package_dir):
            print(f"error: {package_dir} is not directory! maybe package({hal}) not yet installed.")
            sys.exit(2)

        data = {
            "Author": "csplink coder",
            "Version": VERSION,
            "Project": project_json,
            "Time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "Year": time.strftime('%Y', time.localtime()),
            "ToolchainsPath": toolchains_dir if toolchains_dir != "" else None,
        }

        if not os.path.isdir(f"{output_dir}/core/src/"):
            os.makedirs(f"{output_dir}/core/src/")
        if not os.path.isdir(f"{output_dir}/core/inc/csplink"):
            os.makedirs(f"{output_dir}/core/inc/csplink")

        env = jinja2.Environment(loader=jinja2.FileSystemLoader(
            [f'{ROOT_DIR}/templates', f'{package_dir}/tools/coder/templates']),
                                 line_comment_prefix="//")

        filter_files = glob.glob(f"{package_dir}/tools/coder/filters/*.py")
        for file in filter_files:
            spec = importlib.util.spec_from_file_location(os.path.basename(file).split(".")[0], file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            functions = [name for name in dir(module) if callable(getattr(module, name))]
            for fun in functions:
                if not fun.startswith("_"):
                    function = getattr(module, fun)
                    env.filters[fun] = function

        generate_cfile(env, "main", output_dir, data)

        for module in modules:
            module = str.lower(module)
            generate_cfile(env, module, output_dir, data)

        generate_project(env, output_dir, data)

        deploy(package_dir, project_json, output_dir)
