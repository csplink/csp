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
# 2025-07-30     xqyjlj       use click
#

import datetime
import os
import sys
from pathlib import Path

import click
import proto.sio_coder_dump_pb2 as sio_coder_dump_pb2
import proto.sio_coder_generate_pb2 as sio_coder_generate_pb2
import proto.sio_package_description_pb2 as sio_package_description_pb2
import proto.sio_package_install_pb2 as sio_package_install_pb2
import proto.sio_package_list_pb2 as sio_package_list_pb2
import proto.sio_package_uninstall_pb2 as sio_package_uninstall_pb2
from actions import (
    action_coder_dump,
    action_coder_generate,
    action_package_description,
    action_package_install,
    action_package_list,
    action_package_make,
    action_package_uninstall,
    action_tools_candb_dump,
    action_tools_check_ip,
    action_tools_cmx_ip,
    action_tools_csp2filter,
    action_tools_yaml2json,
)
from flask import Flask, abort, jsonify, request
from flask_socketio import SocketIO
from google.protobuf.json_format import MessageToDict
from loguru import logger
from utils.ip import IpUtils
from utils.net import NetUtils
from utils.project import ProjectUtils
from utils.sys import SysUtils

app = Flask("csp-server")
socketio = SocketIO(app, cors_allowed_origins="*")
client_online = {}


@app.route("/api/coder/dump", methods=["POST"])
def api_coder_dump():
    payload = request.json
    if payload is None:
        logger.error("Called with missing JSON payload")
        abort(400, description="Missing JSON payload.")

    logger.trace(f"Call api/coder/dump with {payload!r}")

    arg_content = payload.get("content")
    arg_path = payload.get("path")
    arg_diff = payload.get("diff", False)

    if not isinstance(arg_path, str):
        logger.error(f"Called with invalid path: {arg_path!r}")
        abort(400, description="'path' must be a file path string")

    if arg_content:
        if not ProjectUtils.check_project(arg_content):
            logger.error(f"Called with invalid content: {arg_content!r}")
            abort(400, description="'project' does not conform to expected schema.")
        project = ProjectUtils.load_project(arg_content, arg_path)
    else:
        project = ProjectUtils.load_project_from_file(arg_path)
        if not project.origin:
            logger.error(f"Called with invalid path: {arg_path!r}")
            abort(400, description=f"Failed to load file: {arg_path}")
    try:
        files = action_coder_dump(project, arg_diff, arg_path, arg_content)
        if files is None or len(files) == 0:
            abort(500, description="Unknown error, please see more in server log")
        return jsonify({"files": files})
    except Exception as e:
        logger.exception(f"Dump failed: {str(e)!r}")
        abort(500, description=str(e))


@app.route("/api/coder/generate", methods=["POST"])
def api_coder_generate():
    payload = request.json
    if payload is None:
        logger.error("Called with missing JSON payload")
        abort(400, description="Missing JSON payload.")

    logger.trace(f"Call api/coder/generate with {payload!r}")

    arg_path = payload.get("path")
    arg_output = payload.get("output")

    if not isinstance(arg_path, str):
        logger.error(f"Called with invalid file path: {arg_path!r}")
        abort(400, description="'file' must be a file path string")

    try:
        project = ProjectUtils.load_project_from_file(arg_path)
        if not project.origin:
            logger.error(f"Called with invalid file path: {arg_path!r}")
            abort(400, description=f"Failed to load file: {arg_path}")

        result = action_coder_generate(project, arg_output, False)
        if not result:
            abort(500, description="Generation failed, please see more in server log")
        return jsonify({"success": True})
    except Exception as e:
        logger.exception(f"Generate failed: {str(e)!r}")
        abort(500, description=str(e))


@app.route("/api/package/install", methods=["POST"])
def api_package_install():
    payload = request.json
    if payload is None:
        logger.error("Called with missing JSON payload")
        abort(400, description="Missing JSON payload.")

    arg_path = payload.get("path")

    logger.trace(f"Call api/package/install with {payload!r}")

    if not isinstance(arg_path, str):
        logger.error(f"Called with invalid path: {arg_path!r}")
        abort(400, description="'path' must be a file path string")

    try:
        package_desc = action_package_install(arg_path, False, False)
        if package_desc is None:
            abort(500, description="Unknown error, please see more in server log")
        return jsonify(package_desc.origin)
    except Exception as e:
        logger.exception(f"Install failed: {str(e)!r}")
        abort(500, description=str(e))


