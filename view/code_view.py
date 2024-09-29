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

import os

from PySide6.QtCore import Qt, QItemSelection
# from PySide6.QtGui import QShowEvent
from PySide6.QtWidgets import QWidget, QTreeWidgetItem
from qfluentwidgets import (FlowLayout, ToolButton)

from common import Style, Icon, Coder, PROJECT
from dialogs import GenCodeDialog
from utils import converters
from widget import CHighlighter
from .ui.code_view_ui import Ui_CodeView


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

        Style.CODE_VIEW.apply(self)

    def __checkGenSetting(self) -> bool:
        if not os.path.isdir(PROJECT.toolchainsDir):
            return False
        elif not os.path.isdir(PROJECT.halDir):
            return False
        elif PROJECT.builder == "":
            return False
        elif PROJECT.builderVersion == "":
            return False

        if (not converters.ishex(PROJECT.defaultHeapSize)) and converters.ishex(PROJECT.summary.defaultHeapSize):
            return False
        elif not converters.ishex(PROJECT.defaultStackSize) and converters.ishex(PROJECT.summary.defaultStackSize):
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
        self.codes = coder.dump(PROJECT.halDir)
        tree = converters.paths2dict(self.codes)

        def traverseTree(treeItem: dict, top_item: QTreeWidgetItem, path: str):
            for k, v in treeItem.items():
                if isinstance(v, dict):
                    item = QTreeWidgetItem(top_item, [k])
                    item.setIcon(0, Icon.M_FOLDER_LIB.qicon())
                    traverseTree(v, item, f"{path}/{k}")
                    item.setExpanded(True)
                else:
                    item = QTreeWidgetItem(top_item, [k])
                    item.setData(0, Qt.ItemDataRole.StatusTipRole, f"{path}/{k}")
                    if k.lower().endswith(".h"):
                        item.setIcon(0, Icon.M_H.qicon())
                    elif k.lower().endswith(".c"):
                        item.setIcon(0, Icon.M_C.qicon())

        for key, di in tree.get("core", {}).items():
            top_level_item = QTreeWidgetItem([key])
            top_level_item.setIcon(0, Icon.M_FOLDER_LIB.qicon())
            top_level_item.setExpanded(True)
            self.fileTree.addTopLevelItem(top_level_item)
            traverseTree(di, top_level_item, f"core/{key}")
            top_level_item.setExpanded(True)

    def __on_fileTree_selectionChanged(self, selected: QItemSelection, _: QItemSelection):
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
