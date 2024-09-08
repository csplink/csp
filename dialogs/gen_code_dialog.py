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
from PySide6.QtWidgets import QWidget, QListWidgetItem

from qfluentwidgets import (MessageBoxBase, Flyout, InfoBarIcon, MessageBox, IconInfoBadge, InfoBadgePosition,
                            CaptionLabel)
from qfluentwidgets import FluentIcon as FIF

from .ui.ui_gen_code_dialog import Ui_GenCodeDialog
from common import PROJECT, PACKAGE, Coder, Icon
from utils import converters


class GenCodeDialogWidget(Ui_GenCodeDialog, QWidget):

    __toolchainsPathLineEditIconInfoBadge = None
    __halPathLineEditIconInfoBadge = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.splitter.setSizes([100, 300])

        self.__toolchainsPathLineEditIconInfoBadge = self.__setErrorState(self.__toolchainsPathLineEditIconInfoBadge,
                                                                          self.toolchainsPathLineEdit,
                                                                          self.tr("The Path is not directory"))
        self.__halPathLineEditIconInfoBadge = self.__setErrorState(self.__halPathLineEditIconInfoBadge,
                                                                   self.halPathLineEdit,
                                                                   self.tr("The Path is not directory"))

        self.__settingListInit()
        self.__builderSettingInit()
        self.__linkerSettingInit()
        self.__packageSettingInit()

    def __settingListInit(self):
        self.settingStackedMap = {
            self.tr("Builder Settings"): {
                "index": 0,
                "errorCount": 0,
            },
            self.tr("Linker Settings"): {
                "index": 1,
                "errorCount": 0,
            },
            self.tr("Package Settings"): {
                "index": 2,
                "errorCount": 0,
            },
        }

        for key in self.settingStackedMap.keys():
            item = QListWidgetItem(key)
            self.settingList.addItem(item)
        item.setIcon(FIF.CANCEL_MEDIUM.icon())

        # self.settingList.currentTextChanged.connect(self.__on_settingList_currentTextChanged)

        self.settingList.setCurrentRow(0)

    def __builderSettingInit(self):
        self.useToolchainsPackageCheckbox.setChecked(PROJECT.useToolchainsPackage)

        self.useToolchainsPackageCheckbox.stateChanged.connect(self.__on_useToolchainsPackageCheckbox_stateChanged)

        self.toolchainsManagerBtn.setIcon(Icon.BOX)
        self.__builderInit()

    def __builderInit(self):
        builder = PROJECT.summary.builder
        builderList = builder.keys()
        if len(builderList) != 0:
            self.builderComboBox.addItems(builderList)
            if PROJECT.builder == "":
                PROJECT.builder = self.builderComboBox.currentText()
            else:
                if PROJECT.builder not in builderList:
                    self.builderComboBox.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace("%1", PROJECT.builder)
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.builderComboBox.setCurrentText(PROJECT.builder)
            # builder version choose
            self.__builderVersionInit(builder)
        self.builderComboBox.currentTextChanged.connect(self.__on_builderComboBox_currentTextChanged)

    def __builderVersionInit(self, builder: dict[str, dict[str, list[str]]]):
        builderVersion = builder.get(self.builderComboBox.currentText(), {})
        builderVersionList = builderVersion.keys()
        if len(builderVersionList) != 0:
            self.builderVersionComboBox.addItems(builderVersionList)
            if PROJECT.builderVersion == "":
                PROJECT.builderVersion = self.builderVersionComboBox.currentText()
            else:
                if PROJECT.builderVersion not in builderVersionList:
                    self.builderVersionComboBox.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace(
                        "%1", f"{self.builderComboBox.currentText()}@{PROJECT.builderVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.builderVersionComboBox.setCurrentText(PROJECT.builderVersion)
            # toolchains choose
            self.__toolchainsInit(builderVersion)
        self.builderVersionComboBox.currentTextChanged.connect(self.__on_builderVersionComboBox_currentTextChanged)

    def __toolchainsInit(self, builderVersion: dict[str, list[str]]):
        toolchains = builderVersion.get(self.builderVersionComboBox.currentText(), {})
        if len(toolchains) != 0:
            self.toolchainsCombobox.addItems(toolchains)
            if PROJECT.toolchains == "":
                PROJECT.toolchains = self.toolchainsCombobox.currentText()
            else:
                if PROJECT.toolchains not in toolchains:
                    self.toolchainsCombobox.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace(
                        "%1", f"{self.builderComboBox.currentText()}@{PROJECT.toolchains}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.toolchainsCombobox.setCurrentText(PROJECT.toolchains)
            # toolchains choose
            self.__toolchainsVersionInit()
        self.toolchainsCombobox.currentTextChanged.connect(self.__on_toolchainsCombobox_currentTextChanged)

    def __toolchainsVersionInit(self):
        toolchains = self.toolchainsCombobox.currentText()
        versions = PACKAGE.toolchains.get(toolchains, {}).keys()
        if len(versions) != 0:
            self.toolchainsVersionComboBox.addItems(versions)
            if PROJECT.toolchainsVersion == "":
                PROJECT.toolchainsVersion = self.toolchainsVersionComboBox.currentText()
            else:
                if PROJECT.toolchainsVersion not in versions:
                    self.toolchainsVersionComboBox.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The toolchains package %1 is not installed.").replace(
                        "%1", f"{toolchains}@{PROJECT.toolchainsVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.toolchainsVersionComboBox.setCurrentText(PROJECT.toolchainsVersion)
            self.toolchainsPathLineEdit.textChanged.connect(self.__on_toolchainsPathLineEdit_text_changed)
            self.toolchainsPathLineEdit.setText(
                PACKAGE.path("toolchains", toolchains, self.toolchainsVersionComboBox.currentText()))
        self.toolchainsVersionComboBox.currentTextChanged.connect(
            self.__on_toolchainsVersionComboBox_currentTextChanged)

    def __linkerSettingInit(self):
        self.minHeapLineEdit.setValidator(QRegularExpressionValidator(QRegularExpression(R"(^0x[0-9A-Fa-f]+$)")))
        self.minStackLineEdit.setValidator(QRegularExpressionValidator(QRegularExpression(R"(^0x[0-9A-Fa-f]+$)")))

        # linker default heap size
        if converters.ishex(PROJECT.defaultHeapSize):
            self.minHeapLineEdit.setText(PROJECT.defaultHeapSize)
        elif converters.ishex(PROJECT.summary.defaultHeapSize):
            self.minHeapLineEdit.setText(PROJECT.summary.defaultHeapSize)
        else:
            self.minHeapLineEdit.setEnabled(False)

        # linker default stack size
        if converters.ishex(PROJECT.defaultStackSize):
            self.minStackLineEdit.setText(PROJECT.defaultStackSize)
        elif PROJECT.summary.defaultStackSize != "":
            self.minStackLineEdit.setText(PROJECT.summary.defaultStackSize)
        else:
            self.minStackLineEdit.setEnabled(False)

    def __packageSettingInit(self):
        self.copyLibraryCheckbox.setChecked(PROJECT.copyLibrary)
        self.packageManagerBtn.setIcon(Icon.BOX)

        hal = PROJECT.summary.hal
        versions = PACKAGE.hal.get(hal, {}).keys()
        if len(versions) != 0:
            self.halVersionComboBox.addItems(versions)
            if PROJECT.halVersion == "":
                PROJECT.halVersion = self.halVersionComboBox.currentText()
            else:
                if PROJECT.halVersion not in versions:
                    self.halVersionComboBox.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The HAL package %1 is not installed.").replace(
                        "%1", f"{hal}@{PROJECT.halVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.halVersionComboBox.setCurrentText(PROJECT.halVersion)
            self.halPathLineEdit.textChanged.connect(self.__on_halPathLineEdit_textChanged)
            self.halPathLineEdit.setText(PROJECT.halDir)
        self.halVersionComboBox.currentTextChanged.connect(self.__on_halVersionComboBox_currentTextChanged)

    def __on_builderComboBox_currentTextChanged(self, text: str):
        builderVersion = PROJECT.summary.builder.get(text, {})
        builderVersionList = builderVersion.keys()
        self.builderVersionComboBox.clear()
        if len(builderVersionList) != 0:
            self.builderVersionComboBox.addItems(builderVersionList)
        else:
            self.__on_builderVersionComboBox_currentTextChanged("")

    def __on_builderVersionComboBox_currentTextChanged(self, text: str):
        builderVersion = PROJECT.summary.builder.get(self.builderComboBox.currentText(), {})
        toolchains = builderVersion.get(text, {})
        self.toolchainsCombobox.clear()
        if len(toolchains) != 0:
            self.toolchainsCombobox.addItems(toolchains)
        else:
            self.__on_toolchainsCombobox_currentTextChanged("")

    def __on_toolchainsCombobox_currentTextChanged(self, text: str):
        versions = PACKAGE.toolchains.get(text, {}).keys()
        self.toolchainsVersionComboBox.clear()
        if len(versions) != 0:
            self.toolchainsVersionComboBox.addItems(versions)
        else:
            self.__on_toolchainsVersionComboBox_currentTextChanged("")

    def __on_toolchainsVersionComboBox_currentTextChanged(self, text: str):
        self.toolchainsPathLineEdit.setText(PACKAGE.path("toolchains", self.toolchainsCombobox.currentText(), text))

    def __on_halVersionComboBox_currentTextChanged(self, text: str):
        self.halPathLineEdit.setText(PACKAGE.path("hal", PROJECT.summary.hal, text))

    def __on_useToolchainsPackageCheckbox_stateChanged(self, state: int):
        self.widget_toolchains_package.setEnabled(state == Qt.CheckState.Checked.value)

    def __on_halPathLineEdit_textChanged(self, text: str):
        if not os.path.isdir(text):
            message = self.tr("The Path is not directory")
        else:
            message = ""
        self.__halPathLineEditIconInfoBadge = self.__setErrorState(self.__halPathLineEditIconInfoBadge,
                                                                   self.halPathLineEdit, message)

    def __on_toolchainsPathLineEdit_text_changed(self, text: str):
        if not os.path.isdir(text):
            message = self.tr("The Path is not directory")
        else:
            message = ""
        self.__toolchainsPathLineEditIconInfoBadge = self.__setErrorState(self.__toolchainsPathLineEditIconInfoBadge,
                                                                          self.toolchainsPathLineEdit, message)

    def __on_settingList_currentTextChanged(self, text: str):
        self.settingStackedWidget.setCurrentIndex(self.settingStackedMap[text]["index"])

    def __setErrorState(self, infoBadge, target: QWidget, message: str):
        if message != "":
            if infoBadge == None:
                infoBadge = IconInfoBadge.error(icon=FIF.CANCEL_MEDIUM,
                                                parent=target.parent(),
                                                target=target,
                                                position=InfoBadgePosition.TOP_RIGHT)
                target.setToolTip(message)
        else:
            if infoBadge != None:
                infoBadge.deleteLater()
                infoBadge.hide()
                infoBadge = None
        return infoBadge


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
        defaultHeapSize = self.main_widget.minHeapLineEdit.text()
        defaultStackSize = self.main_widget.minStackLineEdit.text()
        isCopyLibrary = self.main_widget.copyLibraryCheckbox.isChecked()
        packagePath = self.main_widget.halPathLineEdit.text()

        if not (self.main_widget.minHeapLineEdit.isEnabled() and converters.ishex(defaultHeapSize)):
            self.__showError(self.tr("The minimum heap size data is invalid"))
            return
        elif not (self.main_widget.minStackLineEdit.isEnabled() and converters.ishex(defaultStackSize)):
            self.__showError(self.tr("The minimum stack size data is invalid"))
            return
        elif self.main_widget.halVersionComboBox.currentText() == "":
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
            PROJECT.halVersion = self.main_widget.halVersionComboBox.currentText()

            if self.m_gen:
                coder = Coder()
                coder.generate(PROJECT.halDir)
            self.reject()
            self.rejected.emit()