@app.route("/api/package/list", methods=["GET"])
def api_package_list():
    logger.trace(f"Call api/package/list")
    try:
        result = action_package_list()
        return jsonify(result)
    except Exception as e:
        logger.exception(f"List failed: {str(e)!r}")
        abort(500, description=str(e))


@app.route("/api/client/online", methods=["GET"])
def online():
    payload = request.args.to_dict()

    arg_id = payload.get("id")

    logger.trace(f"Call api/client/online with {payload!r}")

    if not isinstance(arg_id, str):
        logger.error(f"Called with invalid id: {arg_id!r}")
        abort(400, description="'id' must be a string")

    client_online.setdefault(arg_id, {"time": datetime.datetime.now()})

    return jsonify({"success": True})


@app.route("/api/client/offline", methods=["GET"])
def offline():
    payload = request.args.to_dict()

    arg_id = payload.get("id")

    logger.trace(f"Call api/client/offline with {payload!r}")

    if not isinstance(arg_id, str):
        logger.error(f"Called with invalid id: {arg_id!r}")
        abort(400, description="'id' must be a string")

    if arg_id in client_online:
        del client_online[arg_id]

    if len(client_online.keys()) == 0:
        logger.info("No client online, the server will be closed.")
        os._exit(0)

    return jsonify({"success": True})


# ------------------------------------------------------------------------------


@socketio.on("sio/coder/dump")
def sio_coder_dump(data: bytes):
    # args: (content: str, path: str, diff: bool=False)
    # emit:
    #   coder/dump.result (success: bool, result?: dict, error?: str)
    #   coder/dump.progress (count: int, index: int, file: str)
    sid: str = request.sid  # type: ignore

    msg = sio_coder_dump_pb2.SioCoderDumpRequest()
    msg.ParseFromString(data)
    arg_content = MessageToDict(msg.content)
    arg_path = msg.path
    arg_diff = msg.diff

    logger.trace(
        f"{sid!r} calling sio/coder/dump with content:{arg_content!r}, path:{arg_path!r}, diff:{arg_diff!r}"
    )

    if not isinstance(arg_path, str):
        logger.error(f"Called with invalid path: {arg_path!r}")
        socketio.emit(
            "coder/dump.result",
            sio_coder_dump_pb2.SioCoderDumpResponse(
                success=False,
                error="'path' must be a file path string",
            ).SerializeToString(),
            to=sid,
        )
        return

    if arg_content:
        if not ProjectUtils.check_project(arg_content):
            logger.error(f"Called with invalid content: {arg_content!r}")
            socketio.emit(
                "coder/dump.result",
                sio_coder_dump_pb2.SioCoderDumpResponse(
                    success=False,
                    error="'project' does not conform to expected schema.",
                ).SerializeToString(),
                to=sid,
            )
            return
        project = ProjectUtils.load_project(arg_content, arg_path)
    else:
        project = ProjectUtils.load_project_from_file(arg_path)
        if not project.origin:
            logger.error(f"Called with invalid path: {arg_path!r}")
            socketio.emit(
                "coder/dump.result",
                sio_coder_dump_pb2.SioCoderDumpResponse(
                    success=False,
                    error=f"Failed to load file: {arg_path}",
                ).SerializeToString(),
                to=sid,
            )
            return

    try:
        files = action_coder_dump(
            project, arg_diff, arg_path, arg_content, sid, socketio
        )
        if files is None or len(files) == 0:
            logger.error(f"Dump failed: empty result")
            socketio.emit(
                "coder/dump.result",
                sio_coder_dump_pb2.SioCoderDumpResponse(
                    success=False,
                    error="Unknown error, please see more in server log",
                ).SerializeToString(),
                to=sid,
            )
            return

        logger.trace(f"Dump successful")
        socketio.emit(
            "coder/dump.result",
            sio_coder_dump_pb2.SioCoderDumpResponse(
                success=True,
                files=files,
            ).SerializeToString(),
            to=sid,
        )
    except Exception as e:
        logger.exception(f"Dump failed: {str(e)!r}")
        socketio.emit(
            "coder/dump.result",
            sio_coder_dump_pb2.SioCoderDumpResponse(
                success=False,
                error=str(e),
            ).SerializeToString(),
            to=sid,
        )


