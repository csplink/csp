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
from PySide6.QtWidgets import (QFileDialog, QHBoxLayout)
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, ToolButton, ProgressBar, CaptionLabel, BodyLabel)

from common import Icon, SETTINGS, PACKAGE, SIGNAL_BUS


# from qframelesswindow import (FramelessDialog)


class PackageInstallThread(QThread):
    progressUpdated = Signal(str, float)

    def __init__(self, path: str, parent: QObject):
        super().__init__(parent=parent)
        self.path = path

    def run(self):
        PACKAGE.install(self.path, self.__package_install_callback)

    def __package_install_callback(self, file: str, progress: float):
        self.progressUpdated.emit(file, progress)


class PackageInstallDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.titleLabel = SubtitleLabel(self.tr('Install package'), self)
        # ----------------------------------------------------------------------
        self.pathLayout = QHBoxLayout()

        self.pathLineEdit = LineEdit(self)
        self.pathLineEdit.setReadOnly(True)
        self.pathLineEdit.setPlaceholderText(self.tr('Choose package (*.csppack) path'))
        self.pathLineEdit.textChanged.connect(self.__on_pathLineEdit_textChanged)

        self.folderBtn = ToolButton()
        self.folderBtn.pressed.connect(self.__on_folderBtn_pressed)
        self.folderBtn.setIcon(Icon.FOLDER)

        self.pathLayout.addWidget(self.pathLineEdit)
        self.pathLayout.addWidget(self.folderBtn)
        # ----------------------------------------------------------------------
        self.progressLayout = QHBoxLayout()

        self.progressBar = ProgressBar(self)

        self.progressLabel = CaptionLabel(self)
        self.progressLabel.setMinimumWidth(3 + self.progressLabel.fontMetrics().horizontalAdvance('100%'))
        self.progressLabel.setText(self.progressBar.valText())

        self.progressLayout.addWidget(self.progressBar)
        self.progressLayout.addWidget(self.progressLabel)
        self.progressBar.hide()
        self.progressLabel.hide()
        # ----------------------------------------------------------------------
        self.fileLabel = BodyLabel(self)
        self.fileLabel.hide()
        # ----------------------------------------------------------------------
        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addLayout(self.pathLayout)
        self.viewLayout.addLayout(self.progressLayout)
        self.viewLayout.addWidget(self.fileLabel)
        # ----------------------------------------------------------------------
        self.yesButton.setText(self.tr('Install'))
        self.yesButton.clicked.disconnect()  # self._MessageBoxBase__onYesButtonClicked
        self.yesButton.clicked.connect(self.__on_yesButton_clicked)
        self.yesButton.setEnabled(False)

        self.widget.setFixedWidth(560)

    def __on_pathLineEdit_textChanged(self, text: str):
        if os.path.isfile(text):
            self.yesButton.setEnabled(True)
        else:
            self.yesButton.setEnabled(False)

    def __on_folderBtn_pressed(self):
        path, _ = QFileDialog.getOpenFileName(self, self.tr('Choose CSP package file'),
                                               SETTINGS.lastPackageFileFolder.value,
                                               self.tr('CSP package file (*.csppack)'))
        if os.path.isfile(path):
            SETTINGS.set(SETTINGS.lastPackageFileFolder, os.path.dirname(path))
            self.pathLineEdit.setText(path)

    def __on_yesButton_clicked(self):
        thread = PackageInstallThread(self.pathLineEdit.text(), self)
        thread.progressUpdated.connect(self.__updateProgress)
        thread.started.connect(self.__showProgress)
        thread.finished.connect(self.__finish)
        thread.start()
        self.yesButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

    def __showProgress(self):
        self.progressBar.show()
        self.progressLabel.show()
        self.fileLabel.show()

    def __updateProgress(self, file: str, progress: float):
        self.progressBar.setVal(progress * 100)
        self.progressLabel.setText(self.progressBar.valText())
        self.fileLabel.setText(file)

    def __finish(self):
        SIGNAL_BUS.packageUpdated.emit()
        self.accept()
