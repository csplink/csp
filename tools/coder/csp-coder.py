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
# @file        csp-coder.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-03-22     xqyjlj       initial version
#

import xml.etree.ElementTree as etree
import re
import copy
import time
import os, sys, getopt
import json
import jinja2
import importlib.util
import glob

script_dir = os.path.dirname(__file__)
version = "v0.0.0.2"

sys.path.append(script_dir)
import helper_keil as keil


def match_xmake_user(file_path: str) -> dict:
    """
    match user code in xmake.lua
    """
    user_code = {}
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            data = file.read()
            for s in re.findall("----< add user code begin (.*), do not change this comment!\n", data):
                matcher = f"----< add user code begin {s}, do not change this comment!\n(.*)----> add user code end {s}, do not change this comment!\n"
                result = str.rstrip(re.findall(matcher, data, re.S)[0])
                if result:
                    user_code[s] = str.rstrip(result)
                    if user_code[s] != "":
                        user_code[s] = user_code[s] + "\n"
                else:
                    user_code[s] = ""
    return user_code


def match_cmake_user(file_path: str) -> dict:
    """
    match user code in CMakeLists.txt
    """
    user_code = {}
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            data = file.read()
            for s in re.findall("##==< add user code begin (.*), do not change this comment!\n", data):
                matcher = f"##==< add user code begin {s}, do not change this comment!\n(.*)##==> add user code end {s}, do not change this comment!\n"
                result = str.rstrip(re.findall(matcher, data, re.S)[0])
                if result:
                    user_code[s] = str.rstrip(result)
                    if user_code[s] != "":
                        user_code[s] = user_code[s] + "\n"
                else:
                    user_code[s] = ""
    return user_code


def match_cfile_user(file_path: str) -> dict:
    """
    match user code in c file
    """
    user_code = {}
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            data = file.read()
            for s in re.findall("/\*\*< add user code begin (.*), do not change this comment! \*/", data):
                matcher = f"/\*\*< add user code begin {s}, do not change this comment! \*/\n(.*)/\*\*> add user code end {s}, do not change this comment! \*/"
                result = str.rstrip(re.findall(matcher, data, re.S)[0])
                if result:
                    user_code[s] = str.rstrip(result)
                    if user_code[s] != "":
                        user_code[s] = user_code[s] + "\n"
                else:
                    user_code[s] = ""
    return user_code


def file_write(file_path: str, data: str):
    """
    write file
    """

    print(f"Create file {file_path} success!")
    with open(file_path, "w", encoding='utf-8') as file:
        file.write(data.strip())
        file.write("\n")
    pass


def generate_cfile(env: jinja2.Environment, module: str, output_dir: str, args: dict):
    """
    generate c file
    """
    if module == "main":
        path = f"{output_dir}/core/inc/main.h"
        tpl = env.get_template(f'{os.path.basename(path)}.j2')
        args["UserCode"] = match_cfile_user(path)
        output = tpl.render(args, File=os.path.basename(path), Brief="main program body")
        file_write(path, output)

        path = f"{output_dir}/core/src/main.c"
        tpl = env.get_template(f'{os.path.basename(path)}.j2')
        args["UserCode"] = match_cfile_user(path)
        output = tpl.render(args, File=os.path.basename(path), Brief="main program body")
        file_write(path, output)
    else:
        path = f"{output_dir}/core/inc/csplink/{module}.h"
        tpl = env.get_template(f'{os.path.basename(path)}.j2')
        args["UserCode"] = match_cfile_user(path)
        output = tpl.render(args,
                            File=os.path.basename(path),
                            Brief=f"this file provides code for the {module} initialization")
        file_write(path, output)

        path = f"{output_dir}/core/src/{module}.c"
        tpl = env.get_template(f'{os.path.basename(path)}.j2')
        args["UserCode"] = match_cfile_user(path)
        output = tpl.render(args,
                            File=os.path.basename(path),
                            Brief=f"this file provides code for the {module} initialization")
        file_write(path, output)


