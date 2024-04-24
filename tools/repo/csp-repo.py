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
# @file        csp-repo.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-04-01     xqyjlj     initial version
#

import tarfile
import zipfile
import hashlib
import tqdm
import glob
import subprocess
import ping3
import json
import yaml
import os, sys, getopt
import platform
import threading
import re
import shutil
import requests
from urllib.parse import urlparse

script_dir = os.path.dirname(__file__)

verbose_key = "CSP_VERBOSE"


def is_installed(type: str, name: str, version: str, repositories: str) -> bool:
    """
    Check if the package is installed.
    :param type: The type of the package.
    :param name: The name of the package.
    :param version: The version of the package.
    :param repositories: The path of the repositories.
    :return: True if the package is installed, False otherwise.
    """
    installed = False
    output_dir = os.path.join(repositories, type.lower(), name, version)

    if os.path.isdir(os.path.join(output_dir, ".csplink")):
        installed = True

    manifest_file = os.path.join(repositories, "manifest.json")
    manifest = {}
    if not os.path.isfile(manifest_file):
        with open(manifest_file, "w+", encoding='utf-8') as _:
            pass
    else:
        with open(manifest_file, "r", encoding='utf-8') as file:
            manifest = json.loads(file.read())

    is_changed = False
    if not type in manifest.keys():
        manifest[type] = {}
    if not name in manifest[type].keys():
        manifest[type][name] = {}
    if not version in manifest[type][name].keys():
        manifest[type][name][version] = {"Installed": False}
        is_changed = True

    if not is_changed:
        is_changed = (manifest[type][name][version]["Installed"] != installed)

    manifest[type][name][version]["Installed"] = installed

    if is_changed:
        with open(f"{repositories}/manifest.json", "w", encoding='utf-8') as file:
            file.write(json.dumps(manifest, indent=2, sort_keys=True))

    return installed


def get_git_head(path: str) -> str:
    """
    Get the git head of the package.
    :param path: The path of the package.
    :return: The git head of the package.
    """
    sha = subprocess.run(['git', 'rev-parse', 'HEAD'],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         cwd=path,
                         text=True)
    date = subprocess.run(['git', 'log', '-1', '--date=format:%Y%m%d%H%M%S', "--format=%ad"],
                          stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          cwd=path,
                          text=True)
    if sha.returncode == 0 and date.returncode == 0:
        return f"{sha.stdout.strip()}@{date.stdout.strip()}"
    else:
        return ""


def show_package_list(package: dict, package_name: str, repositories: str):
    """
    Show the package list.
    :param package: The package list.
    :param package_name: The name of the package.
    :param repositories: The path of the repositories.
    :return: None
    """
    if package_name == "all":
        for name in package["Library"].keys():
            for version in package["Library"][name]["Versions"].keys():
                installed = is_installed("Library", name, version, repositories)
                package["Library"][name]["Versions"][version]["Installed"] = installed
                if version == "latest" and installed:
                    package["Library"][name]["Versions"][version]["Sha"] = get_git_head(
                        os.path.join(repositories, "library", name, version))
        for name in package["Toolchains"].keys():
            system = platform.system()
            if system == "Linux":
                pass
            elif system == "Windows":
                pass
            else:
                raise Exception(f'Temporarily unsupported operating systems ("{system}")')

            for version in package["Toolchains"][name]["Versions"][system].keys():
                installed = is_installed("Toolchains", name, version, repositories)
                package["Toolchains"][name]["Versions"][system][version]["Installed"] = installed
            package["Toolchains"][name]["Versions"] = package["Toolchains"][name]["Versions"][system]

        print(json.dumps(package, indent=2, sort_keys=True))
    else:
        map = {}
        for name in package["Library"].keys():
            if name == package_name:
                for version in package["Library"][name]["Versions"].keys():
                    installed = is_installed("Library", name, version, repositories)
                    package["Library"][name]["Versions"][version]["Installed"] = installed
                    if version == "latest" and installed:
                        package["Library"][name]["Versions"][version]["Sha"] = get_git_head(
                            os.path.join(repositories, "library", name, version))
                    map["Library"] = {}
                    map["Library"][name] = package["Library"][name]
                break

        if map == {}:
            for name in package["Toolchains"].keys():
                if name == package_name:
                    system = platform.system()
                    if system == "Linux":
                        pass
                    elif system == "Windows":
                        pass
                    else:
                        raise Exception(f'Temporarily unsupported operating systems ("{system}")')

                    for version in package["Toolchains"][name]["Versions"][system].keys():
                        installed = is_installed("Toolchains", name, version, repositories)
                        package["Toolchains"][name]["Versions"][system][version]["Installed"] = installed
                    package["Toolchains"][name]["Versions"] = package["Toolchains"][name]["Versions"][system]
                    map["Toolchains"] = {}
                    map["Toolchains"][name] = package["Toolchains"][name]

        print(json.dumps(map, indent=2, sort_keys=True))


