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
# @file        grid_property_ip.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-01     xqyjlj       initial version
#

import attr
from PySide6.QtCore import Qt, QRegularExpression, QModelIndex, QAbstractTableModel, QSortFilterProxyModel, \
    QAbstractItemModel
from PySide6.QtGui import QRegularExpressionValidator, QFont
from PySide6.QtWidgets import (QWidget, QHeaderView, QAbstractItemView, QStyleOptionViewItem, QApplication)
from loguru import logger
from qfluentwidgets import LineEdit, TableItemDelegate, ComboBox

from common import PROJECT, SETTINGS, SIGNAL_BUS, SUMMARY, IP, Style
from .ui.grid_property_ip_ui import Ui_GridPropertyIp


@attr.s
class PModel:
    property = attr.ib(default="", validator=attr.validators.instance_of(str))
    path = attr.ib(default="", validator=attr.validators.instance_of(str))
    value = attr.ib(default="", validator=attr.validators.instance_of(str))
    typeof = attr.ib(default="", validator=attr.validators.instance_of(str))
    possibleValues = attr.ib(default=[], validator=attr.validators.instance_of(list))
    readonly = attr.ib(default="", validator=attr.validators.instance_of(bool))
    description = attr.ib(default="", validator=attr.validators.instance_of(str))


g_data = []


class EditorDelegate(TableItemDelegate):

    def __init__(self, parent=None):
        super().__init__(parent)

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget | None:
        column = index.column()
        row = index.row()
        if column == 0:
            return None

        if g_data[row].typeof == "string":
            lineEdit = LineEdit(parent)
            lineEdit.setProperty("transparent", False)
            lineEdit.setStyle(QApplication.style())
            lineEdit.setText(g_data[row].value)
            lineEdit.setValidator(QRegularExpressionValidator(QRegularExpression("^[A-Za-z_][A-Za-z0-9_]+$")))
            return lineEdit
        elif g_data[row].typeof == "enum":
            comboBox = ComboBox(parent)
            Style.GRID_PROPERTY_IP.apply(comboBox)
            comboBox.setStyle(QApplication.style())
            for value in g_data[index.row()].possibleValues:
                comboBox.addItem(IP.iptr(value))
            comboBox.setCurrentText(IP.iptr(g_data[index.row()].value))
            return comboBox
        else:
            return None

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        column = index.column()
        row = index.row()
        if column == 0:
            return None

        if g_data[row].typeof == "string":
            editor: LineEdit
            model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)
        elif g_data[row].typeof == "enum":
            editor: ComboBox
            model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)


class GridPropertyIpModel(QAbstractTableModel):
    __pinInstance = ""

    __font = QFont('JetBrains Mono')
    __font.setPixelSize(12)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__headers = [self.tr("Property"), self.tr("Value")]
        self.__pinInstance = SUMMARY.projectSummary().pinIp()

        SIGNAL_BUS.gridPropertyIpTriggered.connect(self.changePropertyIp)

    # noinspection PyMethodOverriding
    def rowCount(self, parent: QModelIndex) -> int:
        return len(g_data)

    # noinspection PyMethodOverriding
    def columnCount(self, parent: QModelIndex) -> int:
        return 2

    # noinspection PyMethodOverriding
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:  # 0, 2
            if index.column() == 0:
                return g_data[index.row()].property
            elif index.column() == 1:
                return IP.iptr(g_data[index.row()].value)
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            if index.column() == 1:
                return g_data[index.row()].description
            else:
                return ""
        elif role == Qt.ItemDataRole.StatusTipRole:  # 4
            return None
        elif role == Qt.ItemDataRole.FontRole:  # 6
            return self.__font
        elif role == Qt.ItemDataRole.TextAlignmentRole:  # 7
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
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

    # noinspection PyMethodOverriding
    def setData(self, index: QModelIndex, value: object, role: int) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            if g_data[index.row()].typeof == "string":
                path = g_data[index.row()].path
                PROJECT.project().configs.set(path, value)
            elif g_data[index.row()].typeof == "enum":
                path = g_data[index.row()].path
                PROJECT.project().configs.set(path, IP.iptr2(value))
                g_data[index.row()].value = value
            return True
        else:
            return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        if index.column() == 1:
            if g_data[index.row()].readonly:
                return super().flags(index) & ~Qt.ItemFlag.ItemIsEnabled
            else:
                return super().flags(index) | Qt.ItemFlag.ItemIsEditable
        else:
            return super().flags(index)

    # noinspection PyMethodOverriding
    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole:  # 0
            return self.__headers[section]
        else:
            return None

    def changePropertyIp(self, instance: str, value: str):
        g_data.clear()
        function: str = PROJECT.project().configs.get(f"pin/{value}/function", "")
        if len(function) == 0:
            self.modelReset.emit()
            return

        ip = IP.projectIps().get(instance)
        if ip is None:
            logger.error(f'the ip instance:"{instance}" is invalid.')
            self.modelReset.emit()
            return

        mode = function.split('-')[1]
        mode_cfg = ip.modes[mode]

        if self.__pinInstance == instance:
            g_data.append(
                PModel(property=self.tr("Name"),
                       path="",
                       value=value,
                       typeof="string",
                       possibleValues=[],
                       readonly=True,
                       description=""))
            path = f"pin/{value}/label"
            g_data.append(
                PModel(property=self.tr("Label"),
                       path=path,
                       value=PROJECT.project().configs.get(path, ""),
                       typeof="string",
                       possibleValues=[],
                       readonly=False,
                       description=""))

        if len(ip.parameters) > 0:
            local = SETTINGS.get(SETTINGS.language).value.name()
            for mode, cfg in mode_cfg.items():
                path = f"{instance}/{value}/{mode}"
                g_data.append(
                    PModel(property=ip.parameters[mode].displayName[local],
                           path=path,
                           value=PROJECT.project().configs.get(path, ""),
                           typeof=ip.parameters[mode].type,
                           possibleValues=cfg.values,
                           readonly=False,
                           description=ip.parameters[mode].description[local]))

        self.modelReset.emit()


class GridPropertyIp(Ui_GridPropertyIp, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        proxyModel = QSortFilterProxyModel(self)
        model = GridPropertyIpModel(self)
        proxyModel.setSourceModel(model)
        self.tableView_property.setModel(proxyModel)
        self.tableView_property.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView_property.verticalHeader().setVisible(False)
        self.tableView_property.setBorderVisible(True)
        self.tableView_property.setBorderRadius(8)
        self.tableView_property.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tableView_property.setItemDelegateForColumn(1, EditorDelegate(self.tableView_property))
