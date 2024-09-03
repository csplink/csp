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
from common import PROJECT, PACKAGE, Coder, Icon
from utils import converters


class GenCodeDialogWidget(Ui_GenCodeDialog, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.lineedit_min_heap_size.setValidator(QRegularExpressionValidator(QRegularExpression(R"(^0x[0-9A-Fa-f]+$)")))
        self.lineedit_min_stack_size.setValidator(QRegularExpressionValidator(
            QRegularExpression(R"(^0x[0-9A-Fa-f]+$)")))

        # linker default heap size
        if converters.ishex(PROJECT.default_heap_size):
            self.lineedit_min_heap_size.setText(PROJECT.default_heap_size)
        elif converters.ishex(PROJECT.summary.default_heap_size):
            self.lineedit_min_heap_size.setText(PROJECT.summary.default_heap_size)
        else:
            self.lineedit_min_heap_size.setEnabled(False)

        # linker default stack size
        if converters.ishex(PROJECT.default_stack_size):
            self.lineedit_min_stack_size.setText(PROJECT.default_stack_size)
        elif PROJECT.summary.default_stack_size != "":
            self.lineedit_min_stack_size.setText(PROJECT.summary.default_stack_size)
        else:
            self.lineedit_min_stack_size.setEnabled(False)

        # isCopyLibrary checkBox
        self.checkbox_is_copy_library.setChecked(PROJECT.copy_library)

        # useToolchainsPackage checkBox
        self.checkbox_use_toolchains_package.setChecked(PROJECT.use_toolchains_package)
        self.widget_toolchains_package.setEnabled(PROJECT.use_toolchains_package)
        self.checkbox_use_toolchains_package.stateChanged.connect(
            self.__on_checkbox_use_toolchains_package_state_changed)

        self.btn_package_manager.setIcon(Icon.BOX)
        self.btn_toolchains_manager.setIcon(Icon.BOX)

        self.lineedit_hal_path.textChanged.connect(self.__on_lineedit_hal_path_text_changed)
        self.lineedit_toolchains_path.textChanged.connect(self.__on_lineedit_toolchains_path_text_changed)

        # hal choose
        self.__hal_init()

        # builder choose
        self.__builder_init()

        self.setMinimumWidth(600)

    def __hal_init(self):
        hal = PROJECT.summary.hal
        versions = PACKAGE.hal.get(hal, {}).keys()
        if len(versions) != 0:
            self.combobox_hal_version.addItems(versions)
            if PROJECT.hal_version == "":
                PROJECT.hal_version = self.combobox_hal_version.currentText()
            else:
                if PROJECT.hal_version not in versions:
                    self.combobox_hal_version.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The HAL package %1 is not installed.").replace(
                        "%1", f"{hal}@{PROJECT.hal_version}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.combobox_hal_version.setCurrentText(PROJECT.hal_version)
            self.lineedit_hal_path.setText(PROJECT.hal_path)
        self.combobox_hal_version.currentTextChanged.connect(self.__on_combobox_hal_version_current_text_changed)

    def __builder_init(self):
        builder = PROJECT.summary.builder
        builderList = builder.keys()
        if len(builderList) != 0:
            self.combobox_builder.addItems(builderList)
            if PROJECT.builder == "":
                PROJECT.builder = self.combobox_builder.currentText()
            else:
                if PROJECT.builder not in builderList:
                    self.combobox_builder.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace("%1", PROJECT.builder)
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.combobox_builder.setCurrentText(PROJECT.builder)
            # builder version choose
            self.__builder_version_init(builder)
        self.combobox_builder.currentTextChanged.connect(self.__on_combobox_builder_current_text_changed)

    def __builder_version_init(self, builder: dict[str, dict[str, list[str]]]):
        builderVersion = builder.get(self.combobox_builder.currentText(), {})
        builderVersionList = builderVersion.keys()
        if len(builderVersionList) != 0:
            self.combobox_builder_version.addItems(builderVersionList)
            if PROJECT.builder_version == "":
                PROJECT.builder_version = self.combobox_builder_version.currentText()
            else:
                if PROJECT.builder_version not in builderVersionList:
                    self.combobox_builder_version.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace(
                        "%1", f"{self.combobox_builder.currentText()}@{PROJECT.builder_version}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.combobox_builder_version.setCurrentText(PROJECT.builder_version)
            # toolchains choose
            self.__toolchains_init(builderVersion)
        self.combobox_builder_version.currentTextChanged.connect(
            self.__on_combobox_builder_version_current_text_changed)

    def __toolchains_init(self, builderVersion: dict[str, list[str]]):
        toolchains = builderVersion.get(self.combobox_builder_version.currentText(), {})
        if len(toolchains) != 0:
            self.combobox_toolchains.addItems(toolchains)
            if PROJECT.toolchains == "":
                PROJECT.toolchains = self.combobox_toolchains.currentText()
            else:
                if PROJECT.toolchains not in toolchains:
                    self.combobox_toolchains.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The builder %1 is not supported.").replace(
                        "%1", f"{self.combobox_builder.currentText()}@{PROJECT.toolchains}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.combobox_toolchains.setCurrentText(PROJECT.toolchains)
            # toolchains choose
            self.__toolchains_version_init()
        self.combobox_toolchains.currentTextChanged.connect(self.__on_combobox_toolchains_current_text_changed)

    def __toolchains_version_init(self):
        toolchains = self.combobox_toolchains.currentText()
        versions = PACKAGE.toolchains.get(toolchains, {}).keys()
        if len(versions) != 0:
            self.combobox_toolchains_version.addItems(versions)
            if PROJECT.toolchainsVersion == "":
                PROJECT.toolchainsVersion = self.combobox_toolchains_version.currentText()
            else:
                if PROJECT.toolchainsVersion not in versions:
                    self.combobox_toolchains_version.setCurrentIndex(-1)
                    title = self.tr('Warning')
                    content = self.tr("The toolchains package %1 is not installed.").replace(
                        "%1", f"{toolchains}@{PROJECT.toolchainsVersion}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.exec()
                else:
                    self.combobox_toolchains_version.setCurrentText(PROJECT.toolchainsVersion)
            self.lineedit_toolchains_path.setText(
                PACKAGE.path("toolchains", toolchains, self.combobox_toolchains_version.currentText()))
        self.combobox_toolchains_version.currentTextChanged.connect(
            self.__on_combobox_toolchains_version_current_text_changed)

    def __on_combobox_builder_current_text_changed(self, text: str):
        builderVersion = PROJECT.summary.builder.get(text, {})
        builderVersionList = builderVersion.keys()
        self.combobox_builder_version.clear()
        if len(builderVersionList) != 0:
            self.combobox_builder_version.addItems(builderVersionList)
        else:
            self.__on_combobox_builder_version_current_text_changed("")

    def __on_combobox_builder_version_current_text_changed(self, text: str):
        builderVersion = PROJECT.summary.builder.get(self.combobox_builder.currentText(), {})
        toolchains = builderVersion.get(text, {})
        self.combobox_toolchains.clear()
        if len(toolchains) != 0:
            self.combobox_toolchains.addItems(toolchains)
        else:
            self.__on_combobox_toolchains_current_text_changed("")

    def __on_combobox_toolchains_current_text_changed(self, text: str):
        versions = PACKAGE.toolchains.get(text, {}).keys()
        self.combobox_toolchains_version.clear()
        if len(versions) != 0:
            self.combobox_toolchains_version.addItems(versions)
        else:
            self.__on_combobox_toolchains_version_current_text_changed("")

    def __on_combobox_toolchains_version_current_text_changed(self, text: str):
        self.lineedit_toolchains_path.setText(PACKAGE.path("toolchains", self.combobox_toolchains.currentText(), text))

    def __on_combobox_hal_version_current_text_changed(self, text: str):
        self.lineedit_hal_path.setText(PACKAGE.path("hal", PROJECT.summary.hal, text))

    def __on_checkbox_use_toolchains_package_state_changed(self, state: int):
        self.widget_toolchains_package.setEnabled(state == Qt.CheckState.Checked)

    def __on_lineedit_hal_path_text_changed(self, text: str):
        if not os.path.isdir(self.lineedit_hal_path.text()):
            self.label_hal_folder_invalid.show()
        else:
            self.label_hal_folder_invalid.hide()

    def __on_lineedit_toolchains_path_text_changed(self, text: str):
        if not os.path.isdir(self.lineedit_toolchains_path.text()):
            self.label_toolchains_folder_invalid.show()
        else:
            self.label_toolchains_folder_invalid.hide()


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
        defaultHeapSize = self.main_widget.lineedit_min_heap_size.text()
        defaultStackSize = self.main_widget.lineedit_min_stack_size.text()
        isCopyLibrary = self.main_widget.checkbox_is_copy_library.isChecked()
        packagePath = self.main_widget.lineedit_hal_path.text()

        if not (self.main_widget.lineedit_min_heap_size.isEnabled() and converters.ishex(defaultHeapSize)):
            self.__showError(self.tr("The minimum heap size data is invalid"))
            return
        elif not (self.main_widget.lineedit_min_stack_size.isEnabled() and converters.ishex(defaultStackSize)):
            self.__showError(self.tr("The minimum stack size data is invalid"))
            return
        elif self.main_widget.combobox_hal_version.currentText() == "":
            self.__showError(self.tr("Please select a valid package version"))
            return
        elif not os.path.isdir(packagePath):
            error = self.tr("'%1' is not directory! maybe '%2' not yet installed.").replace("%1", packagePath).replace(
                "%2", f"{hal}@{PROJECT.hal_version}")
            self.__showError(error)
            return
        else:
            PROJECT.default_heap_size = defaultHeapSize
            PROJECT.default_stack_size = defaultStackSize
            PROJECT.copy_library = isCopyLibrary
            PROJECT.hal_version = self.main_widget.combobox_hal_version.currentText()

            if self.m_gen:
                coder = Coder()
                coder.generate(PROJECT.hal_path)
            self.reject()
            self.rejected.emit()
