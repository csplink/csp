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
# @file        __init__.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-01     xqyjlj        initial version
#

__all__ = []

from .highlighter import BaseHighlighter, CHighlighter

__all__ += ["BaseHighlighter", "CHighlighter"]

from .packages import LQFP

__all__ += ["LQFP"]

from .settings import (ComboBoxPropertySettingCard, LineEditPropertySettingCard, SwitchPropertySettingCard,
                       ToolButtonPropertySettingCard)

__all__ += [
    "ComboBoxPropertySettingCard",
    "LineEditPropertySettingCard",
    "SwitchPropertySettingCard",
    "ToolButtonPropertySettingCard",
]

from .graphics_item_chip_body import GraphicsItemChipBody
from .graphics_item_pin import GraphicsItemPin
from .graphics_view_pan_zoom import GraphicsViewPanZoom
from .grid_mode_io import GridModeIo
# from .grid_mode_ip import GridModeIp
from .grid_property_ip import GridPropertyIp
from .list_contributors import ListContributors
from .plain_text_edit_code import PlainTextEditCode
from .stacked_widget import StackedWidget
from .tree_module import TreeModule

__all__ += [
    "GraphicsItemChipBody",
    "GraphicsItemPin",
    "GraphicsViewPanZoom",
    "GridModeIo",
    "GridPropertyIp",
    "ListContributors",
    "PlainTextEditCode",
    "StackedWidget",
    "TreeModule",
]
