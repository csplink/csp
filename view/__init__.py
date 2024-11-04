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
# 2024-07-01     xqyjlj       initial version
#

from .clock_tree_view import ClockTreeView
from .code_view import CodeView
from .main_window import MainWindow
from .new_project_window import NewProjectWindow
from .package_view import PackageView
from .setting_view import SettingView
from .soc_view import SocView
from .startup_window import StartupWindow

__all__ = [
    'ClockTreeView',
    'CodeView',
    'MainWindow',
    'NewProjectWindow',
    'PackageView',
    'SettingView',
    'SocView',
    'StartupWindow',
]
