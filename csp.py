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

from loguru import logger

script_dir = os.path.dirname(__file__)
sys.path.append(f'{script_dir}/jinja2')

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

# masking printing: 📢 Tips: QFluentWidgets Pro is now released. Click https://qfluentwidgets.com/pages/pro to learn more about it.
stdout = sys.stdout
sys.stdout = None

from qfluentwidgets import FluentTranslator

sys.stdout = stdout

from common import SETTINGS, PROJECT, CoderCmd, PackageCmd
from window import MainWindow, StartupWindow, NewProjectWindow


def main():
    try:
        parser = createParser()
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(e)
        sys.exit(1)

    today = datetime.datetime.today()
    logger.add(f'log/csp-{today.year}-{today.month}.log', rotation='10 MB')

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)
    app.setStyle('fusion')

    if args.command:
        args.func(args, parser, app)
    else:
        if args.version:
            print(f'csp version {SETTINGS.VERSION}. a fully open source chip configuration software system')
            print(f'copyright (C) 2023-present xqyjlj, csplink.top, xqyjlj@126.com')
        elif args.file:
            handleMain(args, parser, app)
        else:
            handleStartup(args, parser, app)


def __initQtEnv(app: QApplication):
    if SETTINGS.get(SETTINGS.dpiScale) != 'Auto':
        os.environ['QT_ENABLE_HIGHDPI_SCALING'] = '0'
        os.environ['QT_SCALE_FACTOR'] = str(SETTINGS.get(SETTINGS.dpiScale))

    locale = SETTINGS.get(SETTINGS.language).value
    translator = FluentTranslator(locale, app)
    app.installTranslator(translator)

    files = glob.glob(os.path.join(SETTINGS.I18N_FOLDER, f'*.{locale.name()}.qm'))
    for file in files:
        translator = QTranslator(app)
        translator.load(file)
        app.installTranslator(translator)

    folders = glob.glob(os.path.join(SETTINGS.FONTS_FOLDER, '*'))
    for folder in folders:
        files = glob.glob(f'{folder}/*.ttf')
        for file in files:
            QFontDatabase.addApplicationFont(file)


def __setProject(file: str):
    if not os.path.isfile(file):
        print(f'The file {file!r} is not exist.')
        sys.exit(1)

    PROJECT.setPath(file)
    if not PROJECT.valid():
        print(f'The csp project file {file!r} is invalid.')
        sys.exit(1)


# noinspection PyUnusedLocal
def handleNew(args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication):
    __initQtEnv(app)
    window = NewProjectWindow()
    window.updateFrameless()
    window.show()
    app.exec()


# noinspection PyUnusedLocal
def handleStartup(args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication):
    __initQtEnv(app)
    window = StartupWindow()
    window.updateFrameless()
    window.show()
    app.exec()


# noinspection PyUnusedLocal
def handleMain(args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication):
    file = args.file
    __setProject(file)
    __initQtEnv(app)
    window = MainWindow()
    window.updateFrameless()
    window.show()
    app.exec()


# noinspection PyUnusedLocal
def handleGen(args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication):
    file = args.file
    progress = args.progress
    output = args.output
    __setProject(file)

    if not PROJECT.isGenerateSettingValid():
        print(f'The coder settings is invalid. Please check it.')
        sys.exit(1)

    generator = CoderCmd(output, progress)
    generator.gen()


# noinspection PyUnusedLocal
def handleInstall(args: argparse.Namespace, parser: argparse.ArgumentParser, app: QApplication):
    path = args.path
    progress = args.progress

    if not os.path.exists(path):
        print(f'The path {path!r} is not exist.')
        sys.exit(1)

    cmd = PackageCmd(progress)
    if not cmd.install(path):
        print(f'install failed. Please check it.')
        sys.exit(1)


def createParser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='a fully open source chip configuration software system',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(title='subparsers', dest='command', required=False)

    new = subparsers.add_parser('new', help='new a project')
    new.set_defaults(func=handleNew)

    gen = subparsers.add_parser('gen', help='generate code from csp project')
    gen.add_argument('-f', '--file', required=True, help='csp project file')
    gen.add_argument('-o', '--output', required=False, help='output dir')
    gen.add_argument('--progress', required=False, help='enable progress bar printing', action='store_true')
    gen.set_defaults(func=handleGen)

    install = subparsers.add_parser('install', help='install csp package')
    install.add_argument('-p', '--path', required=True, help='csp package path')
    install.add_argument('--progress', required=False, help='enable progress bar printing', action='store_true')
    install.set_defaults(func=handleInstall)

    parser.add_argument('-f', '--file', required=False, help='csp project file')
    parser.add_argument('-v', '--version', required=False, help='print the version number', action='store_true')

    return parser


if __name__ == '__main__':
    main()
