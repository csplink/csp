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
# @file        view_code.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-20     xqyjlj       initial version
#

import os

from PySide6.QtCore import Qt, Signal, QItemSelection
from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QFrame, QLabel, QHBoxLayout, QFrame, QSizePolicy
from qfluentwidgets import (FluentIconBase, qrouter, FlowLayout, PushButton, ToolButton, ComboBox,
                            TabCloseButtonDisplayMode, BodyLabel, SpinBox, BreadcrumbBar, SegmentedToggleToolWidget,
                            FluentIcon)

from .ui.ui_view_code import Ui_view_code
from common import Style, Icon, Coder, Utils, PROJECT, PACKAGE
from widget import CHighlighter
from dialogs import GenCodeDialog


class view_code(Ui_view_code, QWidget):
    """ Tab interface """

    m_codes = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.cardWidget_file.setFixedWidth(300)
        self.treeWidget_file.header().setVisible(False)
        self.treeWidget_file.selectionModel().selectionChanged.connect(self.__on__treeWidget_file__selectionChanged)

        layout = FlowLayout(None, False)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        self.tb_gen_settings = ToolButton()
        self.tb_gen_settings.setIcon(Icon.EQUALIZER)
        self.tb_gen_settings.pressed.connect(self.__on__tb_gen_settings__pressed)
        layout.addWidget(self.tb_gen_settings)

        self.verticalLayout_cardWidget_file.insertLayout(0, layout)

        Style.VIEW_CODE.apply(self)

    def __check_gen_setting(self) -> bool:
        if not os.path.isdir(PROJECT.toolchainsPath):
            return False
        elif not os.path.isdir(PROJECT.halPath):
            return False
        elif PROJECT.builder == "":
            return False
        elif PROJECT.builderVersion == "":
            return False

        if (not Utils.ishex(PROJECT.defaultHeapSize)) and Utils.ishex(PROJECT.summary.defaultHeapSize):
            return False
        elif not Utils.ishex(PROJECT.defaultStackSize) and Utils.ishex(PROJECT.summary.defaultStackSize):
            return False

        return True

    def flush(self):
        self.treeWidget_file.clear()
        self.plainTextEdit.clear()

        if not self.__check_gen_setting():
            dialog = GenCodeDialog(self, False)
            if not dialog.exec():
                return

        coder = Coder()
        self.m_codes = coder.dump(PROJECT.halPath)
        tree = Utils.paths2dict(self.m_codes)

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

    def __on__treeWidget_file__selectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            path = str(index.data(Qt.ItemDataRole.StatusTipRole))
            if path != "None":
                self.plainTextEdit.setPlainText(self.m_codes.get(path, ""))
                self.highlighter = CHighlighter(self.plainTextEdit.document())

    def __on__tb_gen_settings__pressed(self):
        dialog = GenCodeDialog(self, False)
        dialog.exec()
