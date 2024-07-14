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

from PyQt5.QtCore import Qt, QRegExp, QModelIndex, QAbstractTableModel, QSortFilterProxyModel, QAbstractItemModel
from PyQt5.QtGui import QRegExpValidator, QFont
from PyQt5.QtWidgets import (QWidget, QHeaderView, QTableWidgetItem, QAbstractItemView, QStyleOptionViewItem,
                             QApplication)

from qfluentwidgets import LineEdit, TableItemDelegate, ComboBox

from .ui.Ui_grid_property_ip import Ui_GridPropertyIp
from common import PROJECT, SETTINGS


@attr.s
class PModel():
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

    def createEditor(self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex) -> QWidget:
        column = index.column()
        row = index.row()
        if column == 0:
            return None

        if g_data[row].typeof == "string":
            lineEdit = LineEdit(parent)
            lineEdit.setProperty("transparent", False)
            lineEdit.setStyle(QApplication.style())
            lineEdit.setText(g_data[row].value)
            lineEdit.setValidator(QRegExpValidator(QRegExp("^[A-Za-z_][A-Za-z0-9_]+$")))
            return lineEdit
        elif g_data[row].typeof == "enum":
            comboBox = ComboBox(parent)
            comboBox.setStyleSheet("""
ComboBox {
    border: 1px solid rgba(255, 255, 255, 0.053);
    border-radius: 5px;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding: 5px 31px 6px 11px;
    /* font: 14px 'Segoe UI', 'Microsoft YaHei', 'PingFang SC'; */
    color: white;
    background-color: rgba(30, 30, 30, 1);
    text-align: left;
    outline: none;
}

ComboBox:hover {
    background-color: rgba(30, 30, 30, 1);
}

ComboBox:pressed {
    background-color: rgba(30, 30, 30, 1);
    border-top: 1px solid rgba(255, 255, 255, 0.053);
    color: rgba(255, 255, 255, 0.63);
}

ComboBox:disabled {
    color: rgba(255, 255, 255, 0.3628);
    background-color: rgba(30, 30, 30, 1);
    border: 1px solid rgba(255, 255, 255, 0.053);
    border-top: 1px solid rgba(255, 255, 255, 0.053);
}

ComboBox[isPlaceholderText=true] {
    color: rgba(255, 255, 255, 0.6063);
}""")
            comboBox.setStyle(QApplication.style())
            for value in g_data[index.row()].possibleValues:
                comboBox.addItem(PROJECT.ip.ipTr(value))
            comboBox.setCurrentText(PROJECT.ip.ipTr(g_data[index.row()].value))
            return comboBox
        else:
            return None

    def setModelData(self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex):
        column = index.column()
        row = index.row()
        if column == 0:
            return None

        if g_data[row].typeof == "string":
            model.setData(index, editor.text(), Qt.ItemDataRole.EditRole)
        elif g_data[row].typeof == "enum":
            model.setData(index, editor.currentText(), Qt.ItemDataRole.EditRole)


class GridPropertyIpModel(QAbstractTableModel):

    m_pin_instance = ""

    m_font = QFont('JetBrains Mono')
    m_font.setPixelSize(12)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.m_headers = [self.tr("property"), self.tr("value")]
        self.m_pin_instance = PROJECT.summary.pinIp

        PROJECT.gridPropertyIpTriggered.connect(self.projectGridPropertyIpTriggered)

    def rowCount(self, parent: QModelIndex) -> int:
        return len(g_data)

    def columnCount(self, parent: QModelIndex) -> int:
        return 2

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole:  # 0, 2
            if index.column() == 0:
                return g_data[index.row()].property
            elif index.column() == 1:
                return PROJECT.ip.ipTr(g_data[index.row()].value)
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
            return self.m_font
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
            print(index, role)
            return None

    def setData(self, index: QModelIndex, value: object, role: int) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            if g_data[index.row()].typeof == "string":
                path = g_data[index.row()].path
                PROJECT.setConfig(path, value)
            elif g_data[index.row()].typeof == "enum":
                path = g_data[index.row()].path
                PROJECT.setConfig(path, PROJECT.ip.ipTrR(value))
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

    def headerData(self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole) -> object:
        if role == Qt.ItemDataRole.DisplayRole:  # 0
            return self.m_headers[section]
        else:
            return None

    def projectGridPropertyIpTriggered(self, instance: str, value: str):
        g_data.clear()
        signal = PROJECT.config(f"pin/{value}/signal", "")
        if signal == "":
            self.modelReset.emit()
            return

        cfg = PROJECT.summary.pins[value]["signals"][signal]
        ip = PROJECT.ip.ip(instance)
        if len(ip) == 0:
            self.modelReset.emit()
            return

        if "mode" in cfg:
            mode = cfg["mode"]
            mode_cfg = ip["modes"][mode]

            if self.m_pin_instance == instance:
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
                           value=PROJECT.config(path, ""),
                           typeof="string",
                           possibleValues=[],
                           readonly=False,
                           description=""))

            ip = PROJECT.ip.ip(instance)
            if "parameters" in ip:
                parameters = PROJECT.ip.ip(instance)["parameters"]
                local = SETTINGS.get(SETTINGS.language).value.name()
                for mode, cfg in mode_cfg.items():
                    path = f"{instance}/{value}/{mode}"
                    g_data.append(
                        PModel(property=parameters[mode]["displayName"][local],
                               path=path,
                               value=PROJECT.config(path, ""),
                               typeof=parameters[mode]["type"],
                               possibleValues=cfg["values"],
                               readonly=False,
                               description=parameters[mode]["description"][local]))

        self.modelReset.emit()


class GridPropertyIp(Ui_GridPropertyIp, QWidget):

    m_pin_instance = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.m_tableView_propertyProxyModel = QSortFilterProxyModel(self)
        self.m_model = GridPropertyIpModel(self)
        self.m_tableView_propertyProxyModel.setSourceModel(self.m_model)
        self.tableView_property.setModel(self.m_tableView_propertyProxyModel)
        self.tableView_property.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.tableView_property.verticalHeader().setVisible(False)
        self.tableView_property.setBorderVisible(True)
        self.tableView_property.setBorderRadius(8)
        self.tableView_property.setMinimumWidth(200)
        self.tableView_property.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.tableView_property.setItemDelegateForColumn(1, EditorDelegate(self.tableView_property))
