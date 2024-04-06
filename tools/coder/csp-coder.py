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

import re
import copy
import time
import os, sys, getopt
import json
import jinja2

script_dir = os.path.dirname(__file__)
version = "v0.0.0.1"


def match_xmake_user(file_path: str) -> dict:
    """
    match user code in xmake.lua
    """
    user_code = {}
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding='utf-8') as file:
            data = file.read()
            for s in re.findall("----< add user code begin (.*)\n", data):
                matcher = f"----< add user code begin {s}\n(.*)----> add user code end {s}\n"
                result = str.rstrip(re.findall(matcher, data, re.S)[0])
                if result:
                    user_code[s] = str.rstrip(result)
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
            for s in re.findall("/\*\*< add user code begin (.*) \*/", data):
                matcher = f"/\*\*< add user code begin {s} \*/\n(.*)/\*\*> add user code end {s} \*/"
                result = str.rstrip(re.findall(matcher, data, re.S)[0])
                if result:
                    user_code[s] = str.rstrip(result)
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
        pass
    elif args["Project"]["TargetProject"] == "MDK-Arm":
        pass
    else:
        pass

    path = f"{output_dir}/CMakeLists.txt"
    tpl = env.get_template(f'{os.path.basename(path)}.j2')
    args["UserCode"] = match_xmake_user(path)
    output = tpl.render(args, File=os.path.basename(path), Brief="file automatically-generated by tool: [csp]")
    file_write(path, output)

    path = f"{output_dir}/Makefile"
    tpl = env.get_template(f'{os.path.basename(path)}.j2')
    args["UserCode"] = match_xmake_user(path)
    output = tpl.render(args, File=os.path.basename(path), Brief="file automatically-generated by tool: [csp]")
    file_write(path, output)


def param_check():
    """
    param check
    """
    pass


def parse(project: dict) -> dict:
    """
    parse
    """
    import coder
    data = coder.parse(copy.deepcopy(project))
    return data


def deploy(project: dict, output_dir: str) -> dict:
    """
    deploy
    """
    import coder
    data = coder.deploy(copy.deepcopy(project), output_dir)
    return data


def main(project_file: str, output_dir: str, repositories_dir: str):
    """
    main
    """
    project_json = {}
    with open(project_file, "r", encoding='utf-8') as file:
        project_json = json.loads(file.read())

    hal = project_json["Hal"]
    modules = project_json["Modules"]
    package_dir = f'{repositories_dir}/{hal}/{project_json["HalVersion"]}'

    if not os.path.isdir(package_dir):
        print(f"error: {package_dir} is not directory! maybe package({hal}) not yet installed.")
        sys.exit(2)

    sys.path.append(f'{package_dir}/tools/coder')

    coder_data = parse(project_json)

    data = {
        "Base": {
            "Author": "csplink coder",
            "Version": version
        },
        "Project": project_json,
        "Time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
        "Year": time.strftime('%Y', time.localtime()),
        "CoderData": coder_data
    }

    if not os.path.isdir(f"{output_dir}/core/src/"):
        os.makedirs(f"{output_dir}/core/src/")
    if not os.path.isdir(f"{output_dir}/core/inc/csplink"):
        os.makedirs(f"{output_dir}/core/inc/csplink")

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader([f'{script_dir}/templates', f'{package_dir}/tools/coder/templates']))

    generate_cfile(env, "main", output_dir, data)

    for module in modules:
        module = str.lower(module)
        generate_cfile(env, module, output_dir, data)

    generate_project(env, output_dir, data)

    deploy(project_json, output_dir)


def help():
    """
    Print the help message.
    """
    print("usage: " + os.path.basename(__file__) + " [<options>] ")
    print("")
    print("    -h, --help               print this help.")
    print("    -f, --file               csp project file path.")
    print("    -o, --output             set the output directory.")
    print("    -r, --repositories       repositories dir.")


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:o:r:", ["help", "file=", "output=", "repositories="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    file = ""
    output = ""
    repositories = ""
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("-f", "--file"):
            file = arg
        elif opt in ("-o", "--output"):
            output = arg
        elif opt in ("-r", "--repositories"):
            repositories = arg

    if file == "" or repositories == "":
        help()
        sys.exit(2)

    if not os.path.isfile(file):
        print(f"error: {file} is not file!")
        sys.exit(2)

    if not os.path.isdir(repositories):
        print(f"error: {repositories} is not directory!")
        sys.exit(2)

    if output == "":
        output = os.path.dirname(file)

    main(file, output, repositories)