@socketio.on("sio/coder/generate")
def sio_coder_generate(data: bytes):
    # args: (path: str, output: str, files?: str[])
    # emit:
    #   coder/generate.result (success: bool, error?: str)
    #   coder/generate.progress (count: int, index: int, file: str, write: bool)
    sid: str = request.sid  # type: ignore

    msg = sio_coder_generate_pb2.SioCoderGenerateRequest()
    msg.ParseFromString(data)
    arg_path = msg.path
    arg_output = msg.output
    arg_files = list(msg.files)

    logger.trace(
        f"{sid!r} calling sio/coder/generate with path:{arg_path!r}, output:{arg_output!r}, files:{arg_files!r}"
    )

    if not isinstance(arg_path, str):
        logger.error(f"Called with invalid file path: {arg_path!r}")
        socketio.emit(
            "coder/generate.result",
            sio_coder_generate_pb2.SioCoderGenerateResponse(
                success=False,
                error="'file' must be a file path string",
            ).SerializeToString(),
            to=sid,
        )
        return

    try:
        project = ProjectUtils.load_project_from_file(arg_path)
        if not project.origin:
            logger.error(f"Called with invalid file path: {arg_path!r}")
            socketio.emit(
                "coder/generate.result",
                sio_coder_generate_pb2.SioCoderGenerateResponse(
                    success=False,
                    error=f"Failed to load file: {arg_path}",
                ).SerializeToString(),
                to=sid,
            )
            return

        result = action_coder_generate(
            project, arg_output, False, arg_files, sid, socketio
        )
        if not result:
            logger.error(f"Generate failed: unknown error")
            socketio.emit(
                "coder/generate.result",
                sio_coder_generate_pb2.SioCoderGenerateResponse(
                    success=False,
                    error="Generation failed, please see more in server log",
                ).SerializeToString(),
                to=sid,
            )
            return

        logger.trace(f"Generate successful")
        socketio.emit(
            "coder/generate.result",
            sio_coder_generate_pb2.SioCoderGenerateResponse(
                success=True,
            ).SerializeToString(),
            to=sid,
        )
    except Exception as e:
        logger.exception(f"Generate failed: {str(e)!r}")
        socketio.emit(
            "coder/generate.result",
            sio_coder_generate_pb2.SioCoderGenerateResponse(
                success=False,
                error=str(e),
            ).SerializeToString(),
            to=sid,
        )


@socketio.on("sio/package/install")
def sio_package_install(data: bytes):
    # args: (path: str)
    # emit:
    #   package/install.result (success: bool, error?: str)
    #   package/install.progress (count: int, index: int, file: str)
    sid: str = request.sid  # type: ignore

    msg = sio_package_install_pb2.SioPackageInstallRequest()
    msg.ParseFromString(data)
    arg_path = msg.path

    logger.trace(f"{sid!r} calling sio/package/install with path:{arg_path!r}")

    if not isinstance(arg_path, str):
        logger.error(f"Called with invalid path: {arg_path!r}")
        socketio.emit(
            "package/install.result",
            sio_package_install_pb2.SioPackageInstallResponse(
                success=False,
                error="'path' must be a file path string",
            ).SerializeToString(),
            to=sid,
        )
        return

    try:
        package_desc = action_package_install(arg_path, False, False, sid, socketio)
        if package_desc is None:
            socketio.emit(
                "package/install.result",
                sio_package_install_pb2.SioPackageInstallResponse(
                    success=False,
                    error="Unknown error, please see more in server log",
                ).SerializeToString(),
                to=sid,
            )
            return

        # Convert PackageDescription to protobuf Description
        description = sio_package_description_pb2.Description()
        description.name = package_desc.name
        description.version = package_desc.version
        description.license = package_desc.license
        description.type = package_desc.type
        description.vendor = package_desc.vendor
        description.support = package_desc.support

        # Convert vendorUrl map
        for key, value in package_desc.vendorUrl.origin.items():
            description.vendorUrl[key] = value

        # Convert description map
        for key, value in package_desc.description.origin.items():
            description.description[key] = value

        # Convert url map
        for key, value in package_desc.url.origin.items():
            description.url[key] = value

        # Convert author
        author = package_desc.author
        author_pb = sio_package_description_pb2.Author()
        author_pb.name = author.name
        author_pb.email = author.email
        author_pb.website.blog = author.website.blog
        author_pb.website.github = author.website.github
        description.author.CopyFrom(author_pb)

        socketio.emit(
            "package/install.result",
            sio_package_install_pb2.SioPackageInstallResponse(
                success=True,
                description=description,
            ).SerializeToString(),
            to=sid,
        )
    except Exception as e:
        logger.exception(f"Install failed: {str(e)!r}")
        socketio.emit(
            "package/install.result",
            sio_package_install_pb2.SioPackageInstallResponse(
                success=False,
                error=str(e),
            ).SerializeToString(),
            to=sid,
        )


