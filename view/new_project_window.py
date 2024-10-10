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
# @file        new_project_window.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-05     xqyjlj       initial version
#

import os

from PySide6.QtCore import Qt, QSortFilterProxyModel
from PySide6.QtGui import QIcon, QPixmap, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QSizePolicy
from qfluentwidgets import (PushButton, FluentIconBase, MSFluentWindow, TextBrowser,
                            BodyLabel, PixmapLabel, StrongBodyLabel)

from common import SETTINGS, Icon, Style, Repository
from .ui.new_project_view_ui import Ui_NewProjectView


class FeatureView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.Icon = None
        self.mainVLayout = QVBoxLayout(self)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.infoHLayout = QHBoxLayout()

        self.textBrowser = TextBrowser(self)
        self.textBrowser.setObjectName('readmeTextBrowser')
        self.textBrowser.setReadOnly(True)

        # ----------------------------------------------------------------------
        self.urlBtnGroupLayout = QVBoxLayout()
        self.socNameLabel = StrongBodyLabel('SOC Name', self)
        self.vendorNameLabel = StrongBodyLabel('Vendor Name', self)
        self.urlBtnGroupLayout.addWidget(self.socNameLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.urlBtnGroupLayout.addWidget(self.vendorNameLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.infoHLayout.addLayout(self.urlBtnGroupLayout)
        self.infoHLayout.addSpacing(50)

        # ----------------------------------------------------------------------
        self.info1Layout = QVBoxLayout()
        self.packageNameLabel = BodyLabel('Package Name', self)
        self.marketStatusLabel = BodyLabel('Market Name', self)
        self.info1Layout.addWidget(self.packageNameLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.info1Layout.addWidget(self.marketStatusLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.infoHLayout.addLayout(self.info1Layout)
        self.infoHLayout.addSpacing(20)

        # ----------------------------------------------------------------------
        self.packagePixmapLabel = PixmapLabel(self)
        self.infoHLayout.addWidget(self.packagePixmapLabel, 0, Qt.AlignmentFlag.AlignLeft)
        pixmap = QPixmap(r'C:\Users\xqyjl\Documents\git\github\csplink\csp\resource\packages\LQFP48.png')
        pixmap = pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.packagePixmapLabel.setPixmap(pixmap)
        self.infoHLayout.addSpacing(20)

        # ----------------------------------------------------------------------
        self.info2Layout = QVBoxLayout()
        self.info2ChildLayout = QHBoxLayout()
        self.introductionLabel = StrongBodyLabel('Introduction', self)
        self.priceLabel = BodyLabel('Price', self)
        self.versionLabel = BodyLabel('Version', self)
        self.introductionLabel.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        self.info2ChildLayout.addWidget(self.priceLabel)
        self.info2ChildLayout.addWidget(self.versionLabel)
        self.info2Layout.addWidget(self.introductionLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.info2Layout.addLayout(self.info2ChildLayout)
        self.infoHLayout.addLayout(self.info2Layout)

        # ----------------------------------------------------------------------

        self.mainVLayout.addLayout(self.infoHLayout)
        self.mainVLayout.addWidget(self.textBrowser)

        Style.NEW_PROJECT_WINDOW.apply(self.textBrowser)


class NewProjectView(Ui_NewProjectView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__repo = Repository().repository
        self.__typeTreeViewItems = []
        self.__vendorTreeViewItems = []
        self.__seriesTreeViewItems = []
        self.__lineTreeViewItems = []
        self.__coreTreeViewItems = []
        self.__packageTreeViewItems = []

        self.createBtn = PushButton(self.tr('Create'), self)
        self.btnGroupHorizontalLayout.addWidget(self.createBtn, 0, Qt.AlignmentFlag.AlignRight)

        self.treeView.header().setVisible(False)

        self.mainSplitter.setSizes([100, 600])
        self.mainSplitter.setCollapsible(0, False)
        self.mainSplitter.setCollapsible(1, False)
        self.socSplitter.setSizes([200, 100])
        self.socSplitter.setCollapsible(0, False)
        self.socSplitter.setCollapsible(1, False)

        self.tableView.setBorderVisible(True)
        self.tableView.setBorderRadius(8)
        self.tableView.setSortingEnabled(True)

        self.__initTreeViewFilter()

        self.featureView = FeatureView(self)

        self.addSubInterface(self.featureView, Icon.FOLDER, self.tr('Feature'))

        self.tabBar.setCurrentItem(self.featureView.objectName())

    def addSubInterface(self, interface: QWidget, icon: FluentIconBase, text: str):
        self.stackedWidget.addWidget(interface)
        self.tabBar.addItem(routeKey=interface.objectName(),
                            text=text,
                            icon=icon,
                            onClick=lambda: self.stackedWidget.setCurrentWidget(interface))

    def __initTreeViewFilter(self):
        self.__proxyModelTreeView = QSortFilterProxyModel(self)
        self.__modelTreeView = QStandardItemModel(self.treeView)

        self.__typeTreeViewRootItem = QStandardItem(self.tr("Type"))
        self.__vendorTreeViewRootItem = QStandardItem(self.tr("Vendor"))
        self.__seriesTreeViewRootItem = QStandardItem(self.tr("Series"))
        self.__lineTreeViewRootItem = QStandardItem(self.tr("Line"))
        self.__coreTreeViewRootItem = QStandardItem(self.tr("Core"))
        self.__packageTreeViewRootItem = QStandardItem(self.tr("Package"))

        self.__typeTreeViewRootItem.setCheckable(True)
        self.__vendorTreeViewRootItem.setCheckable(True)
        self.__seriesTreeViewRootItem.setCheckable(True)
        self.__lineTreeViewRootItem.setCheckable(True)
        self.__coreTreeViewRootItem.setCheckable(True)
        self.__packageTreeViewRootItem.setCheckable(True)

        self.__typeTreeViewRootItem.setEditable(False)
        self.__vendorTreeViewRootItem.setEditable(False)
        self.__seriesTreeViewRootItem.setEditable(False)
        self.__lineTreeViewRootItem.setEditable(False)
        self.__coreTreeViewRootItem.setEditable(False)
        self.__packageTreeViewRootItem.setEditable(False)

        self.__modelTreeView.appendRow(self.__typeTreeViewRootItem)
        self.__modelTreeView.appendRow(self.__vendorTreeViewRootItem)
        self.__modelTreeView.appendRow(self.__seriesTreeViewRootItem)
        self.__modelTreeView.appendRow(self.__lineTreeViewRootItem)
        self.__modelTreeView.appendRow(self.__coreTreeViewRootItem)
        self.__modelTreeView.appendRow(self.__packageTreeViewRootItem)

        for kind in self.__repo.allTypes:
            item = QStandardItem(kind)
            item.setCheckable(True)
            item.setEditable(False)
            self.__typeTreeViewItems.append(item)
        self.__typeTreeViewRootItem.appendRows(self.__typeTreeViewItems)

        for vendor in self.__repo.allVendors:
            item = QStandardItem(vendor)
            item.setCheckable(True)
            item.setEditable(False)
            self.__vendorTreeViewItems.append(item)
        self.__vendorTreeViewRootItem.appendRows(self.__vendorTreeViewItems)

        for series in self.__repo.allSeries:
            item = QStandardItem(series)
            item.setCheckable(True)
            item.setEditable(False)
            self.__seriesTreeViewItems.append(item)
        self.__seriesTreeViewRootItem.appendRows(self.__seriesTreeViewItems)

        for line in self.__repo.allLines:
            item = QStandardItem(line)
            item.setCheckable(True)
            item.setEditable(False)
            self.__lineTreeViewItems.append(item)
        self.__lineTreeViewRootItem.appendRows(self.__lineTreeViewItems)

        for core in self.__repo.allCores:
            item = QStandardItem(core)
            item.setCheckable(True)
            item.setEditable(False)
            self.__coreTreeViewItems.append(item)
        self.__coreTreeViewRootItem.appendRows(self.__coreTreeViewItems)

        for package in self.__repo.allPackage:
            item = QStandardItem(package)
            item.setCheckable(True)
            item.setEditable(False)
            self.__packageTreeViewItems.append(item)
        self.__packageTreeViewRootItem.appendRows(self.__packageTreeViewItems)

        self.__proxyModelTreeView.setSourceModel(self.__modelTreeView)
        self.treeView.setModel(self.__proxyModelTreeView)
        self.treeView.expandAll()

        self.__modelTreeView.itemChanged.connect(self.__on_modelTreeView_itemChanged)

    def __on_modelTreeView_itemChanged(self, item: QStandardItem):
        if item is None:
            return

        rowCount = item.rowCount()
        if rowCount > 0:  # root item
            for i in range(rowCount):
                child = item.child(i)
                if child is None:
                    continue
                if item.checkState() == Qt.CheckState.Checked:
                    child.setCheckState(Qt.CheckState.Checked)
                elif item.checkState() == Qt.CheckState.Unchecked:
                    child.setCheckState(Qt.CheckState.Unchecked)
        else:  # root item's child
            parent = item.parent()
            count = parent.rowCount()
            checkedCount = 0
            for i in range(count):
                child = parent.child(i)
                if child is None:
                    continue
                if child.checkState() == Qt.CheckState.Checked:
                    checkedCount += 1

            if checkedCount == count:
                parent.setCheckState(Qt.CheckState.Checked)
            elif checkedCount == 0:
                parent.setCheckState(Qt.CheckState.Unchecked)
            else:
                parent.setCheckState(Qt.CheckState.PartiallyChecked)


class NewProjectWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.navigationInterface.hide()
        self.stackedWidget.hide()

        self.view = NewProjectView()
        self.hBoxLayout.addWidget(self.view)

        self.__initWindow()
        self.showMaximized()

    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(QIcon(os.path.join(SETTINGS.EXE_FOLDER, "resource", "images", "logo.svg")))
        self.setWindowTitle('CSPLink')

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)
