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
        self,
        display_name: str,
        description: str,
        children: list,
        parent: _PModel | None,
    ):
        self.__display_name = display_name
        self.__description = description
        self.__children = children
        self.__parent = parent

    # region getter/setter

    @property
    def display_name(self) -> str:
        return self.__display_name

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

        self.__load_module()
        PROJECT.project().modules_changed.connect(self.__on_project_modulesChanged)

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
            return model.display_name
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
            if model.display_name in PROJECT.project().modules:
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
            parent_model = self.__model
        else:
            parent_model: _PModel = parent.internalPointer()  # type: ignore

        child_model: _PModel = parent_model.child(row)  # type: ignore
        if child_model is not None:
            return self.createIndex(row, column, child_model)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_model: _PModel = index.internalPointer()  # type: ignore
        parent_model = child_model.parent

        if parent_model == self.__model:
            return QModelIndex()

        if parent_model is None:
            logger.error("The parent model is None")
            return QModelIndex()

        return self.createIndex(parent_model.row(), 0, parent_model)

    # endregion

    def __load_module(self):
        locale = SETTINGS.get(SETTINGS.language).value.name()
        peripherals = SUMMARY.project_summary().modules.peripherals
        if peripherals:
            model_root = _PModel("peripherals", "", [], self.__model)
            self.__model.append(model_root)
            for group, module_group in peripherals.items():
                model = _PModel(group, "", [], model_root)
                for name, module in module_group.items():
                    if module.ip:
                        child = _PModel(name, module.description.get(locale), [], model)
                        model.append(child)
                if len(model.children) > 0:
                    model_root.append(model)

        middlewares = SUMMARY.project_summary().modules.middlewares
        if middlewares:
            model_root = _PModel("middlewares", "", [], self.__model)
            self.__model.append(model_root)
            for group, module_group in middlewares.items():
                model = _PModel(group, "", [], model_root)
                for name, module in module_group.items():
                    if module.ip:
                        child = _PModel(name, module.description.get(locale), [], model)
                        model.append(child)
                if len(model.children) > 0:
                    model_root.append(model)

        self.modelReset.emit()

    def __on_project_modulesChanged(self, old: list[str], new: list[str]):
        self.refresh()

    def refresh(self):
        root_index = QModelIndex()  # The root index is empty
        self.__refresh_recursively(root_index)

    def __refresh_recursively(self, parent):
        rows = self.rowCount(parent)
        cols = self.columnCount(parent)
        if rows == 0 or cols == 0:
            return

        top_left = self.index(0, 0, parent)
        bottom_right = self.index(rows - 1, cols - 1, parent)
        self.dataChanged.emit(top_left, bottom_right)

        for row in range(rows):
            child = self.index(row, 0, parent)
            self.__refresh_recursively(child)


class TreeModule(QWidget):
    selection_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        # ----------------------------------------------------------------------
        self.h_layout = QHBoxLayout(self)
        self.h_layout.setContentsMargins(0, 0, 0, 0)
        self.tree_view_modules = TreeView(self)
        self.h_layout.addWidget(self.tree_view_modules)
        # ----------------------------------------------------------------------

        self.tree_view_modules.header().hide()

        proxy_model = QSortFilterProxyModel(self)
        model = TreeModuleModel(self)
        proxy_model.setSourceModel(model)
        self.tree_view_modules.setModel(proxy_model)
        self.tree_view_modules.expandAll()
        self.tree_view_modules.selectionModel().selectionChanged.connect(
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
                ips = IP.project_ips()
                ip = ips[instance]
                pins = []
                for signal in ip.signals():
                    pins.extend(SUMMARY.find_pins_by_signal(signal))
                self.selection_changed.emit(instance)
                SIGNAL_BUS.highlight_pin_triggered.emit(pins)
