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

from PyQt5.QtCore import Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget

from .ui.Ui_mode_grid_io import Ui_ModeGridIo
from common import PROJECT, SETTINGS


class ModeGridIo(Ui_ModeGridIo, QWidget):
    m_instance = ""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.lineEdit_search.setVisible(False)
        self.m_tableView_ioProxyModel = QSortFilterProxyModel(self)
        self.m_model = QStandardItemModel(self)
        self.m_tableView_ioProxyModel.setSourceModel(self.m_model)
        self.tableView_io.verticalHeader().hide()
        self.tableView_io.setModel(self.m_tableView_ioProxyModel)
        self.tableView_io.setBorderVisible(True)
        self.tableView_io.setBorderRadius(8)

    def setInstance(self, instance: str):
        if self.m_instance != instance:
            self.m_instance = instance
            ip = PROJECT.ip(instance)
            headers = {
                self.tr("Name"): "",
                self.tr("Label"): "pin/(name)/label",
                self.tr("Locked"): "pin/(name)/locked"
            }

            locale = SETTINGS.get(SETTINGS.language).value
            self.m_model.clear()
            for key, info in ip["parameters"].items():
                headers[info["displayName"][locale.name()]] = f"{instance}/(name)/{key}"
            self.m_model.setHorizontalHeaderLabels(headers.keys())

            pins = PROJECT.config("pin")
            for name, pin in pins.items():
                if pin["signal"] != "":
                    items = []
                    items.append(QStandardItem(name))
                    for _, path in headers.items():
                        if path != "":
                            path = path.replace("(name)", name)
                            items.append((QStandardItem(PROJECT.ipTr(self.value2str(PROJECT.config(path, ""))))))
                    for item in items:
                        item.setEditable(False)
                    self.m_model.appendRow(items)
            self.tableView_io.resizeColumnsToContents()

    def value2str(self, value):
        if isinstance(value, bool):
            return self.tr("Locked") if value else self.tr("Unlocked")
        return value

    def projectConfigChanged(self, key: list[str], oldValue: str, newvalue: str):
        if key[0] == self.m_instance:
            print(key[0])
