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
# @file        package_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-23     xqyjlj       initial version
#

from PySide6.QtCore import Qt, Signal, QItemSelection, QSortFilterProxyModel
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QVBoxLayout
from qfluentwidgets import (TreeView)

from common import Style, Icon, PACKAGE
from .ui.package_view_ui import Ui_PackageView


class VersionInfoWidget(QWidget):
    flushed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainLayout = QVBoxLayout(self)
        self.treeView = TreeView(self)
        self.mainLayout.addWidget(self.treeView)

        self.treeView.header().hide()

        self.proxyModel = QSortFilterProxyModel(self)
        self.model = QStandardItemModel(self)
        self.proxyModel.setSourceModel(self.model)
        self.treeView.setModel(self.proxyModel)
        self.treeView.expandAll()
        # self.treeView.selectionModel().selectionChanged.connect(self.treeView_modulesSelectionChanged)

    def setInfo(self, kind: str, name: str, version: str):
        path = PACKAGE.path(kind, name, version)
        pdsc = PACKAGE.getPackageDescription(path)
        self.model.clear()
        if pdsc is None:
            return


class PackageView(Ui_PackageView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.packageTreeCard.setFixedWidth(300)
        self.packageTree.header().setVisible(False)
        self.packageTree.selectionModel().selectionChanged.connect(self.__on_packageTree_selectionChanged)

        Style.PACKAGE_VIEW.apply(self)

    def __updateTree(self):
        package = PACKAGE.index.origin
        for kind, item in package.items():
            kind_item = QTreeWidgetItem([kind])
            kind_item.setIcon(0, Icon.M_FOLDER_BASE.qicon())
            kind_item.setSelected(False)
            for name, value in item.items():
                name_item = QTreeWidgetItem(kind_item, [name])
                name_item.setIcon(0, Icon.M_FOLDER_DIST.qicon())
                for version, path in value.items():
                    version_item = QTreeWidgetItem(name_item, [version])
                    version_item.setIcon(0, Icon.DATABASE_2.qicon())
                    version_item.setData(0, Qt.ItemDataRole.StatusTipRole, f"{kind}/{name}/{version}")
            kind_item.setExpanded(True)
            self.packageTree.addTopLevelItem(kind_item)

    def __on_packageTree_selectionChanged(self, selected: QItemSelection, _: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            path: str = index.data(Qt.ItemDataRole.StatusTipRole)
            if path is not None:
                print(path.split("/"))

    def flush(self):
        self.__updateTree()
