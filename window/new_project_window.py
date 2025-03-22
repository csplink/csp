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
        self.title_label = SubtitleLabel(self.tr("Create a new project"), self)  # type: ignore
        # ----------------------------------------------------------------------
        self.name_line_edit = LineEdit(self)
        self.name_line_edit.setPlaceholderText(self.tr("Project Name"))  # type: ignore
        self.name_line_edit.setClearButtonEnabled(True)
        self.name_line_edit.textChanged.connect(self.__on_xLineEdit_textChanged)
        # ----------------------------------------------------------------------
        self.path_layout = QHBoxLayout()

        self.path_line_edit = LineEdit(self)
        self.path_line_edit.setReadOnly(True)
        self.path_line_edit.setPlaceholderText(self.tr("Project Path"))  # type: ignore
        self.path_line_edit.setClearButtonEnabled(True)
        self.path_line_edit.textChanged.connect(self.__on_xLineEdit_textChanged)

        self.folder_btn = ToolButton()
        self.folder_btn.pressed.connect(self.__on_folderBtn_pressed)
        self.folder_btn.setIcon(Icon.FOLDER)

        self.path_layout.addWidget(self.path_line_edit)
        self.path_layout.addWidget(self.folder_btn)
        # ----------------------------------------------------------------------
        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addWidget(self.name_line_edit)
        self.viewLayout.addLayout(self.path_layout)
        # ----------------------------------------------------------------------
        self.yesButton.setText(self.tr("OK"))  # type: ignore
        self.yesButton.setEnabled(False)
        self.yesButton.clicked.disconnect()  # self._MessageBoxBase__onYesButtonClicked
        self.yesButton.clicked.connect(self.__on_yesButton_clicked)
        self.cancelButton.setText(self.tr("Cancel"))  # type: ignore

        self.widget.setFixedWidth(560)

    # noinspection PyUnusedLocal
    def __on_xLineEdit_textChanged(self, text: str):
        if (
            os.path.isdir(self.path_line_edit.text())
            and len(self.name_line_edit.text()) > 0
        ):
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)

    def __on_folderBtn_pressed(self):
        path = QFileDialog.getExistingDirectory(
            self, self.tr("Choose project path"), SETTINGS.last_new_project_folder.value  # type: ignore
        )
        if os.path.isdir(path):
            SETTINGS.set(SETTINGS.last_new_project_folder, path)
            self.path_line_edit.setText(path)

    def __on_yesButton_clicked(self):
        path = os.path.join(self.path_line_edit.text(), self.name_line_edit.text())
        if os.path.isdir(path):
            title = self.tr("Warning")  # type: ignore
            content = self.tr(  # type: ignore
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
        self.main_v_layout = QVBoxLayout(self)
        self.main_v_layout.setContentsMargins(0, 0, 0, 0)
        self.info_h_layout = QHBoxLayout()

        self.text_browser = TextBrowser(self)
        self.text_browser.setObjectName("readmeTextBrowser")
        self.text_browser.setReadOnly(True)

        # ----------------------------------------------------------------------
        self.url_btn_group_layout = QVBoxLayout()
        self.soc_name_label = StrongBodyLabel("SOC Name", self)
        self.vendor_name_label = StrongBodyLabel("Vendor Name", self)
        self.soc_name_label.installEventFilter(self)
        self.vendor_name_label.installEventFilter(self)
        self.soc_name_label.setFixedSize(200, 19)
        self.vendor_name_label.setFixedSize(200, 19)
        self.url_btn_group_layout.addWidget(
            self.soc_name_label, 0, Qt.AlignmentFlag.AlignTop
        )
        self.url_btn_group_layout.addWidget(
            self.vendor_name_label, 0, Qt.AlignmentFlag.AlignTop
        )
        self.info_h_layout.addLayout(self.url_btn_group_layout)
        self.info_h_layout.addSpacing(50)

        # ----------------------------------------------------------------------
        self.info1_layout = QVBoxLayout()
        self.package_name_label = BodyLabel("Package Name", self)
        self.market_status_label = BodyLabel("Market Name", self)
        self.package_name_label.setFixedSize(100, 19)
        self.market_status_label.setFixedSize(100, 19)
        self.info1_layout.addWidget(
            self.package_name_label, 0, Qt.AlignmentFlag.AlignTop
        )
        self.info1_layout.addWidget(
            self.market_status_label, 0, Qt.AlignmentFlag.AlignTop
        )
        self.info_h_layout.addLayout(self.info1_layout)
        self.info_h_layout.addSpacing(20)

        # ----------------------------------------------------------------------
        self.package_pixmap_label = PixmapLabel(self)
        self.package_pixmap_label.setFixedSize(80, 80)
        self.info_h_layout.addWidget(
            self.package_pixmap_label, 0, Qt.AlignmentFlag.AlignLeft
        )
        self.info_h_layout.addSpacing(20)

        # ----------------------------------------------------------------------
        self.info2_layout = QVBoxLayout()
        self.info2_child_layout = QHBoxLayout()
        self.introduction_label = StrongBodyLabel("Introduction", self)
        self.price_label = BodyLabel("Price", self)
        self.introduction_label.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )

        self.info2_child_layout.addWidget(self.price_label)
        self.info2_layout.addWidget(
            self.introduction_label, 0, Qt.AlignmentFlag.AlignTop
        )
        self.info2_layout.addLayout(self.info2_child_layout)
        self.info_h_layout.addLayout(self.info2_layout)

        # ----------------------------------------------------------------------

        self.main_v_layout.addLayout(self.info_h_layout)
        self.main_v_layout.addWidget(self.text_browser)

        Style.NEW_PROJECT_WINDOW.apply(self.text_browser)

    # region overrides

    def eventFilter(self, watched: QObject, event: QEvent) -> bool:
        if isinstance(watched, StrongBodyLabel):
            if event.type() == QEvent.Type.MouseButtonRelease:
                url = watched.property("url")
                if url is not None and url != "":
                    QDesktopServices.openUrl(QUrl(url))
        return super().eventFilter(watched, event)

    # endregion

    def set_info(self, vendor: str, name: str):
        summary = SUMMARY.get_summary(vendor, name)
        locale = SETTINGS.get(SETTINGS.language).value.name()
        self.soc_name_label.setText(name)
        self.vendor_name_label.setText(vendor)
        self.package_name_label.setText(summary.package)
        self.market_status_label.setText("")
        self.introduction_label.setText(summary.introduction.get(locale))
        self.text_browser.setMarkdown(summary.illustrate.get(locale))
        self.price_label.setText("")
        package_path = f"{SETTINGS.PACKAGES_IMAGE_FOLDER}/{summary.package.upper()}.png"
        if os.path.exists(package_path):
            pixmap = QPixmap(package_path)
        else:
            pixmap = QPixmap(f"{SETTINGS.PACKAGES_IMAGE_FOLDER}/unknown.png")
        pixmap = pixmap.scaled(
            80,
            80,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        self.package_pixmap_label.setPixmap(pixmap)
        self.show()


class NewProjectView(Ui_NewProjectView, QWidget):
    created = Signal(str, str, str, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.__repo = Repository().repository()
        self.__target_chip = ""
        self.__vendor = ""

        self.create_btn = PushButton(self.tr("Create"), self)  # type: ignore
        self.create_btn.setEnabled(False)
        self.btnGroupHorizontalLayout.addWidget(
            self.create_btn, 0, Qt.AlignmentFlag.AlignRight
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

        self.__init_tree_view()
        self.__init_table_view()

        self.soc_feature_view = SocFeatureView(self)

        self.add_sub_interface(self.soc_feature_view, Icon.FOLDER, self.tr("Feature"))  # type: ignore

        self.tabBar.setCurrentItem(self.soc_feature_view.objectName())
        self.soc_feature_view.hide()

        self.create_btn.clicked.connect(self.__on_createBtn_clicked)

    def add_sub_interface(self, interface: QWidget, icon: FluentIconBase, text: str):
        self.stackedWidget.addWidget(interface)
        self.tabBar.addItem(
            routeKey=interface.objectName(),
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(interface),
        )

    def __init_tree_view(self):
        self.__proxy_model_tree_view = QSortFilterProxyModel(self)
        self.__model_tree_view = QStandardItemModel(self.treeView)

        self.__type_tree_view_root_item = QStandardItem(self.tr("Type"))  # type: ignore
        self.__vendor_tree_view_root_item = QStandardItem(self.tr("Vendor"))  # type: ignore
        self.__series_tree_view_root_item = QStandardItem(self.tr("Series"))  # type: ignore
        self.__line_tree_view_root_item = QStandardItem(self.tr("Line"))  # type: ignore
        self.__core_tree_view_root_item = QStandardItem(self.tr("Core"))  # type: ignore
        self.__package_tree_view_root_item = QStandardItem(self.tr("Package"))  # type: ignore

        self.__type_tree_view_root_item.setCheckable(True)
        self.__vendor_tree_view_root_item.setCheckable(True)
        self.__series_tree_view_root_item.setCheckable(True)
        self.__line_tree_view_root_item.setCheckable(True)
        self.__core_tree_view_root_item.setCheckable(True)
        self.__package_tree_view_root_item.setCheckable(True)

        self.__type_tree_view_root_item.setEditable(False)
        self.__vendor_tree_view_root_item.setEditable(False)
        self.__series_tree_view_root_item.setEditable(False)
        self.__line_tree_view_root_item.setEditable(False)
        self.__core_tree_view_root_item.setEditable(False)
        self.__package_tree_view_root_item.setEditable(False)

        self.__model_tree_view.appendRow(self.__type_tree_view_root_item)
        self.__model_tree_view.appendRow(self.__vendor_tree_view_root_item)
        self.__model_tree_view.appendRow(self.__series_tree_view_root_item)
        self.__model_tree_view.appendRow(self.__line_tree_view_root_item)
        self.__model_tree_view.appendRow(self.__core_tree_view_root_item)
        self.__model_tree_view.appendRow(self.__package_tree_view_root_item)

        for kind in self.__repo.all_types():
            item = QStandardItem(kind)
            item.setCheckable(True)
            item.setEditable(False)
            self.__type_tree_view_root_item.appendRow(item)

        for vendor in self.__repo.all_vendors():
            item = QStandardItem(vendor)
            item.setCheckable(True)
            item.setEditable(False)
            self.__vendor_tree_view_root_item.appendRow(item)

        for series in self.__repo.all_series():
            item = QStandardItem(series)
            item.setCheckable(True)
            item.setEditable(False)
            self.__series_tree_view_root_item.appendRow(item)

        for line in self.__repo.all_lines():
            item = QStandardItem(line)
            item.setCheckable(True)
            item.setEditable(False)
            self.__line_tree_view_root_item.appendRow(item)

        for core in self.__repo.all_cores():
            item = QStandardItem(core)
            item.setCheckable(True)
            item.setEditable(False)
            self.__core_tree_view_root_item.appendRow(item)

        for package in self.__repo.all_package():
            item = QStandardItem(package)
            item.setCheckable(True)
            item.setEditable(False)
            self.__package_tree_view_root_item.appendRow(item)

        self.__proxy_model_tree_view.setSourceModel(self.__model_tree_view)
        self.treeView.setModel(self.__proxy_model_tree_view)
        self.treeView.expandAll()

        self.__model_tree_view.itemChanged.connect(self.__on_modelTreeView_itemChanged)

    def __init_table_view(self):
        self.__proxy_model_table_view = QSortFilterProxyModel(self)
        self.__model_table_view = QStandardItemModel(self.tableView)

        self.__model_table_view.setColumnCount(11)
        self.__model_table_view.setHeaderData(
            0, Qt.Orientation.Horizontal, self.tr("Name")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            1, Qt.Orientation.Horizontal, self.tr("Market status")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            2, Qt.Orientation.Horizontal, self.tr("Unit price for 10kU")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            3, Qt.Orientation.Horizontal, self.tr("Package")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            4, Qt.Orientation.Horizontal, self.tr("Flash")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            5, Qt.Orientation.Horizontal, self.tr("RAM")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            6, Qt.Orientation.Horizontal, self.tr("IO")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            7, Qt.Orientation.Horizontal, self.tr("Frequency")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            8, Qt.Orientation.Horizontal, self.tr("Vendor")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            9, Qt.Orientation.Horizontal, self.tr("Core")  # type: ignore
        )
        self.__model_table_view.setHeaderData(
            10, Qt.Orientation.Horizontal, self.tr("Type")  # type: ignore
        )

        for soc in self.__repo.all_soc():
            items = [
                QStandardItem(soc.name),
                QStandardItem(self.tr("Unavailable")),  # type: ignore
                QStandardItem(self.tr("Unavailable")),  # type: ignore
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
            self.__model_table_view.appendRow(items)

        self.__proxy_model_table_view.setSourceModel(self.__model_table_view)
        self.tableView.setModel(self.__proxy_model_table_view)
        self.tableView.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.tableView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.tableView.setSortingEnabled(True)
        self.tableView.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        self.tableView.horizontalHeader().setMinimumSectionSize(10)
        self.tableView.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        self.tableView.selectionModel().selectionChanged.connect(
            self.__on_tableView_selectionChanged
        )

    def __on_modelTreeView_itemChanged(self, item: QStandardItem):
        row_count = item.rowCount()
        if row_count > 0:  # root item
            for i in range(row_count):
                child = item.child(i)
                if item.checkState() == Qt.CheckState.Checked:
                    child.setCheckState(Qt.CheckState.Checked)
                elif item.checkState() == Qt.CheckState.Unchecked:
                    child.setCheckState(Qt.CheckState.Unchecked)
        else:  # root item's child
            parent = item.parent()
            count = parent.rowCount()
            checked_count = 0
            for i in range(count):
                child = parent.child(i)
                if child.checkState() == Qt.CheckState.Checked:
                    checked_count += 1

            if checked_count == count:
                parent.setCheckState(Qt.CheckState.Checked)
            elif checked_count == 0:
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
            self.soc_feature_view.set_info(vendor, name)
            self.create_btn.setEnabled(True)
            self.__target_chip = name
            self.__vendor = vendor
        else:
            self.create_btn.setEnabled(False)

    def __on_createBtn_clicked(self):
        message_box = NewMessageBox(self.window())
        if message_box.exec():
            name = message_box.name_line_edit.text()
            path = message_box.path_line_edit.text()
            self.created.emit(path, name, self.__target_chip, self.__vendor)


class NewProjectWindow(MSFluentWindow):
    succeed = Signal()

    def __init__(self):
        super().__init__()

        self.navigationInterface.hide()
        self.stackedWidget.hide()

        self.__main_window = None

        self.view = NewProjectView()
        self.view.created.connect(self.__on_view_create)
        self.hBoxLayout.addWidget(self.view)

        self.__init_window()
        self.showMaximized()

    # noinspection DuplicatedCode
    def __init_window(self):
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

    def __on_view_create(self, path: str, name: str, target_chip: str, vendor: str):
        PROJECT.new(path, name, target_chip, vendor)
        self.deleteLater()
        self.hide()
        self.succeed.emit()
        self.__main_window = MainWindow()
        self.__main_window.updateFrameless()
        self.__main_window.setAttribute(Qt.WidgetAttribute.WA_ShowModal, True)
        self.__main_window.show()
