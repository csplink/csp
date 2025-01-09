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

from PySide6.QtCore import Qt, Signal, QItemSelection, QUrl, QPoint, QThread, QObject
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QTreeWidgetItem, QVBoxLayout, QHBoxLayout, QHeaderView
from qfluentwidgets import (TreeWidget, RoundMenu, Action, MessageBox, MessageBoxBase, IndeterminateProgressRing)

from common import Style, Icon, PACKAGE, SETTINGS, SIGNAL_BUS
from utils import Converters
from .ui.package_view_ui import Ui_PackageView


class PackageInfoWidget(QWidget):
    flushed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainLayout = QVBoxLayout(self)
        self.treeWidget = TreeWidget(self)
        self.treeWidget.header().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.treeWidget.header().hide()
        self.treeWidget.setColumnCount(2)
        self.treeWidget.hide()
        self.mainLayout.addWidget(self.treeWidget)

        self.treeWidget.itemClicked.connect(self.__on_treeWidget_itemClicked)

    def setInfo(self, kind: str, name: str, version: str):
        path = PACKAGE.index().path(kind, name, version)
        pdsc = PACKAGE.getPackageDescription(path)
        self.treeWidget.clear()
        local = SETTINGS.get(SETTINGS.language).value.name()
        if pdsc is None:
            self.treeWidget.hide()
            return
        self.treeWidget.show()

        # Author ---------------------------------------------------------------
        authorItem = QTreeWidgetItem(self.treeWidget, [self.tr('Author')])
        QTreeWidgetItem(authorItem, [self.tr('Name'), pdsc.author.name])
        QTreeWidgetItem(authorItem, [self.tr('Email'), pdsc.author.email])
        websiteItem = QTreeWidgetItem(authorItem, [self.tr('Website')])
        QTreeWidgetItem(websiteItem, [self.tr('Blog'), pdsc.author.website.blog])
        QTreeWidgetItem(websiteItem, [self.tr('Github'), pdsc.author.website.github])
        # ----------------------------------------------------------------------
        QTreeWidgetItem(self.treeWidget, [self.tr('Name'), pdsc.name])
        QTreeWidgetItem(self.treeWidget, [self.tr('Version'), pdsc.version])
        QTreeWidgetItem(self.treeWidget, [self.tr('License'), pdsc.license])
        QTreeWidgetItem(self.treeWidget, [self.tr('Type'), pdsc.type])
        QTreeWidgetItem(self.treeWidget, [self.tr('Vendor'), pdsc.vendor])
        QTreeWidgetItem(self.treeWidget, [self.tr('Vendor url'), pdsc.vendorUrl.get(local)])
        QTreeWidgetItem(self.treeWidget, [self.tr('Description'), pdsc.description.get(local)])
        QTreeWidgetItem(self.treeWidget, [self.tr('Url'), pdsc.url.get(local)])
        QTreeWidgetItem(self.treeWidget, [self.tr('Support'), pdsc.support])
        self.treeWidget.expandAll()

        # def setItems(tree: TreeWidget, parent=None):
        #     if parent is None:
        #         parent = tree.invisibleRootItem()
        #
        #     for i in range(parent.childCount()):
        #         child = parent.child(i)
        #         print(child.data(0, Qt.ItemDataRole.DisplayRole), child.data(1, Qt.ItemDataRole.DisplayRole))
        #         setItems(tree, child)
        #
        # setItems(self.treeWidget)

    def clear(self):
        self.treeWidget.clear()
        self.treeWidget.hide()

    def __on_treeWidget_itemClicked(self, item: QTreeWidgetItem, column: int):
        data: str = item.data(column, Qt.ItemDataRole.DisplayRole)
        if data is not None:
            if Converters.isurl(data):
                QDesktopServices.openUrl(QUrl(data))


