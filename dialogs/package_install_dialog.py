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
# @file        package_install_dialog.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-21     xqyjlj       initial version
#

import os

from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QFileDialog, QHBoxLayout
from qfluentwidgets import (
    MessageBoxBase,
    SubtitleLabel,
    LineEdit,
    ToolButton,
    ProgressBar,
    CaptionLabel,
    BodyLabel,
)

from common import Icon, SETTINGS, PACKAGE, SIGNAL_BUS


class PackageInstallThread(QThread):
    progress_updated = Signal(str, float)

    def __init__(self, path: str, parent: QObject):
        super().__init__(parent=parent)
        self.path = path

    def run(self):
        PACKAGE.install(self.path, self.__package_install_callback)

    def __package_install_callback(self, file: str, progress: float):
        self.progress_updated.emit(file, progress)


class PackageInstallDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.title_label = SubtitleLabel(self.tr("Install package"), self)  # type: ignore
        # ----------------------------------------------------------------------
        self.path_layout = QHBoxLayout()

        self.path_line_edit = LineEdit(self)
        self.path_line_edit.setReadOnly(True)
        self.path_line_edit.setPlaceholderText(self.tr("Choose package (*.csppack) path"))  # type: ignore
        self.path_line_edit.textChanged.connect(self.__on_path_line_edit_textChanged)

        self.folder_btn = ToolButton()
        self.folder_btn.pressed.connect(self.__on_folder_btn_pressed)
        self.folder_btn.setIcon(Icon.FOLDER)

        self.path_layout.addWidget(self.path_line_edit)
        self.path_layout.addWidget(self.folder_btn)
        # ----------------------------------------------------------------------
        self.progress_layout = QHBoxLayout()

        self.progress_bar = ProgressBar(self)

        self.progress_label = CaptionLabel(self)
        self.progress_label.setMinimumWidth(
            3 + self.progress_label.fontMetrics().horizontalAdvance("100%")
        )
        self.progress_label.setText(self.progress_bar.valText())

        self.progress_layout.addWidget(self.progress_bar)
        self.progress_layout.addWidget(self.progress_label)
        self.progress_bar.hide()
        self.progress_label.hide()
        # ----------------------------------------------------------------------
        self.file_label = BodyLabel(self)
        self.file_label.hide()
        # ----------------------------------------------------------------------
        self.viewLayout.addWidget(self.title_label)
        self.viewLayout.addLayout(self.path_layout)
        self.viewLayout.addLayout(self.progress_layout)
        self.viewLayout.addWidget(self.file_label)
        # ----------------------------------------------------------------------
        self.yesButton.setText(self.tr("Install"))  # type: ignore
        self.yesButton.clicked.disconnect()  # self._MessageBoxBase__onYesButtonClicked
        self.yesButton.clicked.connect(self.__on_yes_button_clicked)
        self.yesButton.setEnabled(False)

        self.widget.setFixedWidth(560)

    def __on_path_line_edit_textChanged(self, text: str):
        if os.path.isfile(text):
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)

    def __on_folder_btn_pressed(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            self.tr("Choose CSP package file"),  # type: ignore
            SETTINGS.last_package_file_folder.value,
            self.tr("CSP package file (*.csppack)"),  # type: ignore
        )
        if os.path.isfile(path):
            SETTINGS.set(SETTINGS.last_package_file_folder, os.path.dirname(path))
            self.path_line_edit.setText(path)

    def __on_yes_button_clicked(self):
        thread = PackageInstallThread(self.path_line_edit.text(), self)
        thread.progress_updated.connect(self.__update_progress)
        thread.started.connect(self.__show_progress)
        thread.finished.connect(self.__finish)
        thread.start()
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

    def __show_progress(self):
        self.progress_bar.show()
        self.progress_label.show()
        self.file_label.show()

    def __update_progress(self, file: str, progress: float):
        self.progress_bar.setVal(progress * 100)
        self.progress_label.setText(self.progress_bar.valText())
        self.file_label.setText(file)

    def __finish(self):
        SIGNAL_BUS.package_updated.emit()
        self.accept()
