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
# @file        main_window.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import os

from PySide6.QtCore import QUrl, QPoint, QSize, QEventLoop, QTimer, Qt
from PySide6.QtGui import QIcon, QDesktopServices, QCloseEvent
from PySide6.QtWidgets import QHBoxLayout, QApplication, QWidget, QSplitter, QMessageBox
from loguru import logger
from qfluentwidgets import (
    NavigationItemPosition,
    MessageBox,
    MSFluentTitleBar,
    MSFluentWindow,
    RoundMenu,
    Action,
    TransparentPushButton,
    SplashScreen,
    FluentIconBase,
    NavigationBarPushButton,
    BodyLabel,
    getFont,
    FluentStyleSheet,
)

from common import Icon, SETTINGS, SIGNAL_BUS, PROJECT, Coder
from dialogs import PackageInstallDialog
from view import ClockTreeView, CodeView, PackageView, SettingView, SocView
from widget import StackedWidget, PlainTextEditLogger, TabWidget


class CustomTitleBar(MSFluentTitleBar):
    """Title bar with icon and title"""

    def __init__(self, parent):
        super().__init__(parent)

        # add buttons
        self.btn_layout = QHBoxLayout()

        # ----------------------------------------------------------------------
        self.project_btn = TransparentPushButton(self.tr("Project"), self)  # type: ignore
        self.project_menu = self.__create_project_menu()
        self.project_btn.clicked.connect(
            lambda: self.project_menu.exec(
                self.project_btn.mapToGlobal(QPoint(0, self.project_btn.height())),
                ani=True,
            )
        )
        # ----------------------------------------------------------------------
        self.help_btn = TransparentPushButton(self.tr("Help"), self)  # type: ignore
        self.help_menu = self.__create_help_menu()
        self.help_btn.clicked.connect(
            lambda: self.help_menu.exec(
                self.help_btn.mapToGlobal(QPoint(0, self.help_btn.height())), ani=True
            )
        )
        # ----------------------------------------------------------------------
        self.package_btn = TransparentPushButton(self.tr("Package"), self)  # type: ignore
        self.package_menu = self.__create_package_menu()
        self.package_btn.clicked.connect(
            lambda: self.package_menu.exec(
                self.package_btn.mapToGlobal(QPoint(0, self.package_btn.height())),
                ani=True,
            )
        )
        # ----------------------------------------------------------------------
        self.btn_layout.setContentsMargins(20, 0, 20, 0)
        self.btn_layout.setSpacing(15)

        self.btn_layout.addWidget(self.project_btn)
        self.btn_layout.addWidget(self.help_btn)
        self.btn_layout.addWidget(self.package_btn)

        self.layout_header = self.hBoxLayout
        self.layout_header.insertLayout(4, self.btn_layout)

        self.project_label = BodyLabel(self)
        self.project_label.setFont(getFont(16))
        self.project_label.setText(PROJECT.title())
        PROJECT.title_changed.connect(lambda s: self.project_label.setText(s))

        self.hBoxLayout.insertWidget(
            5,
            self.project_label,
            100,
            Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter,
        )
        self.layout_header.setStretch(6, 0)

    def __create_project_menu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        # self.new_action = Action(self.tr('New'))
        # self.new_action.setShortcut("Ctrl+N")
        # menu.addAction(self.new_action)
        #
        # self.open_action = Action(self.tr('Open'))
        # self.open_action.setShortcut("Ctrl+O")
        # menu.addAction(self.open_action)

        self.save_action = Action(self.tr("Save"))  # type: ignore
        # self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(lambda: PROJECT.save())
        menu.addAction(self.save_action)

        menu.addSeparator()

        self.generate_action = Action(self.tr("Generate"))  # type: ignore
        # self.generate_action.setShortcut("Ctrl+G")
        self.generate_action.triggered.connect(lambda: self.generate_code())
        menu.addAction(self.generate_action)

        return menu

    def __create_help_menu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.about_qt_action = Action(self.tr("About Qt"))  # type: ignore
        self.about_qt_action.triggered.connect(
            lambda: QMessageBox.aboutQt(self.window(), self.tr("About Qt"))  # type: ignore
        )
        menu.addAction(self.about_qt_action)

        self.about_action = Action(self.tr("About"))  # type: ignore
        menu.addAction(self.about_action)

        menu.addSeparator()

        self.open_source_license_action = Action(self.tr("Open Source License"))  # type: ignore
        menu.addAction(self.open_source_license_action)

        return menu

    def __create_package_menu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.install_package_action = Action(self.tr("Install"))  # type: ignore
        self.install_package_action.triggered.connect(
            lambda: PackageInstallDialog(self.window()).exec()
        )
        menu.addAction(self.install_package_action)

        return menu

    def generate_code(self):
        succeed, msg = PROJECT.is_generate_setting_valid()
        if not succeed:
            logger.error(msg)
            title = self.tr("Error")  # type: ignore
            content = self.tr("The coder settings is invalid. Please check it.")  # type: ignore
            message = MessageBox(title, content, self.window())
            message.setContentCopyable(True)
            message.cancelButton.setDisabled(True)
            message.raise_()
            message.exec()
            SIGNAL_BUS.navigation_requested.emit("SettingView", "GenerateSettingView")
            return

        coder = Coder()
        coder.generate()


