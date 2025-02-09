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

from PySide6.QtCore import (
    Qt,
    QSortFilterProxyModel,
    QObject,
    QEvent,
    QUrl,
    QItemSelection,
    Signal,
)
from PySide6.QtGui import (
    QIcon,
    QStandardItem,
    QStandardItemModel,
    QDesktopServices,
    QPixmap,
)
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QSizePolicy,
    QAbstractItemView,
    QHeaderView,
    QFileDialog,
)
from qfluentwidgets import (
    PushButton,
    FluentIconBase,
    MSFluentWindow,
    TextBrowser,
    BodyLabel,
    PixmapLabel,
    StrongBodyLabel,
    MessageBoxBase,
    SubtitleLabel,
    LineEdit,
    ToolButton,
    MessageBox,
)

from common import SETTINGS, Icon, Style, Repository, SUMMARY, PROJECT
from .main_window import MainWindow
from .ui.new_project_view_ui import Ui_NewProjectView


class NewMessageBox(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr("Create a new project"), self)
        # ----------------------------------------------------------------------
        self.nameLineEdit = LineEdit(self)
        self.nameLineEdit.setPlaceholderText(self.tr("Project Name"))
        self.nameLineEdit.setClearButtonEnabled(True)
        self.nameLineEdit.textChanged.connect(self.__on_xLineEdit_textChanged)
        # ----------------------------------------------------------------------
        self.pathLayout = QHBoxLayout()

        self.pathLineEdit = LineEdit(self)
        self.pathLineEdit.setReadOnly(True)
        self.pathLineEdit.setPlaceholderText(self.tr("Project Path"))
        self.pathLineEdit.setClearButtonEnabled(True)
        self.pathLineEdit.textChanged.connect(self.__on_xLineEdit_textChanged)

        self.folderBtn = ToolButton()
        self.folderBtn.pressed.connect(self.__on_folderBtn_pressed)
        self.folderBtn.setIcon(Icon.FOLDER)

        self.pathLayout.addWidget(self.pathLineEdit)
        self.pathLayout.addWidget(self.folderBtn)
        # ----------------------------------------------------------------------
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.nameLineEdit)
        self.viewLayout.addLayout(self.pathLayout)
        # ----------------------------------------------------------------------
        self.yesButton.setText(self.tr("OK"))
        self.yesButton.setEnabled(False)
        self.yesButton.clicked.disconnect()  # self._MessageBoxBase__onYesButtonClicked
        self.yesButton.clicked.connect(self.__on_yesButton_clicked)
        self.cancelButton.setText(self.tr("Cancel"))

        self.widget.setFixedWidth(560)

    # noinspection PyUnusedLocal
    def __on_xLineEdit_textChanged(self, text: str):
        if (
            os.path.isdir(self.pathLineEdit.text())
            and len(self.nameLineEdit.text()) > 0
        ):
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)

    def __on_folderBtn_pressed(self):
        path = QFileDialog.getExistingDirectory(
            self, self.tr("Choose project path"), SETTINGS.lastNewProjectFolder.value
        )
        if os.path.isdir(path):
            SETTINGS.set(SETTINGS.lastNewProjectFolder, path)
            self.pathLineEdit.setText(path)

    def __on_yesButton_clicked(self):
        path = os.path.join(self.pathLineEdit.text(), self.nameLineEdit.text())
        if os.path.isdir(path):
            title = self.tr("Warning")
            content = self.tr(
                "The path {!r} already exists. Do you still want to create a project in this path?"
            ).format(path)
            message = MessageBox(title, content, self.window())
            message.setContentCopyable(True)
            message.raise_()
            if message.exec():
                self.accept()
        else:
            self.accept()


