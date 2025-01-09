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
# @file        integer_clock_tree_widget.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-05     xqyjlj       initial version
#

from PySide6.QtCore import QRegularExpression
from PySide6.QtGui import QRegularExpressionValidator
from PySide6.QtWidgets import QLineEdit
from jinja2 import Template

from common import ClockTreeType, IpType
from .number_clock_tree_widget import NumberClockTreeWidget


class IntegerClockTreeWidget(NumberClockTreeWidget, QLineEdit):
    def __init__(self, id_: str, instance: str, param: str, element: ClockTreeType.ElementUnitType,
                 parameter: IpType.ParameterUnitType, clockTree: ClockTreeType, template: Template, data: dict,
                 parent=None):
        NumberClockTreeWidget.__init__(self, id_, instance, param, element, parameter, clockTree, template, data,
                                       parent)
        self.setObjectName("integerWidget")
        self.setValidator(QRegularExpressionValidator(QRegularExpression(R"^\d+$")))
