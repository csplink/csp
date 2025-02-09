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

import attr
from PySide6.QtCore import (
    Qt,
    QModelIndex,
    QAbstractItemModel,
    QSortFilterProxyModel,
    QItemSelection,
)
from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout
from loguru import logger
from qfluentwidgets import TreeView

from common import PROJECT, SETTINGS, SIGNAL_BUS, SUMMARY, IP


def isPrivateModelOrNone(_, attribute, value):
    if value is not None and not isinstance(value, PModel):
        raise ValueError(f"{attribute.name} must be a PModel instance or None")


@attr.s
class PModel:
    displayName: str = attr.ib(default="", validator=attr.validators.instance_of(str))
    description: str = attr.ib(default="", validator=attr.validators.instance_of(str))
    children: list = attr.ib(default=[], validator=attr.validators.instance_of(list))
    parent: PModel | None = attr.ib(default=None)

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
    __model = PModel()

    SELECTED_COLOR = QColor(0, 204, 68)
    __brush = QBrush()
    __brush.setColor(SELECTED_COLOR)

    __font = QFont("JetBrains Mono")
    __font.setPixelSize(12)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__loadModule()

    # noinspection PyMethodOverriding
    def rowCount(self, parent: QModelIndex) -> int:
        if not parent.isValid():
            return len(self.__model.children)
        else:
            model: PModel = parent.internalPointer()  # type: ignore
            return len(model.children)

    # noinspection PyMethodOverriding
    def columnCount(self, parent: QModelIndex) -> int:
        return 1

    # noinspection PyMethodOverriding
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        if (
            role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole
        ):  # 0, 2
            model: PModel = index.internalPointer()  # type: ignore
            return model.displayName
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            model: PModel = index.internalPointer()  # type: ignore
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
            model: PModel = index.internalPointer()  # type: ignore
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

    # noinspection PyMethodOverriding
    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentModel = self.__model
        else:
            parentModel = parent.internalPointer()

        childModel: PModel = parentModel.child(row)  # type: ignore
        if childModel is not None:
            return self.createIndex(row, column, childModel)
        else:
            return QModelIndex()

    # noinspection PyMethodOverriding
    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        childModel: PModel = index.internalPointer()  # type: ignore
        parentModel = childModel.parent

        if parentModel == self.__model:
            return QModelIndex()

        if parentModel is None:
            logger.error("The parent model is None")
            return QModelIndex()

        return self.createIndex(parentModel.row(), 0, parentModel)

    def __loadModule(self):
        locale = SETTINGS.get(SETTINGS.language).value.name()
        for group, moduleGroup in SUMMARY.projectSummary().modules.items():
            model = PModel(group, "", [], self.__model)
            for name, module in moduleGroup.items():
                model_child = PModel(name, module.description.get(locale), [], model)
                model.append(model_child)
            self.__model.append(model)
        self.modelReset.emit()


class TreeModule(QWidget):

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
        self, selected: QItemSelection, _: QItemSelection
    ):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            if str(index.parent().data()) != "None":
                instance = str(index.data())
                ip = IP.projectIps().get(instance)
                if ip is None:
                    logger.error(f'the ip instance:"{instance}" is invalid.')
                    return
                if instance == SUMMARY.projectSummary().pinInstance():
                    SIGNAL_BUS.controlManagerTriggered.emit(
                        instance, "widget_control_io_manager"
                    )
                else:
                    SIGNAL_BUS.controlManagerTriggered.emit(
                        instance, "widget_control_ip_manager"
                    )
                    SIGNAL_BUS.modeManagerTriggered.emit(instance, "")