def get_ping_time(url: str) -> float:
    """
    Get the ping time of the url.
    :param url: The url of the package.
    :return: The ping time of the url.
    """
    parsed_url = urlparse(url)
    host = parsed_url.netloc
    try:
        delay = ping3.ping(host)
        if delay == None:
            return float('inf')
        else:
            return delay
    except OSError as _:
        return float('inf')


def git_read_output(url: str, stream):
    desc = ""
    if url == "":
        desc = "git pull"
    else:
        desc = f"git clone {url}"
    if os.getenv(verbose_key, "false") == "true":
        progress_bar = tqdm.tqdm(total=100, desc=desc, unit='', unit_scale=False)
        progress_last = 0
    while True:
        line = stream.readline().strip()
        if not line:
            break
        if os.getenv(verbose_key, "false") == "true":
            progress = 0
            match1 = re.search(r"remote: Counting objects: \s*(\d+)%", line)
            match2 = re.search(r"remote: Compressing objects: \s*(\d+)%", line)
            match3 = re.search(r"Receiving objects: \s*(\d+)%", line)
            match4 = re.search(r"Resolving deltas: \s*(\d+)%", line)

            if match1:
                progress = (float(match1.group(1)) / 4) + 0
            elif match2:
                progress = (float(match2.group(1)) / 4) + 25
            elif match3:
                progress = (float(match3.group(1)) / 4) + 50
            elif match4:
                progress = (float(match4.group(1)) / 4) + 75
            elif line == "Already up to date.":
                progress = 100

            if progress != 0:
                progress_bar.update(progress - progress_last)
                progress_bar.refresh()
                progress_last = progress
            else:
                print(line)


def find_package(package: dict, package_name: str, package_version: str, repositories: str):
    """
    Find the package.
    :param package: The package list.
    :param package_name: The name of the package.
    :param package_version: The version of the package.
    :param repositories: The path of the repositories.
    """

    type = ""
    map = {}
    for name in package["Library"].keys():
        if name == package_name:
            for version in package["Library"][name]["Versions"].keys():
                if version == package_version:
                    installed = is_installed("Library", name, version, repositories)
                    package["Library"][name]["Versions"][version]["Installed"] = installed
                    map = package["Library"][name]
                    type = "Library"
                    break
            break

    if map == {}:
        for name in package["Toolchains"].keys():
            if name == package_name:
                system = platform.system()
                if system == "Linux":
                    pass
                elif system == "Windows":
                    pass
                else:
                    raise Exception(f'Temporarily unsupported operating systems ("{system}")')

                for version in package["Toolchains"][name]["Versions"][system].keys():
                    if version == package_version:
                        installed = is_installed("Toolchains", name, version, repositories)
                        package["Toolchains"][name]["Versions"][system][version]["Installed"] = installed
                        package["Toolchains"][name]["Versions"] = package["Toolchains"][name]["Versions"][system]
                        map = package["Toolchains"][name]
                        type = "Toolchains"
                        break
                break

    if map == {}:
        raise Exception(f"package {package_name}@{package_version} not found.")

    return type, map


