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
# @file        csp-server.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-07-06     xqyjlj       initial version
#

import argparse
import datetime
import os
import sys
from pathlib import Path
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
from loguru import logger
import difflib
from typing import TypedDict


from coder.coder import Coder
from public.csp.project import Project
from utils.net import NetUtils
from utils.sys import SysUtils
from utils.project import ProjectUtils
from utils.summary import SummaryUtils
from utils.io import IoUtils

app = Flask("csp-server")
CORS(app)


@app.route("/api/coder/dump", methods=["POST"])
def coder_dump():
    class Args(TypedDict):
        content: dict | None
        path: str | None
        diff: bool

    payload: Args | None = request.json
    if payload is None:
        abort(400, description="Missing JSON payload.")

    arg_content = payload.get("content")
    arg_path = payload.get("path")
    arg_diff = payload.get("diff", False)
    if not isinstance(arg_path, str):
        abort(
            400,
            description="'path' must be a file path string",
        )

    if not arg_content is None:
        if not ProjectUtils.check_project(arg_content):
            abort(400, description="'project' does not conform to expected schema.")

        project_data = arg_content
        project = Project(project_data, arg_path)
    else:
        project = ProjectUtils.load_project(arg_path)
        if not project.origin:
            abort(400, description=f"Failed to load file: {arg_path}")

    summary = SummaryUtils.load_summary(project.vendor, project.target_chip)
    coder = Coder(project, summary)

    files = {}

    for file, data in coder.dump().items():
        files[file] = {"content": data}

    if arg_diff:
        if arg_path is not None and arg_content is not None:
            for file, data in files.items():
                lines = IoUtils.readlines(str(Path(project.folder()) / file))
                text: str = data["content"]
                arg_diff = difflib.unified_diff(
                    lines,
                    text.splitlines(keepends=True),
                    fromfile=file,
                    tofile=file,
                    lineterm="",
                )
                files[file]["diff"] = "".join(arg_diff)

    return jsonify({"files": files})


# region main


def handle_gen(args: argparse.Namespace, parser: argparse.ArgumentParser):
    file: str = args.file
    progress: bool = args.progress
    output: str = args.output

    project = ProjectUtils.load_project(file)
    summary = SummaryUtils.load_summary(project.vendor, project.target_chip)
    coder = Coder(project, summary)
    coder.generate(output)
    print(project.name)


def handle_install(args: argparse.Namespace, parser: argparse.ArgumentParser):
    pass


def handle_uninstall(args: argparse.Namespace, parser: argparse.ArgumentParser):
    pass


def handle_list(args: argparse.Namespace, parser: argparse.ArgumentParser):
    pass


def handle_serve(args: argparse.Namespace, parser: argparse.ArgumentParser):
    port = NetUtils.find_local_available_port(5000)
    http_server = WSGIServer(("127.0.0.1", port), app)
    print(port)
    http_server.serve_forever()


def main():
    try:
        parser = create_parser()
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        sys.exit(1)

    today = datetime.datetime.today()
    logger.add(
        f"{SysUtils.exe_folder()}/log/csp-server-{today.year}-{today.month}.log",
        rotation="10 MB",
    )

    if args.command:
        args.func(args, parser)
    else:
        if args.version:
            print(
                f"csp version {SysUtils.version()}. a fully open source chip configuration software system"
            )
            print(f"copyright (C) 2023-present xqyjlj, csplink.top, xqyjlj@126.com")
        else:
            parser.print_help()


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "---\n"
            "CSP Server - Backend service for the open-source Chip Support Platform (CSP).\n\n"
            "This server provides APIs and services for configuring chip drivers, parameters, "
            "and device settings in a flexible and extensible way.\n\n"
            "Source code: https://github.com/csplink/csp\n"
            "Project homepage: https://csplink.top\n"
            "---\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="subparsers", dest="command", required=False
    )

    gen = subparsers.add_parser(
        "gen", help="Generate source code and configuration files from a CSP project"
    )
    gen.add_argument(
        "-f",
        "--file",
        required=True,
        help="The path to the CSP project file (e.g., project.csp)",
    )
    gen.add_argument(
        "-o",
        "--output",
        required=False,
        help="The output directory where generated code will be saved. Defaults to current directory if not specified",
    )
    gen.add_argument(
        "--progress",
        required=False,
        action="store_true",
        help="Show a progress bar during code generation",
    )
    gen.set_defaults(func=handle_gen)
    # ------------------------------------------------------------------------ #

    install = subparsers.add_parser(
        "install", help="Install a CSP package into the local environment"
    )

    install.add_argument(
        "-p",
        "--path",
        required=True,
        help="The path to the CSP package file or directory to install",
    )

    install.add_argument(
        "--progress",
        required=False,
        action="store_true",
        help="Show a progress bar during installation",
    )

    install.add_argument(
        "--verbose",
        required=False,
        action="store_true",
        help="Enable detailed output for debugging",
    )
    install.set_defaults(func=handle_install)
    # ------------------------------------------------------------------------ #

    uninstall = subparsers.add_parser(
        "uninstall", help="Uninstall a specific CSP package from the local environment"
    )
    uninstall.add_argument(
        "-t",
        "--type",
        required=True,
        help="The type of the CSP package to uninstall (e.g., 'hal', 'toolchains', 'components')",
    )
    uninstall.add_argument(
        "-n", "--name", required=True, help="The name of the CSP package to uninstall"
    )
    uninstall.add_argument(
        "-v",
        "--version",
        required=True,
        help="The version of the CSP package to uninstall (e.g., '1.0.0')",
    )
    uninstall.set_defaults(func=handle_uninstall)
    # ------------------------------------------------------------------------ #

    list_ = subparsers.add_parser(
        "list", help="List installed CSP packages in the local environment"
    )
    list_.add_argument(
        "-t",
        "--type",
        required=False,
        help="Filter packages by type (e.g., 'hal', 'toolchains', 'components')",
    )
    list_.add_argument(
        "--json",
        required=False,
        action="store_true",
        help="Output the list in JSON format",
    )
    list_.set_defaults(func=handle_list)

    # ------------------------------------------------------------------------ #

    serve = subparsers.add_parser("serve", help="Start the CSP backend server")
    serve.add_argument(
        "-p", "--port", required=True, help="The port to listen on (e.g., 5000)"
    )
    serve.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with more verbose output",
    )
    serve.set_defaults(func=handle_serve)
    # ------------------------------------------------------------------------ #

    parser.add_argument(
        "-v",
        "--version",
        required=False,
        help="print the version number",
        action="store_true",
    )

    return parser


if __name__ == "__main__":
    main()

# endregion
