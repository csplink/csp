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
# @file        settings.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-29     xqyjlj       initial version
#

import os
import sys
from enum import Enum
from pathlib import Path

from PySide6.QtCore import QLocale, QStandardPaths
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator, OptionsValidator,
                            EnumSerializer, ColorConfigItem, Theme, FolderValidator, ConfigSerializer)


class LanguageType(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Language.Chinese, QLocale.Country.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Language.Chinese, QLocale.Country.HongKong)
    ENGLISH = QLocale(QLocale.Language.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != LanguageType.AUTO else "Auto"

    def deserialize(self, value: str):
        return LanguageType(QLocale(value)) if value != "Auto" else LanguageType.AUTO


class Settings(QConfig):
    """ Config of application """

    if os.getenv('__CSPLINK_UNIT_TEST_TESTING', '0') == '1':
        EXE_FOLDER = os.getcwd()
    else:
        EXE_FOLDER = str(Path(sys.argv[0]).parent)

    # folders ----------------------------------------------------------------------------------------------------------
    packageFolder = ConfigItem("Folders", "Packages", os.path.join(EXE_FOLDER, "resource", "packages"),
                               FolderValidator())

    # system -----------------------------------------------------------------------------------------------------------
    language = OptionsConfigItem("System",
                                 "languageType",
                                 LanguageType.AUTO,
                                 OptionsValidator(LanguageType),
                                 LanguageSerializer(),
                                 restart=True)

    dpiScale = OptionsConfigItem("System",
                                 "DpiScale",
                                 "Auto",
                                 OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
                                 restart=True)
    isUseOpenGL = ConfigItem("System", "UseOpenGL", True, BoolValidator(), restart=True)
    openGLSamples = OptionsConfigItem("System",
                                      "OpenGLSamples",
                                      4,
                                      OptionsValidator([4, 8, 12, 16]),
                                      restart=True)
    clockTreeType = OptionsConfigItem("System",
                                      "ClockTreeType",
                                      "Pixmap",
                                      OptionsValidator(["Pixmap", "Svg"]),
                                      restart=True)

    # update
    isUpdateAtStartup = ConfigItem("Update", "CheckUpdateAtStartup", True, BoolValidator())

    # style ------------------------------------------------------------------------------------------------------------
    themeMode = OptionsConfigItem("Style", "ThemeMode", Theme.AUTO, OptionsValidator(Theme), EnumSerializer(Theme))
    themeColor = ColorConfigItem("Style", "ThemeColor", '#009faa')
    alertColor = ColorConfigItem("Style", "AlertColor", '#c04851')

    # misc -------------------------------------------------------------------------------------------------------------
    lastOpenProjectFolder = ConfigItem(
        "Misc", "LastOpenProjectFolder",
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation), FolderValidator())
    lastPackageFileFolder = ConfigItem(
        "Misc", "LastPackageFileFolder",
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DownloadLocation), FolderValidator())

    # const data -------------------------------------------------------------------------------------------------------
    DATABASE_FOLDER = os.path.join(EXE_FOLDER, "resource", "database")
    STYLE_FOLDER = os.path.join(EXE_FOLDER, "resource", "style")
    ICON_FOLDER = os.path.join(EXE_FOLDER, "resource", "images", "icon")
    I18N_FOLDER = os.path.join(EXE_FOLDER, "resource", "i18n")
    PACKAGES_IMAGE_FOLDER = os.path.join(EXE_FOLDER, "resource", "images", "packages")
    FONTS_FOLDER = os.path.join(EXE_FOLDER, "resource", "fonts")
    PACKAGE_INDEX_FILE = os.path.join(packageFolder.value, "packages.index")
    CONTRIBUTORS_FILE = os.path.join(EXE_FOLDER, "resource", "contributors", "contributors")
    YEAR = 2023
    AUTHOR = "xqyjlj"
    AUTHOR_BLOG_URL = "https://xqyjlj.github.io/"
    VERSION = "0.1.0"
    HELP_URL = "https://csplink.top"
    REPO_URL = "https://github.com/csplink/csp"
    FEEDBACK_URL = "https://github.com/csplink/csp/issues"
    RELEASE_URL = "https://github.com/csplink/csp/releases/latest"
    PACKAGE_LIST_URL = "https://csplink.top"


SETTINGS = Settings()
qconfig.load('csplink.config', SETTINGS)
