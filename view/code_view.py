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

from .ui.ui_code_view import Ui_CodeView
from common import Style, Icon, Coder, PROJECT, PACKAGE
from widget import CHighlighter
from dialogs import GenCodeDialog
from utils import converters


class CodeView(Ui_CodeView, QWidget):
    """ Tab interface """

    codes = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.fileCard.setFixedWidth(300)
        self.fileTree.header().setVisible(False)
        self.fileTree.selectionModel().selectionChanged.connect(self.__on_fileTree_selectionChanged)

        layout = FlowLayout(None, False)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        self.genSettingsBtn = ToolButton()
        self.genSettingsBtn.setIcon(Icon.EQUALIZER)
        self.genSettingsBtn.pressed.connect(self.__on_genSettingsBtn_pressed)
        layout.addWidget(self.genSettingsBtn)

        self.verticalLayout_cardWidget_file.insertLayout(0, layout)

        Style.VIEW_CODE.apply(self)

    def __checkGenSetting(self) -> bool:
        if not os.path.isdir(PROJECT.toolchains_path):
            return False
        elif not os.path.isdir(PROJECT.hal_path):
            return False
        elif PROJECT.builder == "":
            return False
        elif PROJECT.builder_version == "":
            return False

        if (not converters.ishex(PROJECT.default_heap_size)) and converters.ishex(PROJECT.summary.default_heap_size):
            return False
        elif not converters.ishex(PROJECT.default_stack_size) and converters.ishex(PROJECT.summary.default_stack_size):
            return False

        return True

    def flush(self):
        self.fileTree.clear()
        self.plainTextEdit.clear()

        if not self.__checkGenSetting():
            dialog = GenCodeDialog(self, False)
            if not dialog.exec():
                return

        coder = Coder()
        self.codes = coder.dump(PROJECT.hal_path)
        tree = converters.paths2dict(self.codes)

        def traverseTree(tree: dict, top_item: QTreeWidgetItem, path: str):
            for key, value in tree.items():
                if isinstance(value, dict):
                    item = QTreeWidgetItem(top_item, [key])
                    item.setIcon(0, FluentIconBase.qicon(Icon.FOLDER_LIB))
                    traverseTree(value, item, f"{path}/{key}")
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
            self.fileTree.addTopLevelItem(top_level_item)
            traverseTree(di, top_level_item, f"core/{key}")
            top_level_item.setExpanded(True)

    def __on_fileTree_selectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            path = str(index.data(Qt.ItemDataRole.StatusTipRole))
            if path != "None":
                self.plainTextEdit.setPlainText(self.codes.get(path, ""))
                self.highlighter = CHighlighter(self.plainTextEdit.document())

    def __on_genSettingsBtn_pressed(self):
        dialog = GenCodeDialog(self, False)
        dialog.exec()
