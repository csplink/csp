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
# @file        grid_mode_io.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-02     xqyjlj       initial version
#

from PySide6.QtCore import Qt, QSortFilterProxyModel, QAbstractTableModel, QModelIndex, QItemSelection
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QWidget, QAbstractItemView, QHeaderView
from loguru import logger

from common import PROJECT, SETTINGS, SIGNAL_BUS, IP
from .ui.grid_mode_io_ui import Ui_GridModeIo


class GridModeIoModel(QAbstractTableModel):
    __font = QFont('JetBrains Mono')
    __font.setPixelSize(12)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__instance = ""
        self.__ip = {}
        self.__headersMap = {}
        self.__headersList = []
        self.__config = {}
        self.__data = []

        PROJECT.project().configs.configsChanged.connect(self.projectConfigChanged)
        PROJECT.project().configs.pinConfigsChanged.connect(self.pinProjectConfigChanged)

    # noinspection PyMethodOverriding
    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.__data)

    # noinspection PyMethodOverriding
    def columnCount(self, parent: QModelIndex) -> int:
        if len(self.__headersList) > 0:
            return len(self.__headersList)
        else:
            return 0

    # noinspection PyMethodOverriding
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole:  # 0
            return self.__data[index.row()][index.column()]["display"]
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            return self.__data[index.row()][index.column()]["tooltip"]
        elif role == Qt.ItemDataRole.StatusTipRole:  # 4
            return None
        elif role == Qt.ItemDataRole.FontRole:  # 6
            return self.__font
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
            logger.warning(index, role)
            return None

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        return super().flags(index)

    # noinspection PyMethodOverriding
    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole:  # 0
            if orientation == Qt.Orientation.Horizontal:
                return self.__headersList[section]
            else:
                return f"{section + 1}"
        else:
            return None

    def setInstance(self, instance: str):
        if self.__instance != instance:
            self.__instance = instance

            locale = SETTINGS.get(SETTINGS.language).value

            self.__ip = IP.projectIps().get(instance)
            self.__headersMap.clear()

            if self.__ip is None:
                logger.error(f'the ip instance:"{instance}" is invalid.')
                return

            self.__headersMap = {
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
            for key, info in self.__ip.parameters.items():
                self.__headersMap[info.displayName[locale.name()]] = {
                    "path": f"{instance}/(name)/{key}",
                    "index": index
                }
                index += 1
            self.__headersList = list(self.__headersMap.keys())

            self.__config = PROJECT.project().configs.get(instance)
            self.__data.clear()

            if self.__config is not None:
                for name in self.__config.keys():
                    if PROJECT.project().configs.get(f"pin/{name}/locked"):
                        l = []
                        for _, item in self.__headersMap.items():
                            path = item["path"]
                            if path != "":
                                path = path.replace("(name)", name)
                                value = PROJECT.project().configs.get(path, "")
                                l.append({"display": IP.iptr(self.__value2str(value)), "tooltip": value})
                            else:
                                l.append({"display": name, "tooltip": name})
                        self.__data.append(l)

            self.modelReset.emit()

    def __value2str(self, value):
        if isinstance(value, bool):
            return self.tr("Locked") if value else self.tr("Unlocked")
        return value

    def __removeModelData(self, name: str):
        row = 0
        for item in self.__data:
            if item[0]["display"] == name:
                break
            row += 1
        if row < len(self.__data):
            self.beginRemoveRows(QModelIndex(), row, row)
            self.__data.pop(row)
            self.endRemoveRows()

    def __insertModelData(self, row: int, name: str):
        self.beginInsertRows(QModelIndex(), row, row)

        li = [{"display": name, "tooltip": name}]
        for _ in range(len(self.__headersList) - 1):
            li.append({"display": "", "tooltip": ""})
        self.__data.insert(row, li)

        self.endInsertRows()

    def __getModelDataIndex(self, name: str) -> int:
        li = sorted(list(self.__config.keys()))
        if not name in li:
            return -1
        index = li.index(name)
        if index < len(self.__data):
            if self.__data[index][0]["display"] == name:
                exists = True
            else:
                exists = False
        else:
            exists = False

        if not exists:
            self.__insertModelData(index, name)

        return index

    def projectConfigChanged(self, keys: list[str], _: str, newValue: str):
        if keys[0] == self.__instance:
            name = keys[1]

            if len(keys) == 2:
                self.__removeModelData(name)
            elif len(keys) == 3:
                index = self.__getModelDataIndex(name)
                if index >= 0:
                    locale = SETTINGS.get(SETTINGS.language).value
                    param = self.__ip["parameters"][keys[2]]["displayName"][locale.name()]
                    column = self.__headersList.index(param)
                    self.__data[index][column] = {
                        "display": IP.iptr(self.__value2str(newValue)),
                        "tooltip": newValue
                    }
                    index = self.createIndex(index, column)
                    self.dataChanged.emit(index, index)

    def pinProjectConfigChanged(self, keys: list[str], _: str, newValue: str):
        if "" != self.__instance:
            if len(keys) == 3 and keys[2] == "label":
                name = keys[1]
                index = self.__getModelDataIndex(name)
                if index >= 0:
                    self.__data[index][1] = {"display": newValue, "tooltip": newValue}
                    index = self.createIndex(index, 1)
                    self.dataChanged.emit(index, index)


class GridModeIo(Ui_GridModeIo, QWidget):
    __instance = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.m_tableView_ioProxyModel = QSortFilterProxyModel(self)
        self.m_model = GridModeIoModel(self)
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
        if self.__instance != instance:
            self.__instance = instance
            self.m_model.setInstance(instance)

    def tableView_ioSelectionChanged(self, selected: QItemSelection, _: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            name = str(index.data())
            SIGNAL_BUS.gridPropertyIpTriggered.emit(self.__instance, name)
