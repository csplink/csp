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

import sys
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator, OptionsValidator,
                            EnumSerializer, ColorConfigItem, FolderListValidator, Theme, FolderValidator,
                            ConfigSerializer)


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    CHINESE_TRADITIONAL = QLocale(QLocale.Chinese, QLocale.HongKong)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


class Settings(QConfig):
    """ Config of application """

    # folders
    databaseFolder = ConfigItem("Folders", "Database", "resource/database", FolderValidator())

    # system
    language = OptionsConfigItem("System",
                                 "Language",
                                 Language.AUTO,
                                 OptionsValidator(Language),
                                 LanguageSerializer(),
                                 restart=True)
    checkUpdateAtStartUp = ConfigItem("System", "CheckUpdateAtStartUp", True, BoolValidator())
    dpiScale = OptionsConfigItem("System",
                                 "DpiScale",
                                 "Auto",
                                 OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]),
                                 restart=True)

    # style
    themeMode = OptionsConfigItem("Style", "ThemeMode", Theme.AUTO, OptionsValidator(Theme), EnumSerializer(Theme))
    themeColor = ColorConfigItem("Style", "ThemeColor", '#009faa')


YEAR = 2023
AUTHOR = "xqyjlj"
VERSION = "0.1.0"
HELP_URL = "https://csplink.top"
REPO_URL = "https://github.com/csplink/csp"
FEEDBACK_URL = "https://github.com/csplink/csp/issues"
RELEASE_URL = "https://github.com/csplink/csp/releases/latest"

SETTINGS = Settings()
qconfig.load('csplink.config', SETTINGS)
