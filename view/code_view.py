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
# @file        code_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-20     xqyjlj       initial version
#

from PyQt5.QtCore import Qt, QEasingCurve, QItemSelection
from PyQt5.QtGui import QShowEvent
from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QPlainTextEdit, QLabel, QHBoxLayout, QFrame, QSizePolicy
from qfluentwidgets import (FluentIconBase, qrouter, SegmentedWidget, TabBar, CheckBox, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar, SegmentedToggleToolWidget,
                            FluentIcon)

from .ui.Ui_code_view import Ui_CodeView
from common import Style, Icon, Coder, Utils, PROJECT
from widget import CHighlighter


class CodeView(Ui_CodeView, QWidget):
    """ Tab interface """

    m_codes = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.cardWidget_file.setFixedWidth(300)
        self.treeWidget_file.header().setVisible(False)
        self.treeWidget_file.selectionModel().selectionChanged.connect(self.treeWidget_fileSelectionChanged)

        Style.CODE_VIEW.apply(self)

    def showEvent(self, event: QShowEvent):
        super().showEvent(event)
        coder = Coder()
        self.m_codes = coder.dump(PROJECT.halPath)
        tree = Utils.paths2Dict(self.m_codes)

        self.treeWidget_file.clear()
        self.plainTextEdit.clear()

        def traverse_tree(tree: dict, top_item: QTreeWidgetItem, path: str):
            for key, value in tree.items():
                if isinstance(value, dict):
                    item = QTreeWidgetItem(top_item, [key])
                    item.setIcon(0, FluentIconBase.qicon(Icon.FOLDER_LIB))
                    traverse_tree(value, item, f"{path}/{key}")
                    item.setExpanded(True)
                else:
                    item = QTreeWidgetItem(top_item, [key])
                    item.setData(0, Qt.ItemDataRole.StatusTipRole, f"{path}/{key}")
                    if key.lower().endswith(".h"):
                        item.setIcon(0, FluentIconBase.qicon(Icon.H))
                    elif key.lower().endswith(".c"):
                        item.setIcon(0, FluentIconBase.qicon(Icon.C))

        for key, di in tree.get("core", {}).items():
            top_level_item = QTreeWidgetItem([key])
            top_level_item.setIcon(0, FluentIconBase.qicon(Icon.FOLDER_LIB))
            top_level_item.setExpanded(True)
            self.treeWidget_file.addTopLevelItem(top_level_item)
            traverse_tree(di, top_level_item, f"core/{key}")
            top_level_item.setExpanded(True)

    def treeWidget_fileSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            path = str(index.data(Qt.ItemDataRole.StatusTipRole))
            if path != "None":
                self.plainTextEdit.setPlainText(self.m_codes.get(path, ""))
                self.highlighter = CHighlighter(self.plainTextEdit.document())
