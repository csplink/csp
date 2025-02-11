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

from PySide6.QtCore import Qt, QItemSelection
from PySide6.QtWidgets import QWidget, QTreeWidgetItem
from loguru import logger
from qfluentwidgets import FlowLayout, MessageBox

from common import Style, Icon, Coder, PROJECT, SIGNAL_BUS
from utils import Converters
from widget import CHighlighter
from .ui.code_view_ui import Ui_CodeView


class CodeView(Ui_CodeView, QWidget):
    """Tab interface"""

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.codes = {}

        self.fileCard.setFixedWidth(300)
        self.fileTree.header().setVisible(False)
        self.fileTree.selectionModel().selectionChanged.connect(
            self.__on_fileTree_selectionChanged
        )

        layout = FlowLayout(None, False)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setVerticalSpacing(20)
        layout.setHorizontalSpacing(10)

        self.verticalLayout_cardWidget_file.insertLayout(0, layout)

        Style.CODE_VIEW.apply(self)

    def flush(self):
        self.fileTree.clear()
        self.plainTextEdit.clear()

        succeed, msg = PROJECT.isGenerateSettingValid()
        if not succeed:
            logger.error(msg)
            title = self.tr("Error")  # type: ignore
            content = self.tr("The coder settings is invalid. Please check it.")  # type: ignore
            message = MessageBox(title, content, self.window())
            message.setContentCopyable(True)
            message.cancelButton.setDisabled(True)
            message.raise_()
            message.exec()
            SIGNAL_BUS.navigationRequested.emit("SettingView", "GenerateSettingView")
            return

        coder = Coder()
        self.codes = coder.dump()
        tree = Converters.paths2dict(list(self.codes.keys()))

        def traverseTree(treeItem: dict, topItem: QTreeWidgetItem, path: str):
            for k, v in treeItem.items():
                if isinstance(v, dict):
                    item = QTreeWidgetItem(topItem, [k])
                    item.setIcon(0, Icon.M_FOLDER_LIB.qicon())
                    traverseTree(v, item, f"{path}/{k}")
                    item.setExpanded(True)
                else:
                    item = QTreeWidgetItem(topItem, [k])
                    item.setData(0, Qt.ItemDataRole.StatusTipRole, f"{path}/{k}")
                    if k.lower().endswith(".h"):
                        item.setIcon(0, Icon.M_H.qicon())
                    elif k.lower().endswith(".c"):
                        item.setIcon(0, Icon.M_C.qicon())

        for key, di in tree.items():
            topLevelItem = QTreeWidgetItem([key])
            topLevelItem.setExpanded(True)
            self.fileTree.addTopLevelItem(topLevelItem)
            if isinstance(di, dict):
                topLevelItem.setIcon(0, Icon.M_FOLDER_LIB.qicon())
                traverseTree(di, topLevelItem, key)
            else:
                topLevelItem.setIcon(0, Icon.M_FILE.qicon())
                topLevelItem.setData(0, Qt.ItemDataRole.StatusTipRole, key)
            topLevelItem.setExpanded(True)

    def __on_fileTree_selectionChanged(
        self, selected: QItemSelection, _: QItemSelection
    ):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            path = str(index.data(Qt.ItemDataRole.StatusTipRole))
            if path != "None":
                self.plainTextEdit.setPlainText(self.codes.get(path, ""))
                self.highlighter = CHighlighter(self.plainTextEdit.document())