def install_package(package: dict, package_name: str, package_version: str, repositories: str):
    """
    Install the package.
    :param package: The package list.
    :param package_name: The name of the package.
    :param package_version: The version of the package.
    :param repositories: The path of the repositories.
    """

    type, map = find_package(package, package_name, package_version, repositories)

    if map["Versions"][package_version]["Installed"]:
        print(f"package {package_name}@{package_version} has been installed.")
        return

    urls = sorted(map["Versions"][package_version]["Urls"], key=get_ping_time)
    url = urls[0]

    ############################# download package #############################

    package_dir = os.path.join(repositories, type.lower(), package_name)
    if not os.path.isdir(package_dir):
        os.makedirs(package_dir)

    output_path = os.path.join(repositories, type.lower(), package_name, package_version)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

    if str.endswith(url, ".git"):  # git clone
        print(f"git clone {url}")

        env = os.environ.copy()
        env['LANG'] = 'en'
        proc = subprocess.Popen(
            ['git', 'clone', '--progress', '--recursive', '-c', 'core.longpaths=true', url, output_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            text=True)
        thread = threading.Thread(target=git_read_output, args=(
            url,
            proc.stderr,
        ))
        thread.start()
        proc.wait()
        thread.join()

        if proc.returncode != 0:
            raise Exception(f"git clone failed with exit code {proc.returncode}.")
    else:  # http download
        pkg_file = os.path.join(repositories, type.lower(), package_name, os.path.basename(url))
        pkg_tmp_file = f"{pkg_file}.tmp"
        if os.path.exists(pkg_tmp_file):
            os.remove(pkg_tmp_file)

        if not os.path.exists(pkg_file):
            print(f"Download file from {url}")
            response = requests.get(url, stream=True)
            block_size = 1024  # 1Kb
            if os.getenv(verbose_key, "false") == "true":
                total_size_in_bytes = int(response.headers.get('content-length', 0))
                progress_bar = tqdm.tqdm(total=total_size_in_bytes,
                                         desc=f"Downloading file {os.path.basename(pkg_tmp_file)}",
                                         unit='iB',
                                         unit_scale=True)
            sha256_hash = hashlib.sha256()
            with open(pkg_tmp_file, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    sha256_hash.update(data)
                    if os.getenv(verbose_key, "false") == "true":
                        progress_bar.update(len(data))
            if os.getenv(verbose_key, "false") == "true":
                progress_bar.close()
            hash_value = sha256_hash.hexdigest()
            if map["Versions"][package_version]["Sha"] == hash_value:
                os.rename(pkg_tmp_file, pkg_file)
                if os.getenv(verbose_key, "false") == "true":
                    print(f"Download file {pkg_file} successful")
            else:
                raise Exception(f"Download file {os.path.basename(pkg_tmp_file)} failed. Sha256 value does not match.")

        if os.path.exists(pkg_file):
            tmp = f"{output_path}.tmp"
            if not os.path.exists(tmp):
                os.makedirs(tmp)
            if os.getenv(verbose_key, "false") == "true":
                print(f"extract file {pkg_file} to {tmp}")
            if pkg_file.endswith(".zip"):
                with zipfile.ZipFile(pkg_file, 'r') as zip_ref:
                    zip_ref.extractall(tmp)
            else:
                with tarfile.open(pkg_file, 'r|*') as tar_ref:
                    tar_ref.extractall(tmp, filter='data')
            file_dirs = glob.glob(os.path.join(tmp, "*"))

            if len(file_dirs) == 1 and os.path.isdir(file_dirs[0]):
                shutil.move(file_dirs[0], output_path)
                shutil.rmtree(tmp)
            else:
                shutil.move(tmp, output_path)
        else:
            raise Exception(f"package {package_name}@{package_version} not found.")

    if not os.path.isdir(os.path.join(output_path, ".csplink")):
        os.makedirs(os.path.join(output_path, ".csplink"))
        if is_installed(type, package_name, package_version, repositories):
            print(f"package {package_name}@{package_version} install successful.")
        else:
            raise Exception(f"package {package_name}@{package_version} install failed.")
    else:
        raise Exception(f"package {package_name}@{package_version} has been installed.")


def update_package(package: dict, package_name: str, repositories: str):
    """
    Update the package.
    :param package: The package.
    :param package_name: The name of the package.
    :param repositories: The path of the repositories.
    """

    type, map = find_package(package, package_name, "latest", repositories)

    if not map["Versions"]["latest"]["Installed"]:
        print(f"package {package_name}@latest not yet installed.")
        return

    output_path = os.path.join(repositories, type.lower(), package_name, "latest")
    if os.path.exists(output_path):
        env = os.environ.copy()
        env['LANG'] = 'en'
        proc = subprocess.Popen(['git', 'pull', '--progress'],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                env=env,
                                cwd=output_path,
                                text=True)
        thread = threading.Thread(target=git_read_output, args=(
            "",
            proc.stdout,
        ))
        thread.start()
        proc.wait()
        thread.join()

        if proc.returncode != 0:
            raise Exception(f"git pull failed with exit code {proc.returncode}.")
        else:
            print(f"package {package_name}@latest update successful.")
    else:
        raise Exception(f"package {package_name}@latest not found.")


def uninstall_package(package: dict, package_name: str, package_version: str, repositories: str):
    """
    Uninstall the package.
    :param package: The package.
    :param package_name: The name of the package.
    :param package_version: The version of the package.
    :param repositories: The path of the repositories.
    """

    type, map = find_package(package, package_name, package_version, repositories)

    if not map["Versions"][package_version]["Installed"]:
        print(f"package {package_name}@{package_version} has been installed.")
        return

    output_path = os.path.join(repositories, type.lower(), package_name, package_version)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)

        if not is_installed(type, package_name, package_version, repositories):
            print(f"package {package_name}@{package_version} uninstall successful.")
        else:
            raise Exception(f"package {package_name}@{package_version} uninstall failed.")
    else:
        raise Exception(f"package {package_name}@latest not found.")


def help():
    """
    Print the help message.
    """
    print("usage: " + os.path.basename(__file__) + " [<options>] ")
    print("")
    print("    -h, --help               print this help.")
    print("        --verbose            print lots of verbose information for users.")
    print("    -d, --dump               dump packages.\n"
          "                             e.g.\n"
          f"                                - {os.path.basename(__file__)} --dump=csp_hal_apm32f1 -r <dir>\n"
          f"                                - {os.path.basename(__file__)} --dump=all -r <dir>")
    print("        --install            install the package.\n"
          "                             e.g.\n"
          f"                                - {os.path.basename(__file__)} --install=csp_hal_apm32f1 -r <dir>")
    print("        --update             update the package.\n"
          "                             e.g.\n"
          f"                                - {os.path.basename(__file__)} --update=csp_hal_apm32f1 -r <dir>")
    print("        --uninstall          uninstall the package.\n"
          "                             e.g.\n"
          f"                                - {os.path.basename(__file__)} --uninstall=csp_hal_apm32f1 -r <dir>")
    print(
        "        --package-version    package version.\n"
        "                             e.g.\n"
        f"                                - {os.path.basename(__file__)} --install=csp_hal_apm32f1 --package-version=latest -r <dir>\n"
        f"                                - {os.path.basename(__file__)} --uninstall=csp_hal_apm32f1 --package-version=latest -r <dir>"
    )
    print("    -r, --repositories       repositories dir.")


def main(dump: str, package_name: str, command: str, version: str, repositories: str):
    """
    Main function.
    """

    if not os.path.isdir(repositories):
        os.makedirs(repositories)

    package_yaml = {}
    with open(f"{script_dir}/resources/package.yml", "r", encoding='utf-8') as file:
        package_yaml = yaml.load(file, Loader=yaml.FullLoader)

    if dump != "":
        show_package_list(package_yaml, dump, repositories)
    elif command == "install" and version != "":
        install_package(package_yaml, package_name, version, repositories)
    elif command == "update":
        update_package(package_yaml, package_name, repositories)
    elif command == "uninstall" and version != "":
        uninstall_package(package_yaml, package_name, version, repositories)
    else:
        help()
        sys.exit(2)


if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(
            sys.argv[1:], "hd:r:",
            ["help", "verbose", "dump=", "install=", "update=", "uninstall=", "package-version=", "repositories="])
    except getopt.GetoptError:
        help()
        sys.exit(2)

    dump = ""
    package_name = ""
    command = ""
    version = ""
    repositories = ""

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            help()
            sys.exit()
        elif opt in ("verbose"):
            os.environ[verbose_key] = "true"
        elif opt in ("-d", "--dump"):
            dump = arg
        elif opt in ("--install"):
            package_name = arg
            command = "install"
        elif opt in ("--update"):
            package_name = arg
            command = "update"
        elif opt in ("--uninstall"):
            package_name = arg
            command = "uninstall"
        elif opt in ("--package-version"):
            version = arg
        elif opt in ("--repositories"):
            repositories = arg

    if repositories == "" or (command == "" and dump == ""):
        help()
        sys.exit(2)

    main(dump, package_name, command, version, repositories)
