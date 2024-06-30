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

import sys, os, glob, getopt

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QFontDatabase

# masking printing: 📢 Tips: QFluentWidgets Pro is now released. Click https://qfluentwidgets.com/pages/pro to learn more about it.
stdout = sys.stdout
sys.stdout = None

from qfluentwidgets import FluentTranslator

sys.stdout = stdout

from common.settings import SETTINGS
from common.project import PROJECT
from view.main_view import MainWindowView


def main():

    if SETTINGS.get(SETTINGS.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(SETTINGS.get(SETTINGS.dpiScale))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    locale = SETTINGS.get(SETTINGS.language).value
    translator = FluentTranslator(locale, app)
    app.installTranslator(translator)

    files = glob.glob(f"resource/i18n/qm/*.{locale.name()}.qm")
    for file in files:
        translator = QTranslator(app)
        translator.load(file)
        app.installTranslator(translator)

    dirs = glob.glob(f"resource/fonts/*")
    for dir in dirs:
        files = glob.glob(f"{dir}/*.ttf")
        for file in files:
            QFontDatabase.addApplicationFont(file)

    w = MainWindowView()
    w.show()

    w.setMicaEffectEnabled(False)
    app.exec_()


def checkOpt():
    if len(sys.argv) == 2:
        file = sys.argv[1]
        if os.path.isfile(file):
            PROJECT.path = file
    elif len(sys.argv) > 2:
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hf:o:r:d:t:",
                                       ["help", "file=", "output=", "repository=", "package_dir=", "toolchains_dir="])
        except getopt.GetoptError:
            # help()
            sys.exit(2)
    else:
        return


if __name__ == '__main__':
    checkOpt()
    main()
