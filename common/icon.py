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

from enum import Enum

from qfluentwidgets import getIconColor, Theme, FluentIconBase


class Icon(FluentIconBase, Enum):
    """ Custom icons """

    CPU = "cpu-line"
    REFRESH = "refresh-line"
    ZOOM_IN = "zoom-in-line"
    ZOOM_OUT = "zoom-out-line"
    MONEY = "money-cny-circle-line"
    SETTING = "settings-line"
    GENERATE = "ai-generate"

    def path(self, theme=Theme.AUTO):
        return f'resource/icon/{getIconColor(theme)}/{self.value}.svg'