@socketio.on("sio/package/uninstall")
def sio_package_uninstall(data: bytes):
    # args: (type: str, name: str, version: str)
    # emit:
    #   package/uninstall.result (success: bool, error?: str)
    sid: str = request.sid  # type: ignore

    msg = sio_package_uninstall_pb2.SioPackageUninstallRequest()
    msg.ParseFromString(data)
    arg_type = msg.type
    arg_name = msg.name
    arg_version = msg.version

    logger.trace(
        f"{sid!r} calling sio/package/uninstall with type:{arg_type!r}, name:{arg_name!r}, version:{arg_version!r}"
    )

    try:
        result = action_package_uninstall(arg_type, arg_name, arg_version)
        if result:
            socketio.emit(
                "package/uninstall.result",
                sio_package_uninstall_pb2.SioPackageUninstallResponse(
                    success=True,
                ).SerializeToString(),
                to=sid,
            )
        else:
            socketio.emit(
                "package/uninstall.result",
                sio_package_uninstall_pb2.SioPackageUninstallResponse(
                    success=False,
                    error="Unknown error, please see more in server log",
                ).SerializeToString(),
                to=sid,
            )
    except Exception as e:
        logger.exception(f"Uninstall failed: {str(e)!r}")
        socketio.emit(
            "package/uninstall.result",
            sio_package_uninstall_pb2.SioPackageUninstallResponse(
                success=False,
                error=str(e),
            ).SerializeToString(),
            to=sid,
        )


@socketio.on("sio/package/list")
def sio_package_list():
    # emit:
    #   package/list.result (success: bool, error?: str, result?: dict)
    sid: str = request.sid  # type: ignore
    logger.trace(f"{sid!r} calling sio/package/list")
    try:
        result = action_package_list()
        socketio.emit(
            "package/list.result",
            sio_package_list_pb2.SioPackageListResponse(
                success=True,
                packages=result,
            ).SerializeToString(),
            to=sid,
        )
    except Exception as e:
        logger.exception(f"List failed: {str(e)!r}")
        socketio.emit(
            "package/list.result",
            sio_package_list_pb2.SioPackageListResponse(
                success=False,
                error=str(e),
            ).SerializeToString(),
            to=sid,
        )


@socketio.on("sio/package/description")
def sio_package_description(data: bytes):
    # args: (type: str, name: str, version: str)
    # emit:
    #   package/description.result (success: bool, error?: str, result?: dict)
    sid: str = request.sid  # type: ignore
    msg = sio_package_description_pb2.SioPackageDescriptionRequest()
    msg.ParseFromString(data)
    arg_type = msg.type
    arg_name = msg.name
    arg_version = msg.version

    logger.trace(
        f"{sid!r} calling sio/package/description with type:{arg_type!r}, name:{arg_name!r}, version:{arg_version!r}"
    )
    try:
        package_desc = action_package_description(arg_type, arg_name, arg_version)
        if package_desc is None:
            socketio.emit(
                "package/description.result",
                sio_package_description_pb2.SioPackageDescriptionResponse(
                    success=False,
                    error="Unknown error, please see more in server log",
                ).SerializeToString(),
                to=sid,
            )
            return

        # Convert PackageDescription to protobuf Description
        description = sio_package_description_pb2.Description()
        description.name = package_desc.name
        description.version = package_desc.version
        description.license = package_desc.license
        description.type = package_desc.type
        description.vendor = package_desc.vendor
        description.support = package_desc.support

        # Convert vendorUrl map
        for key, value in package_desc.vendorUrl.origin.items():
            description.vendorUrl[key] = value

        # Convert description map
        for key, value in package_desc.description.origin.items():
            description.description[key] = value

        # Convert url map
        for key, value in package_desc.url.origin.items():
            description.url[key] = value

        # Convert author
        author = package_desc.author
        author_pb = sio_package_description_pb2.Author()
        author_pb.name = author.name
        author_pb.email = author.email
        author_pb.website.blog = author.website.blog
        author_pb.website.github = author.website.github
        description.author.CopyFrom(author_pb)

        socketio.emit(
            "package/description.result",
            sio_package_description_pb2.SioPackageDescriptionResponse(
                success=True,
                description=description,
            ).SerializeToString(),
            to=sid,
        )
    except Exception as e:
        logger.exception(f"Description failed: {str(e)!r}")
        socketio.emit(
            "package/description.result",
            sio_package_description_pb2.SioPackageDescriptionResponse(
                success=False,
                error=str(e),
            ).SerializeToString(),
            to=sid,
        )


