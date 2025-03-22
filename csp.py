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
# @file        csp.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-17     xqyjlj       initial version
#

import argparse
import datetime
import glob
import os
import sys

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication
from loguru import logger

# masking printing: 📢 Tips: QFluentWidgets Pro is now released. Click https://qfluentwidgets.com/pages/pro to learn more about it.
stdout = sys.stdout
sys.stdout = None

from qfluentwidgets import FluentTranslator

sys.stdout = stdout

from common import SETTINGS, PROJECT, CoderCmd, PackageCmd, PACKAGE
from window import MainWindow, StartupWindow, NewProjectWindow


def main():
    try:
        parser = create_parser()
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        sys.exit(1)

    today = datetime.datetime.today()
    logger.add(
        f"{SETTINGS.EXE_FOLDER}/log/csp-{today.year}-{today.month}.log",
        rotation="10 MB",
    )

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    app.setStyle("fusion")

    if args.command:
        args.func(args, parser, app)
    else:
        if args.version:
            print(
                f"csp version {SETTINGS.VERSION}. a fully open source chip configuration software system"
            )
            print(f"copyright (C) 2023-present xqyjlj, csplink.top, xqyjlj@126.com")
        elif args.file:
            handle_main(args, parser, app)
        else:
            handle_startup(args, parser, app)


def __init_qt_env(app: QApplication):
    if SETTINGS.get(SETTINGS.dpi_scale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(SETTINGS.get(SETTINGS.dpi_scale))

    locale = SETTINGS.get(SETTINGS.language).value
    translator = FluentTranslator(locale, app)
    app.installTranslator(translator)

    files = glob.glob(os.path.join(SETTINGS.I18N_FOLDER, f"*.{locale.name()}.qm"))
    for file in files:
        translator = QTranslator(app)
        translator.load(file)
        app.installTranslator(translator)

    folders = glob.glob(os.path.join(SETTINGS.FONTS_FOLDER, "*"))
    for folder in folders:
        files = glob.glob(f"{folder}/*.ttf")
        for file in files:
            QFontDatabase.addApplicationFont(file)


def __set_project(file: str):
    if not os.path.isfile(file):
        print(f"The file {file!r} is not exist.")
        sys.exit(1)

    PROJECT.set_path(file)
    if not PROJECT.valid():
        print(f"The csp project file {file!r} is invalid.")
        sys.exit(1)


# noinspection PyUnusedLocal
def handle_new(
    args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication
):
    __init_qt_env(app)
    window = NewProjectWindow()
    window.updateFrameless()
    window.show()
    app.exec()


# noinspection PyUnusedLocal
def handle_startup(
    args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication
):
    __init_qt_env(app)
    window = StartupWindow()
    window.updateFrameless()
    window.show()
    app.exec()


def handle_main(
    args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication
):
    file: str = args.file
    __set_project(file)
    __init_qt_env(app)
    window = MainWindow()
    window.updateFrameless()
    window.show()
    app.exec()


def handle_gen(
    args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication
):
    file: str = args.file
    progress: bool = args.progress
    output: str = args.output
    __set_project(file)

    succeed, msg = PROJECT.is_generate_setting_valid()
    if not succeed:
        print(f"the coder settings is invalid, reason: {msg!r}. please check it.")
        sys.exit(1)

    generator = CoderCmd(output, progress)
    generator.gen()


def handle_install(
    args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication
):
    path: str = args.path
    progress: bool = args.progress
    verbose: bool = args.verbose

    if not os.path.exists(path):
        print(f"The path {path!r} is not exist.")
        sys.exit(1)

    cmd = PackageCmd(progress, verbose)
    if not cmd.install(path):
        print(f"install failed. Please check it.")
        sys.exit(1)


def handle_uninstall(
    args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication
):
    kind: str = args.type
    name: str = args.name
    version: str = args.version

    path = PACKAGE.index().path(kind, name, version)
    if not os.path.exists(path):
        print(f"uninstall failed {kind}@{name}:{version}")
        sys.exit(1)

    cmd = PackageCmd(False, False)
    if not cmd.uninstall(kind, name, version):
        print(f"uninstall failed. Please check it.")
        sys.exit(1)


def handle_list(
    args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication
):
    for kind, package in PACKAGE.index().origin.items():
        print(f"{kind}:")
        for name, info in package.items():
            print(f"  {name}:")
            for version, path in info.items():
                print(f"    {version}: {PACKAGE.index().path(kind, name, version)}")


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="a fully open source chip configuration software system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    subparsers = parser.add_subparsers(
        title="subparsers", dest="command", required=False
    )

    new = subparsers.add_parser("new", help="new a project")
    new.set_defaults(func=handle_new)

    gen = subparsers.add_parser("gen", help="generate code from csp project")
    gen.add_argument("-f", "--file", required=True, help="csp project file")
    gen.add_argument("-o", "--output", required=False, help="output dir")
    gen.add_argument(
        "--progress",
        required=False,
        help="enable progress bar printing",
        action="store_true",
    )
    gen.set_defaults(func=handle_gen)

    install = subparsers.add_parser("install", help="install csp package")
    install.add_argument("-p", "--path", required=True, help="csp package path")
    install.add_argument(
        "--progress",
        required=False,
        help="enable progress bar printing",
        action="store_true",
    )
    install.add_argument(
        "--verbose",
        required=False,
        help="enable verbose information for users.",
        action="store_true",
    )
    install.set_defaults(func=handle_install)

    uninstall = subparsers.add_parser("uninstall", help="uninstall csp package")
    uninstall.add_argument("-t", "--type", required=True, help="csp package type")
    uninstall.add_argument("-n", "--name", required=True, help="csp package name")
    uninstall.add_argument("-v", "--version", required=True, help="csp package version")
    uninstall.set_defaults(func=handle_uninstall)

    list_ = subparsers.add_parser("list", help="list csp package")
    list_.set_defaults(func=handle_list)

    parser.add_argument("-f", "--file", required=False, help="csp project file")
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
