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
# @file        mode_grid_io.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-02     xqyjlj       initial version
#

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QModelIndex, QItemSelection
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QFont
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QHeaderView

from .ui.Ui_mode_grid_io import Ui_ModeGridIo
from common import PROJECT, SETTINGS


class ModeGridIoModel(QAbstractTableModel):

    m_instance = ""
    m_ip = {}
    m_headers_map = {}
    m_headers_list = []
    m_config = {}
    m_data = []

    def __init__(self, parent=None):
        super().__init__(parent)

        PROJECT.configChanged.connect(self.projectConfigChanged)
        PROJECT.pinConfigChanged.connect(self.pinProjectConfigChanged)

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.m_data)

    def columnCount(self, parent: QModelIndex) -> int:
        if len(self.m_headers_list) > 0:
            return len(self.m_headers_list)
        else:
            return 0

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole:  # 0
            return self.m_data[index.row()][index.column()]["display"]
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            return self.m_data[index.row()][index.column()]["tooltip"]
        elif role == Qt.ItemDataRole.StatusTipRole:  # 4
            return None
        elif role == Qt.ItemDataRole.FontRole:  # 6
            font = QFont('JetBrains Mono')
            font.setPixelSize(12)
            return font
        elif role == Qt.ItemDataRole.TextAlignmentRole:  # 7
            return Qt.AlignmentFlag.AlignCenter
        elif role == Qt.ItemDataRole.BackgroundRole:  # 8
            return None
        elif role == Qt.ItemDataRole.ForegroundRole:  # 9
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

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole:  # 0
            if orientation == Qt.Orientation.Horizontal:
                return self.m_headers_list[section]
            else:
                return f"{section + 1}"
        elif role == Qt.ItemDataRole.FontRole:  # 6
            font = QFont('JetBrains Mono')
            font.setPixelSize(12)
            return font
        else:
            return None

    def setInstance(self, instance: str):
        if self.m_instance != instance:
            self.m_instance = instance

            locale = SETTINGS.get(SETTINGS.language).value

            self.m_ip = PROJECT.ip(instance)
            self.m_headers_map.clear()

            self.m_headers_map = {
                self.tr("Name"): {
                    "path": "",
                    "index": 0
                },
                self.tr("Label"): {
                    "path": "pin/(name)/label",
                    "index": 1
                },
            }

            index = 2
            for key, info in self.m_ip["parameters"].items():
                self.m_headers_map[info["displayName"][locale.name()]] = {
                    "path": f"{instance}/(name)/{key}",
                    "index": index
                }
                index += 1
            self.m_headers_list = list(self.m_headers_map.keys())

            self.m_config = PROJECT.config(instance)
            self.m_data.clear()

            if self.m_config != None:
                for name in self.m_config.keys():
                    if PROJECT.config(f"pin/{name}/locked"):
                        l = []
                        for _, item in self.m_headers_map.items():
                            path = item["path"]
                            if path != "":
                                path = path.replace("(name)", name)
                                value = PROJECT.config(path, "")
                                l.append({"display": PROJECT.ipTr(self._value2str(value)), "tooltip": value})
                            else:
                                l.append({"display": name, "tooltip": name})
                        self.m_data.append(l)

            self.modelReset.emit()

    def _value2str(self, value):
        if isinstance(value, bool):
            return self.tr("Locked") if value else self.tr("Unlocked")
        return value

    def _removeModelData(self, name: str):
        row = 0
        for item in self.m_data:
            if item[0]["display"] == name:
                break
            row += 1
        if row < len(self.m_data):
            self.beginRemoveRows(QModelIndex(), row, row)
            self.m_data.pop(row)
            self.endRemoveRows()

    def _insertModelData(self, row: int, name: str):
        self.beginInsertRows(QModelIndex(), row, row)

        li = [{"display": name, "tooltip": name}]
        for _ in range(len(self.m_headers_list) - 1):
            li.append({"display": "", "tooltip": ""})
        self.m_data.insert(row, li)

        self.endInsertRows()

    def _getModelDataIndex(self, name: str) -> int:
        li = sorted(list(self.m_config.keys()))
        if not name in li:
            return -1
        index = li.index(name)
        if index < len(self.m_data):
            if self.m_data[index][0]["display"] == name:
                exists = True
            else:
                exists = False
        else:
            exists = False

        if not exists:
            self._insertModelData(index, name)

        return index

    def projectConfigChanged(self, keys: list[str], oldValue: str, newvalue: str):
        if keys[0] == self.m_instance:
            name = keys[1]

            if len(keys) == 2:
                self._removeModelData(name)
            elif len(keys) == 3:
                index = self._getModelDataIndex(name)
                if index >= 0:
                    locale = SETTINGS.get(SETTINGS.language).value
                    param = self.m_ip["parameters"][keys[2]]["displayName"][locale.name()]
                    column = self.m_headers_list.index(param)
                    self.m_data[index][column] = {
                        "display": PROJECT.ipTr(self._value2str(newvalue)),
                        "tooltip": newvalue
                    }
                    index = self.createIndex(index, column)
                    self.dataChanged.emit(index, index)

    def pinProjectConfigChanged(self, keys: list[str], oldValue: str, newvalue: str):
        if "" != self.m_instance:
            if len(keys) == 3 and keys[2] == "label":
                name = keys[1]
                index = self._getModelDataIndex(name)
                if index >= 0:
                    self.m_data[index][1] = {"display": newvalue, "tooltip": newvalue}
                    index = self.createIndex(index, 1)
                    self.dataChanged.emit(index, index)


class ModeGridIo(Ui_ModeGridIo, QWidget):
    m_instance = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.lineEdit_search.setVisible(False)
        self.m_tableView_ioProxyModel = QSortFilterProxyModel(self)
        self.m_model = ModeGridIoModel(self)
        self.m_tableView_ioProxyModel.setSourceModel(self.m_model)
        self.tableView_io.setModel(self.m_tableView_ioProxyModel)
        self.tableView_io.setBorderVisible(True)
        self.tableView_io.setBorderRadius(8)
        self.tableView_io.setSortingEnabled(True)
        self.tableView_io.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.tableView_io.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView_io.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tableView_io.selectionModel().selectionChanged.connect(self.tableView_ioSelectionChanged)

    def setInstance(self, instance: str):
        if self.m_instance != instance:
            self.m_instance = instance
            self.m_model.setInstance(instance)

    def tableView_ioSelectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            name = str(index.data())
            PROJECT.triggerPropertyGridIp(self.m_instance, name)