# ------------------------------------------------------------------------------


@click.group()
@click.version_option(version=SysUtils.version(), message="%(version)s")
@click.option("--trace", is_flag=True, help="Enable trace logging.")
def cli(trace: bool):
    """CSP Server - CSP backend CLI."""
    today = datetime.datetime.today()

    log_level = "TRACE" if trace else "INFO"
    logger.configure(
        handlers=[
            {
                "sink": sys.stderr,
                "format": "<level>{message}</level>",
                "colorize": True,
                "level": log_level,
            }
        ]
    )
    logger.add(
        f"{SysUtils.exe_folder()}/log/csp-server-{today.year}-{today.month}.log",
        rotation="10 MB",
        level="TRACE",
    )


@cli.command(name="gen")
@click.argument("path", required=True)
@click.option("-o", "--output", help="Output directory.")
@click.option("--progress", is_flag=True, help="Show progress bar.")
@click.option(
    "-f",
    "--files",
    required=False,
    multiple=True,
    default=["all"],
    show_default=True,
    help="Generate files (multiple -f allowed).",
)
def cli_coder_generate(path: str, output: str, progress: bool, files: tuple[str, ...]):
    """Generate source code and config from project."""
    arg = {"path": path, "output": output, "progress": progress}
    logger.trace(f"Calling cli/coder/generate with {arg!r}")

    project = ProjectUtils.load_project_from_file(path)
    if not action_coder_generate(project, output, progress, list(files)):
        exit(1)


@cli.command(name="install")
@click.argument("path", required=True)
@click.option("--progress", is_flag=True, help="Show progress bar.")
@click.option("--verbose", is_flag=True, help="Verbose output.")
def cli_package_install(path: str, progress: bool, verbose: bool):
    """Install a CSP package."""
    arg = {"path": path, "progress": progress, "verbose": verbose}
    logger.trace(f"Calling cli/package/install with {arg!r}")

    if not action_package_install(path, progress, verbose):
        exit(1)


@cli.command(name="uninstall")
@click.option("-t", "--type", required=True, help="Package type (hal/toolchains/...).")
@click.option("-n", "--name", required=True, help="Package name.")
@click.option("-v", "--version", required=True, help="Package version.")
def cli_package_uninstall(type: str, name: str, version: str):
    """Uninstall a CSP package."""
    logger.info(
        f"CLI uninstall called with type: {type!r}, name: {name!r}, version: {version!r}"
    )
    if not action_package_uninstall(type, name, version):
        exit(1)


@cli.command(name="list")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON.")
def cli_package_list(as_json: bool):
    """List installed CSP packages."""
    arg = {"json": as_json}
    logger.trace(f"Calling cli/package/list with {arg!r}")
    action_package_list("json" if as_json else "std")


@cli.command(name="make-pkg")
@click.argument("path", required=True)
@click.option("--progress", is_flag=True, help="Show progress bar.")
@click.option("--verbose", is_flag=True, help="Verbose output.")
def cli_package_make(path: str, progress: bool, verbose: bool):
    """Make a directory to CSP package."""
    arg = {"path": path, "progress": progress, "verbose": verbose}
    logger.trace(f"Calling cli/package/make-pkg with {arg!r}")

    if not action_package_make(path, progress, verbose):
        exit(1)


@cli.command(name="serve")
@click.option("-p", "--port", default=55432, help="Port to listen on.")
@click.option("--debug", is_flag=True, help="Enable debug mode.")
def cli_serve(port: int, debug: bool):
    """Start the CSP backend server."""
    arg = {"port": port, "debug": debug}
    logger.trace(f"Calling cli/serve with {arg!r}")

    port = NetUtils.find_local_available_port(port)

    logger.info(f"Serving on http://127.0.0.1:{port}")
    socketio.run(app, host="0.0.0.0", port=port, debug=debug, use_reloader=False)