def generate_mdk_arm_project(args: dict, target_file: str, min_version: str) -> str:
    """
    generate mdk arm
    """
    project = args["Project"]

    spec = importlib.util.spec_from_file_location("coder", f'{package_dir}/tools/coder/gen_mdk_arm.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    if os.path.isfile(target_file):
        tree = etree.parse(target_file)
    else:
        tree = None

    return module.main(copy.deepcopy(project), copy.deepcopy(min_version), copy.deepcopy(tree), keil)


def generate_project(env: jinja2.Environment, output_dir: str, args: dict):
    """
    generate project file
    """
    if args["Project"]["TargetProject"] == "XMake":
        path = f"{output_dir}/xmake.lua"
        tpl = env.get_template(f'{os.path.basename(path)}.j2')
        args["UserCode"] = match_xmake_user(path)
        output = tpl.render(args, File=os.path.basename(path), Brief="file automatically-generated by tool: [csp]")
        file_write(path, output)
    elif args["Project"]["TargetProject"] == "CMake":
        path = f"{output_dir}/CMakeLists.txt"
        tpl = env.get_template(f'{os.path.basename(path)}.j2')
        args["UserCode"] = match_cmake_user(path)
        output = tpl.render(args, File=os.path.basename(path), Brief="file automatically-generated by tool: [csp]")
        file_write(path, output)
    elif args["Project"]["TargetProject"] == "MDK-Arm":
        if "TargetProjectMinVersion" in args["Project"].keys():
            min_version = args["Project"]["TargetProjectMinVersion"]
        else:
            min_version = "v5"
        if min_version.lower().startswith("v5"):
            path = f"{output_dir}/mdk-arm/{args['Project']['Name']}.uvprojx"
        elif min_version.lower().startswith("v4"):
            path = f"{output_dir}/mdk-arm/{args['Project']['Name']}.uvproj"
        else:
            path = f"{output_dir}/mdk-arm/{args['Project']['Name']}.uvprojx"
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        output = generate_mdk_arm_project(args, path, min_version)
        file_write(path, output)
    else:
        pass


def deploy(package_dir: str, project: dict, output_dir: str) -> dict:
    """
    deploy
    """
    spec = importlib.util.spec_from_file_location("coder", f'{package_dir}/tools/coder/deploy.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    data = module.main(copy.deepcopy(project), copy.deepcopy(output_dir))
    return data


def main(project_file: str, output_dir: str, repository_dir: str, package_dir, toolchains_dir: str):
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
        "Version": version,
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
        [f'{script_dir}/templates', f'{package_dir}/tools/coder/templates']),
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


def help():
    """
    Print the help message.
    """
    print("usage: " + os.path.basename(__file__) + " [<options>] ")
    print("")
    print("    -h, --help               print this help.")
    print("    -f, --file               csp project file path.")
    print("    -o, --output             set the output directory.")
    print("    -r, --repository         repository dir.")
    print("    -d, --package_dir        package dir.")
    print("    -t, --toolchains_dir     toolchains dir.")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:o:r:d:t:",
                                   ["help", "file=", "output=", "repository=", "package_dir=", "toolchains_dir="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    file = ""
    output = ""
    repository = ""
    package_dir = ""
    toolchains_dir = ""
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-r", "--repository"):
            repository = arg
        elif opt in ("-d", "--package_dir"):
            package_dir = arg
        elif opt in ("-t", "--toolchains_dir"):
            toolchains_dir = arg

    if file == "" or (repository == "" and package_dir == ""):
        help()
        sys.exit(2)

    if not os.path.isfile(file):
        print(f"error: {file} is not file!")
        sys.exit(2)

    if repository != "" and (not os.path.isdir(repository)):
        print(f"error: {repository} is not directory!")
        sys.exit(2)

    if package_dir != "" and (not os.path.isdir(package_dir)):
        print(f"error: {package_dir} is not directory!")
        sys.exit(2)

    if toolchains_dir != "" and (not os.path.isdir(toolchains_dir)):
        print(f"error: {toolchains_dir} is not directory!")
        sys.exit(2)

    if output == "":
        output = os.path.dirname(file)

    main(file, output, repository, package_dir, toolchains_dir)
