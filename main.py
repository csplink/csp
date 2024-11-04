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
# @file        main.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-17     xqyjlj       initial version
#

import getopt
import glob
import os
import sys

from PySide6.QtCore import Qt, QTranslator
from PySide6.QtGui import QFontDatabase
from PySide6.QtWidgets import QApplication

# masking printing: 📢 Tips: QFluentWidgets Pro is now released. Click https://qfluentwidgets.com/pages/pro to learn more about it.
stdout = sys.stdout
sys.stdout = None

from qfluentwidgets import FluentTranslator

sys.stdout = stdout

from common import SETTINGS, PROJECT
from view import MainWindow, StartupWindow, NewProjectWindow

script_dir = os.path.dirname(__file__)
sys.path.append(f"{script_dir}/plugins")

isNewProjectRequested = False


def main():
    if SETTINGS.get(SETTINGS.dpiScale) != "Auto":
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(SETTINGS.get(SETTINGS.dpiScale))

    app = QApplication(sys.argv)
    app.setAttribute(Qt.ApplicationAttribute.AA_DontCreateNativeWidgetSiblings)

    if sys.platform == 'win32' and sys.getwindowsversion().build >= 22000:
        app.setStyle("fusion")

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

    if PROJECT.path != "":
        view = MainWindow()
        view.updateFrameless()
        view.show()
    elif isNewProjectRequested:
        view = NewProjectWindow()
        view.updateFrameless()
        view.show()
    else:
        view = StartupWindow()
        view.updateFrameless()
        view.show()

    app.exec()


def checkOpt():
    if len(sys.argv) >= 2:
        file = sys.argv[1]
        if os.path.isfile(file):
            PROJECT.path = file
            return

        try:
            opts, args = getopt.getopt(sys.argv[1:], "hn", ["help", "new"])
        except getopt.GetoptError:
            # help()
            sys.exit(2)

        for opt, arg in opts:
            if opt in ("-h", "--help"):
                help()
                sys.exit(0)
            elif opt in ("-n", "--new"):
                global isNewProjectRequested
                isNewProjectRequested = True
                return
    else:
        return


if __name__ == '__main__':
    checkOpt()
    main()