@cli.command(name="csp2filter")
@click.argument("path", required=True)
@click.option("--channel", is_flag=True, default=False, help="Enable channel mode.")
@click.option("--pin", is_flag=True, default=False, help="Enable pin parameters.")
@click.option("-o", "--output", help="Output dir, defaults to {file} dir.")
def cli_tools_csp2filter(path: str, channel: bool, pin: bool, output: str):
    """Generate jinja2 template filter from csp ip file."""
    arg = {"path": path, "output": output}
    logger.trace(f"Calling cli/csp2filter with {arg!r}")

    if output is None or not os.path.isdir(output):
        output = str(Path(path).parent)

    if not os.path.isdir(output):
        os.makedirs(output)

    ip = IpUtils.load_ip_from_file(path)
    action_tools_csp2filter(ip, channel, pin, output)


@cli.command(name="check-ip")
@click.argument("path", required=True)
@click.option("--vendor", help="Vendor name (e.g., Geehy).")
@click.option("--name", help="IP name (e.g., apm32f103_gpio).")
@click.option(
    "--type",
    "ip_type",
    type=click.Choice(["peripherals"], case_sensitive=False),
    help="IP type.",
)
def cli_tools_check_ip(path: str, vendor: str, name: str, ip_type: str):
    """
    Validate IP configuration file.

    \b
    Two modes:
    1. File mode: PATH
    2. Database mode: --vendor VENDOR --name NAME --type TYPE

    \b
    Examples:
      csp-server check-ip path/to/ip.yml
      csp-server check-ip --vendor Geehy --name apm32f103_gpio --type peripherals
    """

    arg = {"path": path, "vendor": vendor, "name": name, "type": ip_type}
    logger.trace(f"Calling cli/check_ip with {arg!r}")

    # Check if mode 1: file path
    if path:
        ip = IpUtils.load_ip_from_file(path)
        if not action_tools_check_ip(ip):
            exit(1)

    # Check if mode 2: vendor + name + type
    elif vendor and name and ip_type:
        ip = IpUtils.load_ip(vendor, ip_type, name)
        if not action_tools_check_ip(ip):
            exit(1)

    # Neither mode
    else:
        logger.error(
            "Error: Must provide either:\n"
            "  1. --file PATH\n"
            "  2. --vendor VENDOR --name NAME --type TYPE\n"
            "Missing required parameters"
        )
        exit(1)


@cli.command(name="y2j")
@click.argument("path", required=True)
def cli_tools_yaml2json(path: str):
    """
    Convert yaml file to json file
    """
    arg = {"path": path}
    logger.trace(f"Calling cli/yaml2json with {arg!r}")

    if not action_tools_yaml2json(path):
        exit(1)


@cli.command(name="cmx-ip")
@click.argument("path", required=True)
@click.option("--mcu", required=True, help="CubeMX mcu file.")
@click.option("-o", "--output", help="Output file, defaults to {path.prefix}.yml.")
@click.option("--alias", help="IP alias.")
def cli_tools_cmx_ip(path: str, mcu: str, output: str | None, alias: str | None):
    """
    Convert CubeMX ip file to CSP ip file
    """
    arg = {"path": path, "mcu": mcu, "output": output, "alias": alias}
    logger.trace(f"Calling cli/cmx-ip with {arg!r}")

    if not os.path.isfile(path):
        logger.error(f"Input file does not exist: {path}")
        exit(1)

    if not os.path.isfile(mcu):
        logger.error(f"MCU file does not exist: {mcu}")
        exit(1)

    if output is None:
        base, _ = os.path.splitext(path)
        output = f"{base}.yml"
    else:
        output_dir = str(Path(output).parent) or "."
        if not os.path.exists(output_dir):
            logger.error(f"Output directory does not exist: {output_dir}")
            exit(1)
        if os.path.isdir(output):
            logger.error(f"Output path points to a directory, not a file: {output}")
            exit(1)

    if not action_tools_cmx_ip(path, mcu, output, alias or ""):
        exit(1)


@cli.command(name="candb-dump")
@click.argument("path", required=True)
@click.option("--json", "as_json", is_flag=True, help="Output as JSON.")
def cli_tools_candb_dump(path: str, as_json: bool):
    """Dump Can database file."""
    arg = {"path": path, "json": as_json}
    logger.trace(f"Calling cli/tools/candb-dump with {arg!r}")

    if not os.path.isfile(path):
        logger.error(f"Input file does not exist: {path}")
        exit(1)

    action_tools_candb_dump(path, "json" if as_json else "std")


if __name__ == "__main__":
    cli()