class MainWindow(MSFluentWindow):

    def __init__(self):
        super().__init__()

        self.__views = {}

        self.__init_window()

        loop = QEventLoop(self)
        QTimer.singleShot(3000, loop.quit)  # splash screen show at least 3s
        QApplication.processEvents()

        self.soc_view = SocView(self)
        self.clock_tree_view = ClockTreeView(self)

        # ugly, because when opengl is created, the window will automatically hide
        self.show()

        self.code_view = CodeView(self)
        self.package_view = PackageView(self)
        self.setting_view = SettingView(self)

        self.view_splitter = QSplitter(Qt.Orientation.Vertical, self)
        self.sub_tab_view = TabWidget(self.view_splitter)
        self.plain_text_edit_logger = PlainTextEditLogger(self.sub_tab_view)
        self.plain_text_edit_logger.setObjectName("plainTextEditLogger")

        old = self.stackedWidget
        old.deleteLater()
        self.stackedWidget = StackedWidget(self.view_splitter)
        self.stacked_widget = self.stackedWidget

        self.__init_main_view()
        self.__init_navigation()
        self.__init_sub_tab_view()

        # project --------------------------------------------------------------

        SIGNAL_BUS.navigation_requested.connect(
            self.__on_x_navigationRequested, Qt.ConnectionType.QueuedConnection
        )
        self.stacked_widget.current_changed.connect(
            self.__on_stackedWidget_currentChanged, Qt.ConnectionType.QueuedConnection
        )

        if SETTINGS.DEBUG:
            self.splash_screen.finish()
        else:
            loop.exec()
            self.splash_screen.finish()
            self.showMaximized()

    def closeEvent(self, event: QCloseEvent):
        if PROJECT.is_changed():
            title = self.tr("Warning")  # type: ignore
            content = self.tr(  # type: ignore
                "The project {!r} has not been saved yet, do you want to exit?"
            ).format(PROJECT.project().name)
            message = MessageBox(title, content, self.window())
            message.setContentCopyable(True)
            message.raise_()
            if message.exec():
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def __init_navigation(self):
        self.__add_view(self.soc_view, Icon.CPU, self.tr("SOC"), Icon.CPU)  # type: ignore
        self.__add_view(self.clock_tree_view, Icon.TIME, self.tr("Clock"), Icon.TIME)  # type: ignore
        self.__add_view(self.code_view, Icon.CODE, self.tr("Code"), Icon.CODE)  # type: ignore

        self.navigationInterface.addItem(
            routeKey="Generate",
            icon=Icon.FOLDER_TRANSFER,
            text=self.tr("Generate"),  # type: ignore
            onClick=lambda: self.titleBar.generateCode(),  # type: ignore
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.navigationInterface.addItem(
            routeKey="Sponsor",
            icon=Icon.MONEY,
            text=self.tr("Sponsor"),  # type: ignore
            onClick=self.__on_sponsorKey_clicked,
            selectable=False,
            position=NavigationItemPosition.BOTTOM,
        )

        self.__add_view(
            self.package_view,
            Icon.BOOK_SHELF,
            self.tr("Package"),  # type: ignore
            Icon.BOOK_SHELF,
            NavigationItemPosition.BOTTOM,
        )
        self.__add_view(
            self.setting_view,
            Icon.SETTING,
            self.tr("Settings"),  # type: ignore
            Icon.SETTING,
            NavigationItemPosition.BOTTOM,
        )
        self.navigationInterface.setCurrentItem(self.soc_view.objectName())

    def __init_main_view(self):
        self.hBoxLayout.removeWidget(self.stacked_widget)
        self.view_splitter.addWidget(self.stacked_widget)
        self.view_splitter.addWidget(self.sub_tab_view)
        self.view_splitter.setSizes([700, 200])
        self.view_splitter.setCollapsible(0, False)
        self.view_splitter.setCollapsible(1, False)
        self.hBoxLayout.addWidget(self.view_splitter, 1)

        FluentStyleSheet.FLUENT_WINDOW.apply(self.stacked_widget)

    def __init_window(self):
        self.bar_title = CustomTitleBar(self)
        self.setTitleBar(self.bar_title)

        self.resize(1100, 750)
        self.setWindowIcon(
            QIcon(os.path.join(SETTINGS.EXE_FOLDER, "resource", "images", "logo.svg"))
        )
        self.setWindowTitle("CSPLink")

        self.updateFrameless()
        self.setMicaEffectEnabled(False)

        self.splash_screen = SplashScreen(self.windowIcon(), self)
        self.splash_screen.setIconSize(QSize(106, 106))
        self.splash_screen.raise_()

        # noinspection DuplicatedCode
        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.show()

    def __init_sub_tab_view(self):
        self.sub_tab_view.add_sub_interface(self.plain_text_edit_logger, self.tr("Log"))  # type: ignore

    def __add_view(
        self,
        view: QWidget,
        icon: FluentIconBase,
        text: str,
        selected_icon=None,
        position=NavigationItemPosition.TOP,
        is_transparent=False,
    ) -> NavigationBarPushButton:
        self.__views[view.objectName()] = view
        return self.addSubInterface(
            view, icon, text, selected_icon, position, is_transparent
        )

    def __on_sponsorKey_clicked(self):
        message = MessageBox(
            self.tr("Sponsor"),  # type: ignore
            self.tr(  # type: ignore
                """The csplink projects are personal open-source projects, their development need your help.
If you would like to support the development of csplink, you are encouraged to donate!"""
            ),
            self,
        )
        message.yesButton.setText(self.tr("OK"))  # type: ignore
        message.cancelButton.setText(self.tr("Cancel"))  # type: ignore

        if message.exec():
            QDesktopServices.openUrl(QUrl(SETTINGS.AUTHOR_BLOG_URL))

    def __on_x_navigationRequested(self, route_key: str, sub_key: str):
        if route_key in self.navigationInterface.items.keys():
            self.switchTo(self.__views[route_key])
            self.navigationInterface.setCurrentItem(route_key)
            if route_key == "SettingView" and len(sub_key) > 0:
                self.setting_view.switch_to(sub_key)

    def __on_stackedWidget_currentChanged(self, index: int):
        view = self.stacked_widget.widget(index)
        if view == self.code_view:
            self.code_view.flush()
        elif view == self.package_view:
            self.package_view.flush()
