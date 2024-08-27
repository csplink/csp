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

import attr

from PySide6.QtCore import Qt, QModelIndex, QAbstractItemModel, QSortFilterProxyModel, QItemSelection
from PySide6.QtGui import QFont, QBrush, QColor
from PySide6.QtWidgets import (QWidget)

from .ui.Ui_tree_module import Ui_TreeModule
from common import PROJECT, SETTINGS


def is_private_model_or_none(instance, attribute, value):
    if value is not None and not isinstance(value, PModel):
        raise ValueError(f"{attribute.name} must be a PModel instance or None")


@attr.s
class PModel():
    displayName = attr.ib(default="", validator=attr.validators.instance_of(str))
    description = attr.ib(default="", validator=attr.validators.instance_of(str))
    children = attr.ib(default=[], validator=attr.validators.instance_of(list))
    parent = attr.ib(default=None)

    def append(self, model):
        self.children.append(model)

    def child(self, row: int):
        if row < 0 or row >= len(self.children):
            return None
        return self.children[row]

    def row(self) -> int:
        if self.parent != None:
            return self.parent.children.index(self)
        return 0


class TreeModuleModel(QAbstractItemModel):

    m_model = PModel()

    m_selected_color = QColor(0, 204, 68)
    m_brush = QBrush()
    m_brush.setColor(QColor(0, 204, 68))

    m_font = QFont('JetBrains Mono')
    m_font.setPixelSize(12)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__load_module()

    def rowCount(self, parent: QModelIndex) -> int:
        if not parent.isValid():
            return len(self.m_model.children)
        else:
            model = parent.internalPointer()
            return len(model.children)

    def columnCount(self, parent: QModelIndex) -> int:
        return 1

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:  # 0, 2
            model = index.internalPointer()
            return model.displayName
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            model = index.internalPointer()
            return model.description
        elif role == Qt.ItemDataRole.StatusTipRole:  # 4
            return None
        elif role == Qt.ItemDataRole.FontRole:  # 6
            return self.m_font
        elif role == Qt.ItemDataRole.TextAlignmentRole:  # 7
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.BackgroundRole:  # 8
            return None
        elif role == Qt.ItemDataRole.ForegroundRole:  # 9
            model = index.internalPointer()
            if model.displayName in PROJECT.modules:
                return self.m_brush
            return None
        elif role == Qt.ItemDataRole.CheckStateRole:  # 10
            return None
        elif role == Qt.ItemDataRole.SizeHintRole:  # 13
            return None
        else:
            print(index, role)
            return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return super().flags(index)

    def index(self, row: int, column: int, parent: QModelIndex) -> QModelIndex:
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        if not parent.isValid():
            parentModel = self.m_model
        else:
            parentModel = parent.internalPointer()

        childModel = parentModel.child(row)
        if childModel != None:
            return self.createIndex(row, column, childModel)
        else:
            return QModelIndex()

    def parent(self, index: QModelIndex) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        childModel = index.internalPointer()
        parentModel = childModel.parent

        if parentModel == self.m_model:
            return QModelIndex()

        return self.createIndex(parentModel.row(), 0, parentModel)

    def __load_module(self):
        locale = SETTINGS.get(SETTINGS.language).value.name()
        for group, module_group in PROJECT.summary.modules.items():
            model = PModel(group, "", [], self.m_model)
            for name, module in module_group.items():
                model_child = PModel(name, module["description"][locale], [], model)
                model.append(model_child)
            self.m_model.append(model)
        self.modelReset.emit()


class TreeModule(Ui_TreeModule, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.treeView_modules.header().hide()

        self.m_treeView_modulesProxyModel = QSortFilterProxyModel(self)
        self.m_model = TreeModuleModel(self)
        self.m_treeView_modulesProxyModel.setSourceModel(self.m_model)
        self.treeView_modules.setModel(self.m_treeView_modulesProxyModel)
        self.treeView_modules.expandAll()
        self.treeView_modules.selectionModel().selectionChanged.connect(self.treeView_modulesSelectionChanged)

    def treeView_modulesSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            if str(index.parent().data()) != "None":
                module = str(index.data())
                ip = PROJECT.ip.ip(module)
                if "modeGrid" in ip:
                    PROJECT.trigger_grid_mode(module, ip["modeGrid"])
