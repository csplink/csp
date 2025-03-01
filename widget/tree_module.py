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
# @file        tree_module.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-13     xqyjlj       initial version
#

from __future__ import annotations


from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractItemModel,
    QSortFilterProxyModel,
    QItemSelection,
    Signal,
)
from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout
from loguru import logger
from qfluentwidgets import TreeView

from common import PROJECT, SETTINGS, SUMMARY, IP
from common.signal_bus import SIGNAL_BUS


class _PModel:
    def __init__(
        self, displayName: str, description: str, children: list, parent: _PModel | None
    ):
        self.__displayName = displayName
        self.__description = description
        self.__children = children
        self.__parent = parent

    # region getter/setter

    @property
    def displayName(self) -> str:
        return self.__displayName

    @property
    def description(self) -> str:
        return self.__description

    @property
    def children(self) -> list[_PModel]:
        return self.__children

    @property
    def parent(self) -> _PModel | None:
        return self.__parent

    # endregion

    def append(self, model):
        self.children.append(model)

    def child(self, row: int):
        if row < 0 or row >= len(self.children):
            return None
        return self.children[row]

    def row(self) -> int:
        if self.parent is not None:
            return self.parent.children.index(self)
        return 0


class TreeModuleModel(QAbstractItemModel):
    SELECTED_COLOR = QColor(0, 204, 68)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__model = _PModel("", "", [], None)

        self.__brush = QBrush()
        self.__brush.setColor(self.SELECTED_COLOR)

        self.__font = QFont("JetBrains Mono")
        self.__font.setPixelSize(12)

        self.__loadModule()
        PROJECT.project().modulesChanged.connect(self.__on_project_modulesChanged)

    # region overrides

    def rowCount(self, parent: QModelIndex) -> int:
        if not parent.isValid():
            return len(self.__model.children)
        else:
            model: _PModel = parent.internalPointer()  # type: ignore
            return len(model.children)

    def columnCount(self, parent: QModelIndex) -> int:
        return 1

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        model: _PModel = index.internalPointer()  # type: ignore

        if (
            role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole
        ):  # 0, 2
            return model.displayName
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            return model.description
        elif role == Qt.ItemDataRole.StatusTipRole:  # 4
            return None
        elif role == Qt.ItemDataRole.FontRole:  # 6
            return self.__font
        elif role == Qt.ItemDataRole.TextAlignmentRole:  # 7
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.BackgroundRole:  # 8
            return None
        elif role == Qt.ItemDataRole.ForegroundRole:  # 9
            if model.displayName in PROJECT.project().modules:
                return self.__brush
            return None
        elif role == Qt.ItemDataRole.CheckStateRole:  # 10
            return None
        elif role == Qt.ItemDataRole.SizeHintRole:  # 13
            return None
        else:
            return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        return super().flags(index)

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentModel = self.__model
        else:
            parentModel: _PModel = parent.internalPointer()  # type: ignore

        childModel: _PModel = parentModel.child(row)  # type: ignore
        if childModel is not None:
            return self.createIndex(row, column, childModel)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        childModel: _PModel = index.internalPointer()  # type: ignore
        parentModel = childModel.parent

        if parentModel == self.__model:
            return QModelIndex()

        if parentModel is None:
            logger.error("The parent model is None")
            return QModelIndex()

        return self.createIndex(parentModel.row(), 0, parentModel)

    # endregion

    def __loadModule(self):
        locale = SETTINGS.get(SETTINGS.language).value.name()
        peripherals = SUMMARY.projectSummary().modules.peripherals
        if peripherals:
            modelRoot = _PModel("peripherals", "", [], self.__model)
            self.__model.append(modelRoot)
            for group, moduleGroup in peripherals.items():
                model = _PModel(group, "", [], modelRoot)
                for name, module in moduleGroup.items():
                    if module.ip:
                        child = _PModel(name, module.description.get(locale), [], model)
                        model.append(child)
                if len(model.children) > 0:
                    modelRoot.append(model)

        middlewares = SUMMARY.projectSummary().modules.middlewares
        if middlewares:
            modelRoot = _PModel("middlewares", "", [], self.__model)
            self.__model.append(modelRoot)
            for group, moduleGroup in middlewares.items():
                model = _PModel(group, "", [], modelRoot)
                for name, module in moduleGroup.items():
                    if module.ip:
                        child = _PModel(name, module.description.get(locale), [], model)
                        model.append(child)
                if len(model.children) > 0:
                    modelRoot.append(model)

        self.modelReset.emit()

    def __on_project_modulesChanged(self, old: list[str], new: list[str]):
        self.refresh()

    def refresh(self):
        rootIndex = QModelIndex()  # The root index is empty
        self.__refreshRecursively(rootIndex)

    def __refreshRecursively(self, parent):
        rows = self.rowCount(parent)
        cols = self.columnCount(parent)
        if rows == 0 or cols == 0:
            return

        topLeft = self.index(0, 0, parent)
        bottomRight = self.index(rows - 1, cols - 1, parent)
        self.dataChanged.emit(topLeft, bottomRight)

        for row in range(rows):
            child = self.index(row, 0, parent)
            self.__refreshRecursively(child)


class TreeModule(QWidget):
    selectionChanged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # ----------------------------------------------------------------------
        self.hLayout = QHBoxLayout(self)
        self.hLayout.setContentsMargins(0, 0, 0, 0)
        self.treeView_modules = TreeView(self)
        self.hLayout.addWidget(self.treeView_modules)
        # ----------------------------------------------------------------------

        self.treeView_modules.header().hide()

        proxyModel = QSortFilterProxyModel(self)
        model = TreeModuleModel(self)
        proxyModel.setSourceModel(model)
        self.treeView_modules.setModel(proxyModel)
        self.treeView_modules.expandAll()
        self.treeView_modules.selectionModel().selectionChanged.connect(
            self.treeView_modulesSelectionChanged
        )

    def treeView_modulesSelectionChanged(
        self, selected: QItemSelection, deselected: QItemSelection
    ):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            if index.parent().data() != None and index.parent().parent().data() != None:
                instance = str(index.data())
                ips = IP.projectIps()
                ip = ips[instance]
                pins = []
                for signal in ip.signals():
                    pins.extend(SUMMARY.findPinsBySignal(signal))
                self.selectionChanged.emit(instance)
                SIGNAL_BUS.highlightPinTriggered.emit(pins)
