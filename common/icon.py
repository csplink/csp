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
# @file        icon.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import os
from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase

from .settings import SETTINGS


class Icon(FluentIconBase, Enum):
    """ Custom icons """
    M_C = "material/c"
    M_FOLDER_BASE = "material/folder-base"
    M_FOLDER_BASE_OPEN = "material/folder-base-open"
    M_FOLDER_DIST = "material/folder-dist"
    M_FOLDER_DIST_OPEN = "material/folder-dist-open"
    M_FOLDER_LIB = "material/folder-lib"
    M_FOLDER_LIB_OPEN = "material/folder-lib-open"
    M_FOLDER_PACKAGES = "material/folder-packages"
    M_FOLDER_PACKAGES_OPEN = "material/folder-packages-open"
    M_H = "material/h"
    # ------------------------------------------------------------------------------------------------------------------
    AI_GENERATE = "ai-generate"
    BOOK_SHELF = "book-shelf-line"
    BOX = "box-3-line"
    CHECKBOX_MULTIPLE = "checkbox-multiple-line"
    CLOSE_LARGE = "close-large-line"
    CODE = "code-line"
    CPU = "cpu-line"
    DATABASE_2 = "database-2-line"
    EQUALIZER = "equalizer-line"
    FEEDBACK = "feedback-line"
    FOLDER = "folder-6-line"
    FOLDER_TRANSFER = "folder-transfer-line"
    GITHUB = "github-fill"
    GLOBAL = "global-line"
    HAMMER = "hammer-line"
    INFORMATION = "information-line"
    INSTALL = "install-line"
    LANDSCAPE = "landscape-line"
    LIST_SETTINGS = "list-settings-line"
    MONEY = "money-cny-circle-line"
    MORE = "more-line"
    NUMBERS = "numbers-line"
    PAINT = "paint-brush-line"
    PALETTE = "palette-line"
    PICTURE_IN_PICTURE = "picture-in-picture-line"
    QUESTION = "question-line"
    REFRESH = "refresh-line"
    SETTING = "settings-line"
    SPEED_UP = "speed-up-line"
    STACK = "stack-line"
    TIME = "time-line"
    TOOLS = "tools-line"
    UNINSTALL = "uninstall-line"
    ZOOM_IN = "zoom-in-line"
    ZOOM_OUT = "zoom-out-line"

    def path(self, theme=Theme.AUTO):
        if self.value.startswith("material/"):
            return os.path.join(SETTINGS.ICON_FOLDER, f"{self.value}.svg")
        return os.path.join(SETTINGS.ICON_FOLDER, 'remix', getIconColor(theme), f"{self.value}.svg")
