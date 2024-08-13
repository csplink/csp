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

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import (QRegularExpressionValidator)
from PySide6.QtWidgets import QWidget

from qfluentwidgets import (MessageBoxBase, Flyout, InfoBarIcon, MessageBox)

from .ui.Ui_gen_code_dialog import Ui_GenCodeDialog
from common import PROJECT, PACKAGE, Coder, Utils, Icon


class GenCodeDialogWidget(Ui_GenCodeDialog, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.lineEdit_minHeapSize.setValidator(QRegularExpressionValidator(QRegularExpression(R"(^0x[0-9A-Fa-f]+$)")))
        self.lineEdit_minStackSize.setValidator(QRegularExpressionValidator(QRegularExpression(R"(^0x[0-9A-Fa-f]+$)")))

        # linker default heap size
        if Utils.isHex(PROJECT.defaultHeapSize):
            self.lineEdit_minHeapSize.setText(PROJECT.defaultHeapSize)
        elif Utils.isHex(PROJECT.summary.defaultHeapSize):
            self.lineEdit_minHeapSize.setText(PROJECT.summary.defaultHeapSize)
        else:
            self.lineEdit_minHeapSize.setEnabled(False)

        # linker default stack size
        if Utils.isHex(PROJECT.defaultStackSize):
            self.lineEdit_minStackSize.setText(PROJECT.defaultStackSize)
        elif PROJECT.summary.defaultStackSize != "":
            self.lineEdit_minStackSize.setText(PROJECT.summary.defaultStackSize)
        else:
            self.lineEdit_minStackSize.setEnabled(False)

        # isCopyLibrary checkBox
        self.checkBox_isCopyLibrary.setChecked(PROJECT.copyLibrary)

        # useToolchainsPackage checkBox
        self.checkBox_useToolchainsPackage.setChecked(PROJECT.useToolchainsPackage)
        self.widget_toolchainsPackage.setEnabled(PROJECT.useToolchainsPackage)
        self.checkBox_useToolchainsPackage.stateChanged.connect(self.__on__checkBox_useToolchainsPackage__stateChanged)

        self.toolButton_packageManager.setIcon(Icon.BOX)
        self.toolButton_toolchainsManager.setIcon(Icon.BOX)

        # hal choose
        self.__hal_init()

        # builder choose
        self.__builder_init()

        self.setMinimumWidth(900)

    def __hal_init(self):
        hal = PROJECT.summary.hal
        versions = PACKAGE.hal.get(hal, {}).keys()
        if len(versions) != 0:
            self.comboBox_halVersion.addItems(versions)
            if PROJECT.halVersion == "":
                PROJECT.halVersion = self.comboBox_halVersion.currentText()
            else:
                if PROJECT.halVersion not in versions:
                    self.comboBox_halVersion.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The HAL package %1 is not installed.").replace(
                        "%1", f"{hal}@{PROJECT.halVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.comboBox_halVersion.setCurrentText(PROJECT.halVersion)
            self.lineEdit_halPath.setText(PROJECT.halPath)
        self.comboBox_halVersion.currentTextChanged.connect(self.__on__comboBox_halVersion__currentTextChanged)

    def __builder_init(self):
        builder = PROJECT.summary.builder
        builderList = builder.keys()
        if len(builderList) != 0:
            self.comboBox_builder.addItems(builderList)
            if PROJECT.builder == "":
                PROJECT.builder = self.comboBox_builder.currentText()
            else:
                if PROJECT.builder not in builderList:
                    self.comboBox_builder.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace("%1", PROJECT.builder)
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.comboBox_builder.setCurrentText(PROJECT.builder)
            # builder version choose
            self.__builderVersion_init(builder)
        self.comboBox_builder.currentTextChanged.connect(self.__on__comboBox_builder__currentTextChanged)

    def __builderVersion_init(self, builder: dict[str, dict[str, list[str]]]):
        builderVersion = builder.get(self.comboBox_builder.currentText(), {})
        builderVersionList = builderVersion.keys()
        if len(builderVersionList) != 0:
            self.comboBox_builderVersion.addItems(builderVersionList)
            if PROJECT.builderVersion == "":
                PROJECT.builderVersion = self.comboBox_builderVersion.currentText()
            else:
                if PROJECT.builderVersion not in builderVersionList:
                    self.comboBox_builderVersion.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace(
                        "%1", f"{self.comboBox_builder.currentText()}@{PROJECT.builderVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.comboBox_builderVersion.setCurrentText(PROJECT.builderVersion)
            # toolchains choose
            self.__toolchains_init(builderVersion)
        self.comboBox_builderVersion.currentTextChanged.connect(self.__on__comboBox_builderVersion__currentTextChanged)

    def __toolchains_init(self, builderVersion: dict[str, list[str]]):
        toolchains = builderVersion.get(self.comboBox_builderVersion.currentText(), {})
        if len(toolchains) != 0:
            self.comboBox_toolchains.addItems(toolchains)
            if PROJECT.toolchains == "":
                PROJECT.toolchains = self.comboBox_toolchains.currentText()
            else:
                if PROJECT.toolchains not in toolchains:
                    self.comboBox_toolchains.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace(
                        "%1", f"{self.comboBox_builder.currentText()}@{PROJECT.toolchains}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.comboBox_toolchains.setCurrentText(PROJECT.toolchains)
            # toolchains choose
            self.__toolchainsVersion_init()
        self.comboBox_toolchains.currentTextChanged.connect(self.__on__comboBox_toolchains__currentTextChanged)

    def __toolchainsVersion_init(self):
        toolchains = self.comboBox_toolchains.currentText()
        versions = PACKAGE.toolchains.get(toolchains, {}).keys()
        if len(versions) != 0:
            self.comboBox_toolchainsVersion.addItems(versions)
            if PROJECT.toolchainsVersion == "":
                PROJECT.toolchainsVersion = self.comboBox_toolchainsVersion.currentText()
            else:
                if PROJECT.toolchainsVersion not in versions:
                    self.comboBox_toolchainsVersion.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The toolchains package %1 is not installed.").replace(
                        "%1", f"{toolchains}@{PROJECT.toolchainsVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.comboBox_toolchainsVersion.setCurrentText(PROJECT.toolchainsVersion)
            self.lineEdit_toolchainsPath.setText(
                PACKAGE.path("toolchains", toolchains, self.comboBox_toolchainsVersion.currentText()))
        self.comboBox_toolchainsVersion.currentTextChanged.connect(
            self.__on__comboBox_toolchainsVersion__currentTextChanged)

    def __on__comboBox_builder__currentTextChanged(self, text: str):
        builderVersion = PROJECT.summary.builder.get(text, {})
        builderVersionList = builderVersion.keys()
        self.comboBox_builderVersion.clear()
        if len(builderVersionList) != 0:
            self.comboBox_builderVersion.addItems(builderVersionList)
        else:
            self.__on__comboBox_builderVersion__currentTextChanged("")

    def __on__comboBox_builderVersion__currentTextChanged(self, text: str):
        builderVersion = PROJECT.summary.builder.get(self.comboBox_builder.currentText(), {})
        toolchains = builderVersion.get(text, {})
        self.comboBox_toolchains.clear()
        if len(toolchains) != 0:
            self.comboBox_toolchains.addItems(toolchains)
        else:
            self.__on__comboBox_toolchains__currentTextChanged("")

    def __on__comboBox_toolchains__currentTextChanged(self, text: str):
        versions = PACKAGE.toolchains.get(text, {}).keys()
        self.comboBox_toolchainsVersion.clear()
        if len(versions) != 0:
            self.comboBox_toolchainsVersion.addItems(versions)
        else:
            self.__on__comboBox_toolchainsVersion__currentTextChanged("")

    def __on__comboBox_toolchainsVersion__currentTextChanged(self, text: str):
        self.lineEdit_toolchainsPath.setText(PACKAGE.path("toolchains", self.comboBox_toolchains.currentText(), text))

    def __on__comboBox_halVersion__currentTextChanged(self, text: str):
        self.lineEdit_halPath.setText(PACKAGE.path("hal", PROJECT.summary.hal, text))

    def __on__checkBox_useToolchainsPackage__stateChanged(self, state: int):
        self.widget_toolchainsPackage.setEnabled(state == Qt.CheckState.Checked)


class GenCodeDialog(MessageBoxBase):

    m_gen = False

    def __init__(self, parent=None, gen=False):
        super().__init__(parent)

        self.m_gen = gen

        self.main_widget = GenCodeDialogWidget(self)
        self.viewLayout.addWidget(self.main_widget)

        if gen:
            self.yesButton.setText(self.tr('Generate'))
        else:
            self.yesButton.setText(self.tr('Save'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.yesButton.disconnect(self)
        self.yesButton.clicked.connect(self.__onYesButtonClicked)

    def __showError(self, message: str):
        if not self.m_gen:
            return
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
        packagePath = self.main_widget.lineEdit_halPath.text()

        if not (self.main_widget.lineEdit_minHeapSize.isEnabled() and Utils.isHex(defaultHeapSize)):
            self.__showError(self.tr("The minimum heap size data is invalid"))
            return
        elif not (self.main_widget.lineEdit_minStackSize.isEnabled() and Utils.isHex(defaultStackSize)):
            self.__showError(self.tr("The minimum stack size data is invalid"))
            return
        elif self.main_widget.comboBox_halVersion.currentText() == "":
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
            PROJECT.halVersion = self.main_widget.comboBox_halVersion.currentText()

            if self.m_gen:
                coder = Coder()
                coder.generate(PROJECT.halPath)
            self.reject()
            self.rejected.emit()
