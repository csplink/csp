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
# @file        gen_code_dialog.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-27     xqyjlj       initial version
#

import os

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import (QRegExpValidator)
from PyQt5.QtWidgets import QWidget, QApplication

from qfluentwidgets import (MessageBoxBase, Flyout, InfoBarIcon, MessageBox)

from .ui.Ui_gen_code_dialog import Ui_GenCodeDialog
from common import PROJECT, PACKAGE, Coder, Utils, Icon


class GenCodeDialogWidget(Ui_GenCodeDialog, QWidget):

    @property
    def ready(self) -> bool:
        if not (self.lineEdit_minHeapSize.isEnabled() and Utils.isHex(self.lineEdit_minHeapSize.text())):
            return False
        if not (self.lineEdit_minStackSize.isEnabled() and Utils.isHex(self.lineEdit_minStackSize.text())):
            return False
        return True

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.lineEdit_minHeapSize.setValidator(QRegExpValidator(QRegExp(R"(^0x[0-9A-Fa-f]+$)")))
        self.lineEdit_minStackSize.setValidator(QRegExpValidator(QRegExp(R"(^0x[0-9A-Fa-f]+$)")))

        # enable
        if Utils.isHex(PROJECT.defaultHeapSize):
            self.lineEdit_minHeapSize.setText(PROJECT.defaultHeapSize)
        elif Utils.isHex(PROJECT.summary.defaultHeapSize):
            self.lineEdit_minHeapSize.setText(PROJECT.summary.defaultHeapSize)
        else:
            self.lineEdit_minHeapSize.setEnabled(False)
        if Utils.isHex(PROJECT.defaultStackSize):
            self.lineEdit_minStackSize.setText(PROJECT.defaultStackSize)
        elif PROJECT.summary.defaultStackSize != "":
            self.lineEdit_minStackSize.setText(PROJECT.summary.defaultStackSize)
        else:
            self.lineEdit_minStackSize.setEnabled(False)

        self.checkBox_isCopyLibrary.setChecked(PROJECT.copyLibrary)
        self.checkBox_useToolchainsPackage.setChecked(PROJECT.useToolchainsPackage)

        self.toolButton_packageManager.setIcon(Icon.BOX)
        self.toolButton_toolchainsManager.setIcon(Icon.BOX)

        hal = PROJECT.summary.hal
        versions = PACKAGE.hal.get(hal, {}).keys()
        if len(versions) != 0:
            self.comboBox_packageVersion.addItems(versions)
            if PROJECT.halVersion == "":
                PROJECT.halVersion = self.comboBox_packageVersion.currentText()
            else:
                if PROJECT.halVersion not in versions:
                    self.comboBox_packageVersion.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The HAL package %1 is not installed.").replace(
                        "%1", f"{hal}@{PROJECT.halVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.comboBox_packageVersion.setCurrentText(PROJECT.halVersion)
            self.lineEdit_packagePath.setText(PROJECT.halPath)

        self.comboBox_packageVersion.currentTextChanged.connect(self.__onComboBox_packageVersionCurrentTextChanged)

        toolchains = PROJECT.summary.toolchains
        if len(toolchains) != 0:
            self.comboBox_toolchains.addItems(toolchains)
            self.comboBox_toolchains.setCurrentIndex(-1)
        self.comboBox_toolchains.currentTextChanged.connect(self.__onComboBox_toolchainsVersionCurrentTextChanged)

        builder = PROJECT.summary.builder
        builderList = builder.keys()
        if len(builderList) != 0:
            self.comboBox_builder.addItems(builderList)
            self.comboBox_builder.setCurrentIndex(-1)

        self.setMinimumWidth(900)

    def __onComboBox_packageVersionCurrentTextChanged(self, text: str):
        self.lineEdit_packagePath.setText(PACKAGE.path("hal", PROJECT.summary.hal, text))

    def __onComboBox_toolchainsVersionCurrentTextChanged(self, text: str):
        self.lineEdit_toolchainsPath.setText(
            PACKAGE.path("toolchains", text, self.comboBox_toolchainsVersion.currentText()))


class GenCodeDialog(MessageBoxBase):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.main_widget = GenCodeDialogWidget(self)
        self.viewLayout.addWidget(self.main_widget)

        self.yesButton.setText(self.tr('Generate'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.yesButton.disconnect()
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

    def __showError(self, message: str):
        Flyout.create(icon=InfoBarIcon.ERROR,
                      title=self.tr('Error'),
                      content=message,
                      target=self.yesButton,
                      parent=self.window())

    def __onYesButtonClicked(self):
        hal = PROJECT.summary.hal
        defaultHeapSize = self.main_widget.lineEdit_minHeapSize.text()
        defaultStackSize = self.main_widget.lineEdit_minStackSize.text()
        isCopyLibrary = self.main_widget.checkBox_isCopyLibrary.isChecked()
        packagePath = self.main_widget.lineEdit_packagePath.text()

        if not (self.main_widget.lineEdit_minHeapSize.isEnabled() and Utils.isHex(defaultHeapSize)):
            self.__showError(self.tr("The minimum heap size data is invalid"))
            return
        elif not (self.main_widget.lineEdit_minStackSize.isEnabled() and Utils.isHex(defaultStackSize)):
            self.__showError(self.tr("The minimum stack size data is invalid"))
            return
        elif self.main_widget.comboBox_packageVersion.currentText() == "":
            self.__showError(self.tr("Please select a valid package version"))
            return
        elif not os.path.isdir(packagePath):
            error = self.tr("'%1' is not directory! maybe '%2' not yet installed.").replace("%1", packagePath).replace(
                "%2", f"{hal}@{PROJECT.halVersion}")
            self.__showError(error)
            return
        else:
            PROJECT.defaultHeapSize = defaultHeapSize
            PROJECT.defaultStackSize = defaultStackSize
            PROJECT.copyLibrary = isCopyLibrary
            PROJECT.halVersion = self.main_widget.comboBox_packageVersion.currentText()

            coder = Coder()
            coder.generate(PROJECT.halPath)
            self.reject()
            self.rejected.emit()