class PackageUninstallThread(QThread):
    failed = Signal(str)

    def __init__(self, kind: str, name: str, version: str, parent: QObject):
        super().__init__(parent=parent)
        self.kind = kind
        self.name = name
        self.version = version

    def run(self):
        status = PACKAGE.uninstall(self.kind, self.name, self.version)
        if not status:
            self.failed.emit(self.tr('Uninstall failed'))


class PackageView(Ui_PackageView, QWidget):
    __uninstallArgs = None

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.packageTreeCard.setFixedWidth(300)
        self.packageTree.header().setVisible(False)
        self.packageTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.packageTree.customContextMenuRequested.connect(self.__on_packageTree_customContextMenuRequested)
        self.packageTree.selectionModel().selectionChanged.connect(self.__on_packageTree_selectionChanged)

        self.versionMenu = RoundMenu(parent=self)
        self.uninstallAction = Action(self.tr('Uninstall'))
        self.uninstallAction.triggered.connect(self.__on_uninstallAction_triggered)
        self.versionMenu.addAction(self.uninstallAction)

        self.packageInfoWidget = PackageInfoWidget(self)
        self.packageInfoCardVerticalLayout.addWidget(self.packageInfoWidget)

        self.busyMessageBox = MessageBoxBase(self.window())
        ring = IndeterminateProgressRing(self.busyMessageBox)
        ringLayout = QHBoxLayout()
        ringLayout.addWidget(ring, 0, Qt.AlignmentFlag.AlignCenter)
        self.busyMessageBox.viewLayout.addLayout(ringLayout)
        self.busyMessageBox.setMinimumWidth(350)
        self.busyMessageBox.buttonGroup.hide()

        SIGNAL_BUS.packageUpdated.connect(self.flush)
        Style.PACKAGE_VIEW.apply(self)

    def __updateTree(self):
        package = PACKAGE.index().origin
        self.packageTree.clear()
        self.packageInfoWidget.clear()
        for kind, item in package.items():
            kindItem = QTreeWidgetItem([kind])
            self.packageTree.addTopLevelItem(kindItem)
            kindItem.setIcon(0, Icon.M_FOLDER_BASE.qicon())
            for name, value in item.items():
                nameItem = QTreeWidgetItem(kindItem, [name])
                nameItem.setIcon(0, Icon.M_FOLDER_DIST.qicon())
                for version, path in value.items():
                    versionItem = QTreeWidgetItem(nameItem, [version])
                    versionItem.setIcon(0, Icon.DATABASE_2.qicon())
                    versionItem.setData(0, Qt.ItemDataRole.StatusTipRole, f"{kind}/{name}/{version}")
        self.packageTree.expandAll()

    def __on_uninstallAction_triggered(self):
        if self.__uninstallArgs is None:
            return

        thread = PackageUninstallThread(self.__uninstallArgs[0], self.__uninstallArgs[1], self.__uninstallArgs[2], self)
        thread.started.connect(self.__on_uninstallThread_started)
        thread.failed.connect(lambda s: MessageBox(self.tr("Error"), s, self.window()).exec())
        thread.finished.connect(self.__on_uninstallThread_finished)
        thread.start()

    def __on_uninstallThread_started(self):
        self.busyMessageBox.exec()

    def __on_uninstallThread_finished(self):
        self.busyMessageBox.accept()
        self.flush()

    def __on_packageTree_selectionChanged(self, selected: QItemSelection, _: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            path: str = index.data(Qt.ItemDataRole.StatusTipRole)
            if path is not None:
                args = path.split("/")
                self.packageInfoWidget.setInfo(args[0], args[1], args[2])

    def __on_packageTree_customContextMenuRequested(self, pos: QPoint):
        item = self.packageTree.itemAt(pos)
        if item is None:
            self.__uninstallArgs = None
            return
        path: str = item.data(0, Qt.ItemDataRole.StatusTipRole)
        if path is not None:
            args = path.split("/")
            self.__uninstallArgs = args
            self.versionMenu.exec(self.packageTree.viewport().mapToGlobal(pos), ani=True)

    def flush(self):
        self.__updateTree()