class SocFeatureView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.Icon = None
        self.mainVLayout = QVBoxLayout(self)
        self.mainVLayout.setContentsMargins(0, 0, 0, 0)
        self.infoHLayout = QHBoxLayout()

        self.textBrowser = TextBrowser(self)
        self.textBrowser.setObjectName("readmeTextBrowser")
        self.textBrowser.setReadOnly(True)

        # ----------------------------------------------------------------------
        self.urlBtnGroupLayout = QVBoxLayout()
        self.socNameLabel = StrongBodyLabel("SOC Name", self)
        self.socNameLabel.destroyed.connect(self.__destroyed)
        self.vendorNameLabel = StrongBodyLabel("Vendor Name", self)
        self.socNameLabel.installEventFilter(self)
        self.vendorNameLabel.installEventFilter(self)
        self.socNameLabel.setFixedSize(200, 19)
        self.vendorNameLabel.setFixedSize(200, 19)
        self.urlBtnGroupLayout.addWidget(
            self.socNameLabel, 0, Qt.AlignmentFlag.AlignTop
        )
        self.urlBtnGroupLayout.addWidget(
            self.vendorNameLabel, 0, Qt.AlignmentFlag.AlignTop
        )
        self.infoHLayout.addLayout(self.urlBtnGroupLayout)
        self.infoHLayout.addSpacing(50)

        # ----------------------------------------------------------------------
        self.info1Layout = QVBoxLayout()
        self.packageNameLabel = BodyLabel("Package Name", self)
        self.marketStatusLabel = BodyLabel("Market Name", self)
        self.packageNameLabel.setFixedSize(100, 19)
        self.marketStatusLabel.setFixedSize(100, 19)
        self.info1Layout.addWidget(self.packageNameLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.info1Layout.addWidget(self.marketStatusLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.infoHLayout.addLayout(self.info1Layout)
        self.infoHLayout.addSpacing(20)

        # ----------------------------------------------------------------------
        self.packagePixmapLabel = PixmapLabel(self)
        self.packagePixmapLabel.setFixedSize(80, 80)
        self.infoHLayout.addWidget(
            self.packagePixmapLabel, 0, Qt.AlignmentFlag.AlignLeft
        )
        self.infoHLayout.addSpacing(20)

        # ----------------------------------------------------------------------
        self.info2Layout = QVBoxLayout()
        self.info2ChildLayout = QHBoxLayout()
        self.introductionLabel = StrongBodyLabel("Introduction", self)
        self.priceLabel = BodyLabel("Price", self)
        self.introductionLabel.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.info2ChildLayout.addWidget(self.priceLabel)
        self.info2Layout.addWidget(self.introductionLabel, 0, Qt.AlignmentFlag.AlignTop)
        self.info2Layout.addLayout(self.info2ChildLayout)
        self.infoHLayout.addLayout(self.info2Layout)

        # ----------------------------------------------------------------------

        self.mainVLayout.addLayout(self.infoHLayout)
        self.mainVLayout.addWidget(self.textBrowser)

        Style.NEW_PROJECT_WINDOW.apply(self.textBrowser)

    def __destroyed(self):
        print("destroyed")

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, StrongBodyLabel):
            if event.type() == QEvent.Type.MouseButtonRelease:
                url = watched.property("url")
                if url is not None and url != "":
                    QDesktopServices.openUrl(QUrl(url))
        return super().eventFilter(watched, event)

    def setInfo(self, vendor: str, name: str):
        summary = SUMMARY.getSummary(vendor, name)
        locale = SETTINGS.get(SETTINGS.language).value.name()
        self.socNameLabel.setText(name)
        self.vendorNameLabel.setText(vendor)
        self.packageNameLabel.setText(summary.package)
        self.marketStatusLabel.setText("")
        self.introductionLabel.setText(summary.introduction.get(locale))
        self.textBrowser.setMarkdown(summary.illustrate.get(locale))
        self.priceLabel.setText("")
        packagePath = f"{SETTINGS.PACKAGES_IMAGE_FOLDER}/{summary.package.upper()}.png"
        if os.path.exists(packagePath):
            pixmap = QPixmap(packagePath)
        else:
            pixmap = QPixmap(f"{SETTINGS.PACKAGES_IMAGE_FOLDER}/unknown.png")
        pixmap = pixmap.scaled(
            80,
            80,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.packagePixmapLabel.setPixmap(pixmap)
        self.show()


class NewProjectView(Ui_NewProjectView, QWidget):
    created = Signal(str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__repo = Repository().repository()
        self.__targetChip = ""
        self.__vendor = ""

        self.createBtn = PushButton(self.tr("Create"), self)
        self.createBtn.setEnabled(False)
        self.btnGroupHorizontalLayout.addWidget(
            self.createBtn, 0, Qt.AlignmentFlag.AlignRight
        )

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

        self.__initTreeView()
        self.__initTableView()

        self.socFeatureView = SocFeatureView(self)

        self.addSubInterface(self.socFeatureView, Icon.FOLDER, self.tr("Feature"))

        self.tabBar.setCurrentItem(self.socFeatureView.objectName())
        self.socFeatureView.hide()

        self.createBtn.clicked.connect(self.__on_createBtn_clicked)

    def addSubInterface(self, interface: QWidget, icon: FluentIconBase, text: str):
        self.stackedWidget.addWidget(interface)
        self.tabBar.addItem(
            routeKey=interface.objectName(),
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(interface),
        )

    def __initTreeView(self):
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

        for kind in self.__repo.allTypes():
            item = QStandardItem(kind)
            item.setCheckable(True)
            item.setEditable(False)
            self.__typeTreeViewRootItem.appendRow(item)

        for vendor in self.__repo.allVendors():
            item = QStandardItem(vendor)
            item.setCheckable(True)
            item.setEditable(False)
            self.__vendorTreeViewRootItem.appendRow(item)

        for series in self.__repo.allSeries():
            item = QStandardItem(series)
            item.setCheckable(True)
            item.setEditable(False)
            self.__seriesTreeViewRootItem.appendRow(item)

        for line in self.__repo.allLines():
            item = QStandardItem(line)
            item.setCheckable(True)
            item.setEditable(False)
            self.__lineTreeViewRootItem.appendRow(item)

        for core in self.__repo.allCores():
            item = QStandardItem(core)
            item.setCheckable(True)
            item.setEditable(False)
            self.__coreTreeViewRootItem.appendRow(item)

        for package in self.__repo.allPackage():
            item = QStandardItem(package)
            item.setCheckable(True)
            item.setEditable(False)
            self.__packageTreeViewRootItem.appendRow(item)

        self.__proxyModelTreeView.setSourceModel(self.__modelTreeView)
        self.treeView.setModel(self.__proxyModelTreeView)
        self.treeView.expandAll()

        self.__modelTreeView.itemChanged.connect(self.__on_modelTreeView_itemChanged)

    def __initTableView(self):
        self.__proxyModelTableView = QSortFilterProxyModel(self)
        self.__modelTableView = QStandardItemModel(self.tableView)

        self.__modelTableView.setColumnCount(11)
        self.__modelTableView.setHeaderData(
            0, Qt.Orientation.Horizontal, self.tr("Name")
        )
        self.__modelTableView.setHeaderData(
            1, Qt.Orientation.Horizontal, self.tr("Market status")
        )
        self.__modelTableView.setHeaderData(
            2, Qt.Orientation.Horizontal, self.tr("Unit price for 10kU")
        )
        self.__modelTableView.setHeaderData(
            3, Qt.Orientation.Horizontal, self.tr("Package")
        )
        self.__modelTableView.setHeaderData(
            4, Qt.Orientation.Horizontal, self.tr("Flash")
        )
        self.__modelTableView.setHeaderData(
            5, Qt.Orientation.Horizontal, self.tr("RAM")
        )
        self.__modelTableView.setHeaderData(6, Qt.Orientation.Horizontal, self.tr("IO"))
        self.__modelTableView.setHeaderData(
            7, Qt.Orientation.Horizontal, self.tr("Frequency")
        )
        self.__modelTableView.setHeaderData(
            8, Qt.Orientation.Horizontal, self.tr("Vendor")
        )
        self.__modelTableView.setHeaderData(
            9, Qt.Orientation.Horizontal, self.tr("Core")
        )
        self.__modelTableView.setHeaderData(
            10, Qt.Orientation.Horizontal, self.tr("Type")
        )

        for soc in self.__repo.allSoc():
            items = [
                QStandardItem(soc.name),
                QStandardItem(self.tr("Unavailable")),
                QStandardItem(self.tr("Unavailable")),
                QStandardItem(soc.package),
                QStandardItem("%.2f" % soc.flash),
                QStandardItem("%.2f" % soc.ram),
                QStandardItem(str(soc.io)),
                QStandardItem("%.2f" % soc.frequency),
                QStandardItem(soc.vendor),
                QStandardItem(soc.core),
                QStandardItem("SOC"),
            ]
            for item in items:
                item.setEditable(False)
            self.__modelTableView.appendRow(items)

        self.__proxyModelTableView.setSourceModel(self.__modelTableView)
        self.tableView.setModel(self.__proxyModelTableView)
        self.tableView.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setSortingEnabled(True)
        self.tableView.sortByColumn(0, Qt.AscendingOrder)
        self.tableView.horizontalHeader().setMinimumSectionSize(10)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tableView.selectionModel().selectionChanged.connect(
            self.__on_tableView_selectionChanged
        )

    def __on_modelTreeView_itemChanged(self, item: QStandardItem):
        rowCount = item.rowCount()
        if rowCount > 0:  # root item
            for i in range(rowCount):
                child = item.child(i)
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
                if child.checkState() == Qt.CheckState.Checked:
                    checkedCount += 1

            if checkedCount == count:
                parent.setCheckState(Qt.CheckState.Checked)
            elif checkedCount == 0:
                parent.setCheckState(Qt.CheckState.Unchecked)
            else:
                parent.setCheckState(Qt.CheckState.PartiallyChecked)

    # noinspection PyUnusedLocal
    def __on_tableView_selectionChanged(
        self, selected: QItemSelection, deselected: QItemSelection
    ):
        indexes = selected.indexes()
        name: str = indexes[0].data()
        vendor: str = indexes[8].data()
        kind: str = indexes[10].data()
        if kind == "SOC":
            self.socFeatureView.setInfo(vendor, name)
            self.createBtn.setEnabled(True)
            self.__targetChip = name
            self.__vendor = vendor
        else:
            self.createBtn.setEnabled(False)

    def __on_createBtn_clicked(self):
        messageBox = NewMessageBox(self.window())
        if messageBox.exec():
            name = messageBox.nameLineEdit.text()
            path = messageBox.pathLineEdit.text()
            self.created.emit(path, name, self.__targetChip, self.__vendor)


class NewProjectWindow(MSFluentWindow):
    succeed = Signal()

    def __init__(self):
        super().__init__()

        self.navigationInterface.hide()
        self.stackedWidget.hide()

        self.__mainWindow = None

        self.view = NewProjectView()
        self.view.created.connect(self.__on_view_create)
        self.hBoxLayout.addWidget(self.view)

        self.__initWindow()
        self.showMaximized()

    # noinspection DuplicatedCode
    def __initWindow(self):
        self.resize(1100, 750)
        self.setWindowIcon(
            QIcon(os.path.join(SETTINGS.EXE_FOLDER, "resource", "images", "logo.svg"))
        )
        self.setWindowTitle("CSPLink")

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def __on_view_create(self, path: str, name: str, targetChip: str, vendor: str):
        PROJECT.new(path, name, targetChip, vendor)
        self.deleteLater()
        self.hide()
        self.succeed.emit()
        self.__mainWindow = MainWindow()
        self.__mainWindow.updateFrameless()
        self.__mainWindow.setAttribute(Qt.WidgetAttribute.WA_ShowModal, True)
        self.__mainWindow.show()
