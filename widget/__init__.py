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

from .clock_tree import (
    BaseClockTreeWidget,
    EnumClockTreeWidget,
    FloatClockTreeWidget,
    IntegerClockTreeWidget,
    NumberClockTreeWidget,
    RadioClockTreeWidget,
)
from .graphics_item_chip_body import GraphicsItemChipBody
from .graphics_item_pin import GraphicsItemPin
from .graphics_view_pan_zoom import GraphicsViewPanZoom
from .highlighter import BaseHighlighter, CHighlighter
from .list_contributors import ListContributors
from .packages import LQFP
from .plain_text_edit_code import PlainTextEditCode
from .plain_text_edit_logger import PlainTextEditLogger
from .plain_text_edit_readonly import PlainTextEditReadonly
from .settings import (
    ComboBoxPropertySettingCard,
    LineEditPropertySettingCard,
    SwitchPropertySettingCard,
    ToolButtonPropertySettingCard,
)
from .stacked_widget import StackedWidget
from .tree_module import TreeModule
from .widget_control_dashboard import WidgetControlDashboard
from .widget_control_manager import WidgetControlManager
from .widget_mode_manager import WidgetModeManager

# fmt: off
__all__ = [
    "GraphicsItemChipBody",
    "GraphicsItemPin",
    "GraphicsViewPanZoom",
    "BaseHighlighter", "CHighlighter",
    "ListContributors",
    "LQFP",
    "PlainTextEditCode",
    "PlainTextEditLogger",
    "PlainTextEditReadonly",

    "ComboBoxPropertySettingCard", "LineEditPropertySettingCard",
    "SwitchPropertySettingCard", "ToolButtonPropertySettingCard",

    "BaseClockTreeWidget", "EnumClockTreeWidget", "FloatClockTreeWidget",
    "IntegerClockTreeWidget", "NumberClockTreeWidget", "RadioClockTreeWidget",

    "StackedWidget",
    "TreeModule",
    "WidgetControlDashboard",
    "WidgetControlManager",
    "WidgetModeManager",
]
# fmt: on
