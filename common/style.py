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
# @file        style.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-22     xqyjlj       initial version
#

import os
from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig

from .settings import SETTINGS


class Style(StyleSheetBase, Enum):
    """ Style sheet  """

    CHIP_VIEW = "chip_view"
    CODE_VIEW = "code_view"
    GRID_PROPERTY_IP_COMBOBOX = "grid_property_ip.ComboBox"
    PACKAGE_VIEW = "package_view"
    PLAIN_TEXT_EDIT_CODE = "plain_text_edit_code"
    SETTING_VIEW = "setting_view"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return os.path.join(SETTINGS.STYLE_FOLDER, theme.value.lower(), f"{self.value}.qss")
