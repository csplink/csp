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
from enum import Enum

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

    # folders
    databaseFolder = ConfigItem("Folders", "Database", "resource/database", FolderValidator())

    # system
    language = OptionsConfigItem("System",
                                 "language_type",
                                 LanguageType.AUTO,
                                 OptionsValidator(LanguageType),
                                 LanguageSerializer(),
                                 restart=True)
    checkUpdateAtStartup = ConfigItem("System", "CheckUpdateAtStartup", True, BoolValidator())
    dpiScale = OptionsConfigItem("System",
                                 "DpiScale",
                                 "Auto",
                                 OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
                                 restart=True)

    # style. overloading the parent class
    themeMode = OptionsConfigItem("Style", "ThemeMode", Theme.AUTO, OptionsValidator(Theme), EnumSerializer(Theme))
    themeColor = ColorConfigItem("Style", "ThemeColor", '#009faa')
    alertColor = ColorConfigItem("Style", "AlertColor", '#c04851')

    # misc
    lastOpenProjectFolder = ConfigItem(
        "Misc", "LastOpenProjectFolder",
        QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation), FolderValidator())


YEAR = 2023
AUTHOR = "xqyjlj"
VERSION = "0.1.0"
HELP_URL = "https://csplink.top"
REPO_URL = "https://github.com/csplink/csp"
FEEDBACK_URL = "https://github.com/csplink/csp/issues"
RELEASE_URL = "https://github.com/csplink/csp/releases/latest"
REPOSITORY_FOLDER = f"{os.getcwd()}/repository"
REPOSITORY_INDEX_FILE = f"{os.getcwd()}/repository.index"
CONTRIBUTORS_FILE = f"{os.getcwd()}/resource/contributors/contributors"

SETTINGS = Settings()
qconfig.load('csplink.config', SETTINGS)
