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
from PySide6.QtWidgets import (
    QWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QHBoxLayout,
    QHeaderView,
)
from qfluentwidgets import (
    TreeWidget,
    RoundMenu,
    Action,
    MessageBox,
    MessageBoxBase,
    IndeterminateProgressRing,
)

from common import Style, Icon, PACKAGE, SETTINGS, SIGNAL_BUS
from utils import Converters
from .ui.package_view_ui import Ui_PackageView


class PackageInfoWidget(QWidget):
    flushed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.main_layout = QVBoxLayout(self)
        self.tree_widget = TreeWidget(self)
        self.tree_widget.header().setSectionResizeMode(
            QHeaderView.ResizeMode.ResizeToContents
        )
        self.tree_widget.header().hide()
        self.tree_widget.setColumnCount(2)
        self.tree_widget.hide()
        self.main_layout.addWidget(self.tree_widget)

        self.tree_widget.itemClicked.connect(self.__on_tree_widget_item_clicked)

    def set_info(self, kind: str, name: str, version: str):
        path = PACKAGE.index().path(kind, name, version)
        pdsc = PACKAGE.get_package_description(path)
        self.tree_widget.clear()
        local = SETTINGS.get(SETTINGS.language).value.name()
        if pdsc is None:
            self.tree_widget.hide()
            return
        self.tree_widget.show()

        # Author ---------------------------------------------------------------
        author_item = QTreeWidgetItem(self.tree_widget, [self.tr("Author")])  # type: ignore
        QTreeWidgetItem(author_item, [self.tr("Name"), pdsc.author.name])  # type: ignore
        QTreeWidgetItem(author_item, [self.tr("Email"), pdsc.author.email])  # type: ignore
        website_item = QTreeWidgetItem(author_item, [self.tr("Website")])  # type: ignore
        QTreeWidgetItem(website_item, [self.tr("Blog"), pdsc.author.website.blog])  # type: ignore
        QTreeWidgetItem(website_item, [self.tr("Github"), pdsc.author.website.github])  # type: ignore
        # ----------------------------------------------------------------------
        QTreeWidgetItem(self.tree_widget, [self.tr("Name"), pdsc.name])  # type: ignore
        QTreeWidgetItem(self.tree_widget, [self.tr("Version"), pdsc.version])  # type: ignore
        QTreeWidgetItem(self.tree_widget, [self.tr("License"), pdsc.license])  # type: ignore
        QTreeWidgetItem(self.tree_widget, [self.tr("Type"), pdsc.type])  # type: ignore
        QTreeWidgetItem(self.tree_widget, [self.tr("Vendor"), pdsc.vendor])  # type: ignore
        QTreeWidgetItem(
            self.tree_widget, [self.tr("Vendor url"), pdsc.vendor_url.get(local)]  # type: ignore
        )
        QTreeWidgetItem(
            self.tree_widget, [self.tr("Description"), pdsc.description.get(local)]  # type: ignore
        )
        QTreeWidgetItem(self.tree_widget, [self.tr("Url"), pdsc.url.get(local)])  # type: ignore
        QTreeWidgetItem(self.tree_widget, [self.tr("Support"), pdsc.support])  # type: ignore
        self.tree_widget.expandAll()

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
        self.tree_widget.clear()
        self.tree_widget.hide()

    def __on_tree_widget_item_clicked(self, item: QTreeWidgetItem, column: int):
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
            self.failed.emit(self.tr("Uninstall failed"))  # type: ignore


class PackageView(Ui_PackageView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__uninstall_args = None

        self.packageTreeCard.setFixedWidth(300)
        self.packageTree.header().setVisible(False)
        self.packageTree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.packageTree.customContextMenuRequested.connect(
            self.__on_packageTree_customContextMenuRequested
        )
        self.packageTree.selectionModel().selectionChanged.connect(
            self.__on_packageTree_selectionChanged
        )

        self.version_menu = RoundMenu(parent=self)
        self.uninstall_action = Action(self.tr("Uninstall"))  # type: ignore
        self.uninstall_action.triggered.connect(self.__on_uninstallAction_triggered)
        self.version_menu.addAction(self.uninstall_action)

        self.package_info_widget = PackageInfoWidget(self)
        self.packageInfoCardVerticalLayout.addWidget(self.package_info_widget)

        self.busy_message_box = MessageBoxBase(self.window())
        ring = IndeterminateProgressRing(self.busy_message_box)
        ring_layout = QHBoxLayout()
        ring_layout.addWidget(ring, 0, Qt.AlignmentFlag.AlignCenter)
        self.busy_message_box.viewLayout.addLayout(ring_layout)
        self.busy_message_box.setMinimumWidth(350)
        self.busy_message_box.buttonGroup.hide()

        SIGNAL_BUS.package_updated.connect(self.flush)
        Style.PACKAGE_VIEW.apply(self)

    def __update_tree(self):
        package = PACKAGE.index().origin
        self.packageTree.clear()
        self.package_info_widget.clear()
        for kind, item in package.items():
            kind_item = QTreeWidgetItem([kind])
            self.packageTree.addTopLevelItem(kind_item)
            kind_item.setIcon(0, Icon.M_FOLDER_BASE.qicon())
            for name, value in item.items():
                name_item = QTreeWidgetItem(kind_item, [name])
                name_item.setIcon(0, Icon.M_FOLDER_DIST.qicon())
                for version, path in value.items():
                    version_item = QTreeWidgetItem(name_item, [version])
                    version_item.setIcon(0, Icon.DATABASE_2.qicon())
                    version_item.setData(
                        0, Qt.ItemDataRole.StatusTipRole, f"{kind}/{name}/{version}"
                    )
        self.packageTree.expandAll()

    def __on_uninstallAction_triggered(self):
        if self.__uninstall_args is None:
            return

        thread = PackageUninstallThread(
            self.__uninstall_args[0],
            self.__uninstall_args[1],
            self.__uninstall_args[2],
            self,
        )
        thread.started.connect(self.__on_uninstallThread_started)
        thread.failed.connect(
            lambda s: MessageBox(self.tr("Error"), s, self.window()).exec()  # type: ignore
        )
        thread.finished.connect(self.__on_uninstallThread_finished)
        thread.start()

    def __on_uninstallThread_started(self):
        self.busy_message_box.exec()

    def __on_uninstallThread_finished(self):
        self.busy_message_box.accept()
        self.flush()

    def __on_packageTree_selectionChanged(
        self, selected: QItemSelection, _: QItemSelection
    ):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            path: str = index.data(Qt.ItemDataRole.StatusTipRole)
            if path is not None:
                args = path.split("/")
                self.package_info_widget.set_info(args[0], args[1], args[2])

    def __on_packageTree_customContextMenuRequested(self, pos: QPoint):
        item = self.packageTree.itemAt(pos)
        if item is None:
            self.__uninstall_args = None
            return
        path: str = item.data(0, Qt.ItemDataRole.StatusTipRole)
        if path is not None:
            args = path.split("/")
            self.__uninstall_args = args
            self.version_menu.exec(
                self.packageTree.viewport().mapToGlobal(pos), ani=True
            )

    def flush(self):
        self.__update_tree()
