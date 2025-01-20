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
# @file        setting_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import os.path

from PySide6.QtCore import Qt, QUrl, QItemSelection
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QTreeWidgetItem, QStackedWidget
from loguru import logger
from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, PushSettingCard, HyperlinkCard,
                            PrimaryPushSettingCard, ScrollArea, ComboBoxSettingCard, ExpandLayout, FluentIconBase,
                            CustomColorSettingCard, setTheme, setThemeColor, InfoBar, ToolButton)

from common import (SETTINGS, Style, Icon, PROJECT, PACKAGE, SIGNAL_BUS, SUMMARY)
from utils import Converters
from widget import (LineEditPropertySettingCard, ComboBoxPropertySettingCard, SwitchPropertySettingCard,
                    ToolButtonPropertySettingCard)
from .ui.setting_view_ui import Ui_SettingView


class SystemSettingView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('SystemSettingView')

        # setting label
        self.settingLabel = QLabel(self.tr("System Setting"), self)
        self.settingLabel.setObjectName('settingLabel')
        self.settingLabel.move(36, 30)

        self.widgetScroll = QWidget()
        self.widgetScroll.setObjectName('widgetScroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widgetScroll)
        self.setWidgetResizable(True)

        self.groupFolders = self.__createFoldersGroup()
        self.groupStyle = self.__createPersonalizationGroup()
        self.groupSystem = self.__createSystemGroup()
        self.groupUpdate = self.__createUpdateGroup()
        self.groupAbout = self.__createAboutGroup()

        self.expandLayout = ExpandLayout(self.widgetScroll)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.groupFolders)
        self.expandLayout.addWidget(self.groupStyle)
        self.expandLayout.addWidget(self.groupSystem)
        self.expandLayout.addWidget(self.groupUpdate)
        self.expandLayout.addWidget(self.groupAbout)

        SETTINGS.appRestartSig.connect(self.__showRestartTooltip)
        self.enableTransparentBackground()

    def __createFoldersGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Folders Location"), self.widgetScroll)

        # ---------------------------------------------------------------------------------------------------------------
        self.packageFolderCard = PushSettingCard(self.tr('Choose folder'),
                                                 Icon.FOLDER,
                                                 self.tr("Package directory"),
                                                 SETTINGS.packageFolder.value,
                                                 group)
        self.packageFolderCard.clicked.connect(self.__on_repositoryFolderCard_clicked)
        # ---------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.packageFolderCard)

        return group

    def __createPersonalizationGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('Personalization'), self.widgetScroll)

        self.themeCard = OptionsSettingCard(SETTINGS.themeMode,
                                            Icon.PAINT,
                                            self.tr('Application theme'),
                                            self.tr("Change the appearance of your application"),
                                            texts=[self.tr('Light'),
                                                   self.tr('Dark'),
                                                   self.tr('Use system setting')],
                                            parent=group)
        self.themeCard.optionChanged.connect(lambda ci: setTheme(SETTINGS.get(ci)))

        self.themeColorCard = CustomColorSettingCard(SETTINGS.themeColor, Icon.PALETTE,
                                                     self.tr('Theme color'),
                                                     self.tr('Change the theme color of you application'),
                                                     group)
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))

        self.alertColorCard = CustomColorSettingCard(SETTINGS.alertColor, Icon.PALETTE,
                                                     self.tr('Alert color'),
                                                     self.tr('Change the alert color of you application'),
                                                     group)

        group.addSettingCard(self.themeCard)
        group.addSettingCard(self.themeColorCard)
        group.addSettingCard(self.alertColorCard)

        return group

    def __createSystemGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('System'), self.widgetScroll)

        self.languageCard = ComboBoxSettingCard(SETTINGS.language,
                                                Icon.GLOBAL,
                                                self.tr('Language'),
                                                self.tr('Set your preferred language for UI'),
                                                texts=['简体中文', '繁體中文', 'English',
                                                       self.tr('Use system setting')],
                                                parent=group)
        self.zoomCard = OptionsSettingCard(
            SETTINGS.dpiScale,
            Icon.PICTURE_IN_PICTURE,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=["100%", "125%", "150%", "175%", "200%", self.tr("Use system setting")],
            parent=group)
        self.useOpenGLCard = SwitchSettingCard(
            Icon.SPEED_UP,
            self.tr('Using opengl for acceleration'),
            self.tr('Hardware acceleration for your applications'),
            configItem=SETTINGS.isUseOpenGL,
            parent=group)
        self.openGLSamplesCard = OptionsSettingCard(
            icon=Icon.NUMBERS,
            title=self.tr('OpenGL samples'),
            content=self.tr('Set the preferred number of samples per pixel'),
            configItem=SETTINGS.openGLSamples,
            texts=['4', '8', '12', '16'],
            parent=group)

        group.addSettingCard(self.languageCard)
        group.addSettingCard(self.zoomCard)
        group.addSettingCard(self.useOpenGLCard)
        group.addSettingCard(self.openGLSamplesCard)

        return group

    def __createUpdateGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Software update"), self.widgetScroll)

        self.updateAtStartupCard = SwitchSettingCard(
            Icon.REFRESH,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=SETTINGS.isUpdateAtStartup,
            parent=group)

        group.addSettingCard(self.updateAtStartupCard)

        return group

    def __createAboutGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('About'), self.widgetScroll)

        self.helpCard = HyperlinkCard(SETTINGS.HELP_URL,
                                      self.tr('Open help page'), Icon.QUESTION,
                                      self.tr('Help'),
                                      self.tr('Discover new features and learn useful tips about CSP'),
                                      group)

        self.feedbackCard = PrimaryPushSettingCard(self.tr('Provide feedback'),
                                                   Icon.FEEDBACK,
                                                   self.tr('Provide feedback'),
                                                   self.tr('Help us improve CSP by providing feedback'),
                                                   group)
        self.feedbackCard.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(SETTINGS.FEEDBACK_URL)))

        self.aboutCard = PrimaryPushSettingCard(
            self.tr('Check update'), Icon.INFORMATION,
            self.tr('About'),
            f"© {self.tr('Copyright')} {SETTINGS.YEAR}, {SETTINGS.AUTHOR}. {self.tr('Version')} {SETTINGS.VERSION}",
            group)

        group.addSettingCard(self.helpCard)
        group.addSettingCard(self.feedbackCard)
        group.addSettingCard(self.aboutCard)

        return group

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(self.tr('Updated successfully'),
                        self.tr('Configuration takes effect after restart'),
                        duration=1500,
                        parent=self)

    def __on_repositoryFolderCard_clicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self,
                                                  self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.packageFolder) == folder:
            return

        SETTINGS.set(SETTINGS.packageFolder, folder)
        self.packageFolderCard.setContent(folder)


class GenerateSettingView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('GenerateSettingView')

        # setting label
        self.settingLabel = QLabel(self.tr("Generate Setting"), self)
        self.settingLabel.setObjectName('settingLabel')
        self.settingLabel.move(36, 30)

        self.widgetScroll = QWidget()
        self.widgetScroll.setObjectName('widgetScroll')

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widgetScroll)
        self.setWidgetResizable(True)

        self.linkerGroup = self.__createLinkerGroup()
        self.builderGroup = self.__createBuilderGroup()
        self.halGroup = self.__createHalGroup()

        self.expandLayout = ExpandLayout(self.widgetScroll)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)

        if self.linkerGroup is not None: self.expandLayout.addWidget(self.linkerGroup)
        if self.builderGroup is not None:
            self.expandLayout.addWidget(self.builderGroup)
            SIGNAL_BUS.packageUpdated.connect(self.__updateBuilderSettings)
            self.__updateBuilderSettings()
        if self.halGroup is not None:
            self.expandLayout.addWidget(self.halGroup)
            self.__updateHalSettings()

        self.enableTransparentBackground()

    def __createBuilderGroup(self) -> SettingCardGroup | None:
        # --------------------------------------------------------------------------------------------------------------
        if len(SUMMARY.projectSummary().builder.keys()) == 0:
            return None

        group = SettingCardGroup(self.tr("Builder Settings"), self.widgetScroll)

        # --------------------------------------------------------------------------------------------------------------
        self.builderComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.HAMMER,
                                                                           title=self.tr("Builder Tools"),
                                                                           value='',
                                                                           values=[],
                                                                           content=' ',
                                                                           parent=group)
        self.builderComboBoxGroupSettingCard.currentTextChanged.connect(
            self.__on_builderComboBoxGroupSettingCard_currentTextChanged)
        # --------------------------------------------------------------------------------------------------------------
        self.builderVersionComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.DATABASE_2,
                                                                                  title=self.tr("Builder Version"),
                                                                                  value='',
                                                                                  values=[],
                                                                                  content=' ',
                                                                                  parent=group)
        self.builderVersionComboBoxGroupSettingCard.currentTextChanged.connect(
            self.__on_builderVersionComboBoxGroupSettingCard_currentTextChanged)
        # --------------------------------------------------------------------------------------------------------------
        self.toolchainsComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.TOOLS,
                                                                              title=self.tr("Toolchains"),
                                                                              value='',
                                                                              values=[],
                                                                              content=' ',
                                                                              parent=group)
        self.toolchainsComboBoxGroupSettingCard.currentTextChanged.connect(
            self.__on_toolchainsComboBoxGroupSettingCard_currentTextChanged)
        # --------------------------------------------------------------------------------------------------------------
        self.useToolchainsPackageSwitchSettingCard = SwitchPropertySettingCard(
            icon=Icon.CHECKBOX_MULTIPLE,
            title=self.tr("Use Toolchains Package"),
            value=PROJECT.project().gen.useToolchainsPackage,
            content=self.tr("Use the built-in toolchain of this software"),
            parent=group)
        self.useToolchainsPackageSwitchSettingCard.checkedChanged.connect(
            self.__on_useToolchainsPackageSwitchSettingCard_checkedChanged)
        # --------------------------------------------------------------------------------------------------------------
        self.toolchainsVersionComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.DATABASE_2,
                                                                                     title=self.tr(
                                                                                         "Toolchains Version"),
                                                                                     value='',
                                                                                     values=[],
                                                                                     content=' ',
                                                                                     parent=group)
        count = self.toolchainsVersionComboBoxGroupSettingCard.hBoxLayout.count()
        self.toolchainsManagerBtn = ToolButton()
        self.toolchainsManagerBtn.setIcon(Icon.BOX)
        self.toolchainsVersionComboBoxGroupSettingCard.hBoxLayout.insertWidget(count - 2, self.toolchainsManagerBtn)
        self.toolchainsVersionComboBoxGroupSettingCard.hBoxLayout.insertSpacing(count - 1, 16)
        self.toolchainsVersionComboBoxGroupSettingCard.currentTextChanged.connect(
            self.__on_toolchainsVersionComboBoxGroupSettingCard_currentTextChanged)
        self.toolchainsManagerBtn.clicked.connect(self.__on_toolchainsManagerBtn_clicked)
        # --------------------------------------------------------------------------------------------------------------
        self.toolchainsPathToolButtonSettingCard = ToolButtonPropertySettingCard(icon=Icon.FOLDER,
                                                                                 title=self.tr("Toolchains Path"),
                                                                                 btnIcon=Icon.BOX,
                                                                                 content=' ',
                                                                                 parent=group)
        self.toolchainsPathToolButtonSettingCard.clicked.connect(self.__on_toolchainsPathToolButtonSettingCard_clicked)
        # --------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.builderComboBoxGroupSettingCard)
        group.addSettingCard(self.builderVersionComboBoxGroupSettingCard)
        group.addSettingCard(self.toolchainsComboBoxGroupSettingCard)
        group.addSettingCard(self.useToolchainsPackageSwitchSettingCard)
        group.addSettingCard(self.toolchainsVersionComboBoxGroupSettingCard)
        group.addSettingCard(self.toolchainsPathToolButtonSettingCard)

        if not PROJECT.project().gen.useToolchainsPackage:
            self.toolchainsVersionComboBoxGroupSettingCard.setEnabled(False)
            self.toolchainsPathToolButtonSettingCard.setEnabled(False)

        return group

    def __createLinkerGroup(self) -> SettingCardGroup | None:
        if PROJECT.project().gen.linker.defaultHeapSize > -1:
            defaultHeapSize = PROJECT.project().gen.linker.defaultHeapSize
        elif SUMMARY.projectSummary().linker.defaultHeapSize > -1:
            defaultHeapSize = SUMMARY.projectSummary().linker.defaultHeapSize
        else:
            defaultHeapSize = -1
        PROJECT.project().gen.linker.defaultHeapSize = defaultHeapSize
        # --------------------------------------------------------------------------------------------------------------
        if PROJECT.project().gen.linker.defaultStackSize > -1:
            defaultStackSize = PROJECT.project().gen.linker.defaultStackSize
        elif SUMMARY.projectSummary().linker.defaultStackSize > -1:
            defaultStackSize = SUMMARY.projectSummary().linker.defaultStackSize
        else:
            defaultStackSize = -1
        PROJECT.project().gen.linker.defaultStackSize = defaultStackSize
        # --------------------------------------------------------------------------------------------------------------

        group = SettingCardGroup(self.tr("Linker Settings"), self.widgetScroll)

        # --------------------------------------------------------------------------------------------------------------
        if defaultHeapSize > -1:
            self.defaultHeapLineEditCard = LineEditPropertySettingCard(icon=Icon.FOLDER,
                                                                       title=self.tr("Default Heap Size"),
                                                                       value=hex(defaultHeapSize),
                                                                       content=hex(defaultHeapSize),
                                                                       validator=R"(^0x[0-9A-Fa-f]+$)",
                                                                       parent=group)
            self.defaultHeapLineEditCard.textChanged.connect(self.__on_defaultHeapLineEditCard_textChanged)
            PROJECT.project().gen.linker.defaultHeapSizeChanged.connect(
                lambda old, new: self.defaultHeapLineEditCard.setContent(hex(new)))
            group.addSettingCard(self.defaultHeapLineEditCard)
        # --------------------------------------------------------------------------------------------------------------
        if defaultStackSize > -1:
            self.defaultStackLineEditCard = LineEditPropertySettingCard(icon=Icon.FOLDER,
                                                                        title=self.tr("Default Stack Size"),
                                                                        value=hex(defaultStackSize),
                                                                        content=hex(defaultStackSize),
                                                                        validator=R"(^0x[0-9A-Fa-f]+$)",
                                                                        parent=group)
            self.defaultStackLineEditCard.textChanged.connect(self.__on_defaultStackLineEditCard_textChanged)
            PROJECT.project().gen.linker.defaultStackSizeChanged.connect(
                lambda old, new: self.defaultStackLineEditCard.setContent(hex(new)))
            group.addSettingCard(self.defaultStackLineEditCard)

        return group

    def __createHalGroup(self) -> SettingCardGroup | None:
        # --------------------------------------------------------------------------------------------------------------

        group = SettingCardGroup(self.tr("Hal Settings"), self.widgetScroll)

        # --------------------------------------------------------------------------------------------------------------
        self.copyLibrarySwitchSettingCard = SwitchPropertySettingCard(icon=Icon.CHECKBOX_MULTIPLE,
                                                                      title=self.tr("Copy Hal Library"),
                                                                      value=PROJECT.project().gen.copyLibrary,
                                                                      content=self.tr(
                                                                          "Copy the hal library files to the project directory"),
                                                                      parent=group)
        self.copyLibrarySwitchSettingCard.checkedChanged.connect(
            self.__on_copyLibrarySwitchSettingCard_checkedChanged)
        # --------------------------------------------------------------------------------------------------------------
        self.halComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.HAMMER,
                                                                       title=self.tr("Hal Package"),
                                                                       value='',
                                                                       values=[],
                                                                       content=' ',
                                                                       parent=group)
        self.halComboBoxGroupSettingCard.currentTextChanged.connect(
            self.__on_halComboBoxGroupSettingCard_currentTextChanged)
        # --------------------------------------------------------------------------------------------------------------
        self.halVersionComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.DATABASE_2,
                                                                              title=self.tr("Hal Package Version"),
                                                                              value='',
                                                                              values=[],
                                                                              content=' ',
                                                                              parent=group)
        self.halVersionComboBoxGroupSettingCard.currentTextChanged.connect(
            self.__on_halVersionComboBoxGroupSettingCard_currentTextChanged)
        # --------------------------------------------------------------------------------------------------------------
        self.halPathToolButtonSettingCard = ToolButtonPropertySettingCard(icon=Icon.FOLDER,
                                                                          title=self.tr("Hal Package Path"),
                                                                          btnIcon=Icon.BOX,
                                                                          content=' ',
                                                                          parent=group)
        self.halPathToolButtonSettingCard.clicked.connect(self.__on_halPathToolButtonSettingCard_clicked)
        # --------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.copyLibrarySwitchSettingCard)
        group.addSettingCard(self.halComboBoxGroupSettingCard)
        group.addSettingCard(self.halVersionComboBoxGroupSettingCard)
        group.addSettingCard(self.halPathToolButtonSettingCard)

        return group

    def __on_defaultHeapLineEditCard_textChanged(self, text: str):
        ishex = Converters.ishex(text)
        if ishex:
            PROJECT.project().gen.defaultHeapSize = text
        self.defaultHeapLineEditCard.setStatusInfo(not ishex, self.tr("The Path is not directory"))

    def __on_defaultStackLineEditCard_textChanged(self, text: str):
        ishex = Converters.ishex(text)
        if ishex:
            PROJECT.project().gen.defaultStackSize = text
        self.defaultStackLineEditCard.setStatusInfo(not ishex, self.tr("The Path is not directory"))

    def __on_builderComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.builder = text
        self.__updateBuilderVersionSettings()

    def __on_builderVersionComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.builderVersion = text
        self.__updateToolchainsSettings()

    def __on_useToolchainsPackageSwitchSettingCard_checkedChanged(self, checked: bool):
        PROJECT.project().gen.useToolchainsPackage = checked
        self.toolchainsVersionComboBoxGroupSettingCard.setEnabled(checked)
        self.toolchainsPathToolButtonSettingCard.setEnabled(checked)
        if checked:
            self.__updateToolchainsVersionSettings()
        else:
            self.toolchainsVersionComboBoxGroupSettingCard.clear()
            self.toolchainsPathToolButtonSettingCard.clear()

    def __on_toolchainsComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.toolchains = text
        self.__updateToolchainsVersionSettings()

    def __on_toolchainsVersionComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.toolchainsVersion = text
        self.__updateToolchainsPathSettings()

    def __on_toolchainsManagerBtn_clicked(self):
        self.__navigationToPackageView()

    def __on_toolchainsPathToolButtonSettingCard_clicked(self):
        self.__navigationToPackageView()

    def __navigationToPackageView(self):
        SIGNAL_BUS.navigationRequested.emit('PackageView', "")

    def __updateBuilderSettings(self):
        if self.builderGroup is None:
            return

        builder = SUMMARY.projectSummary().builder
        builderList = list(builder.keys())
        if len(builderList) == 0:
            return

        if PROJECT.project().gen.builder == "":
            PROJECT.project().gen.builder = builderList[-1]
        else:
            if PROJECT.project().gen.builder not in builderList:
                logger.warning(
                    f"The builder {PROJECT.project().gen.builder} is not supported. Use default value {builderList[-1]!r}")
                PROJECT.project().gen.builder = builderList[-1]

        self.builderComboBoxGroupSettingCard.setSource(PROJECT.project().gen.builder, builderList)
        self.builderComboBoxGroupSettingCard.setContent(PROJECT.project().gen.builder)

    # noinspection DuplicatedCode
    def __updateBuilderVersionSettings(self):
        if self.builderGroup is None:
            return

        builderVersion = SUMMARY.projectSummary().builder.get(PROJECT.project().gen.builder, {})
        builderVersionList = list(builderVersion.keys())  # It must not be an empty array.

        if PROJECT.project().gen.builderVersion == "":
            PROJECT.project().gen.builderVersion = builderVersionList[-1]
        else:
            if PROJECT.project().gen.builderVersion not in builderVersionList:
                # logger.warning(
                #     f"The builder '{PROJECT.project().gen.builder}@{PROJECT.project().gen.builderVersion}' is not supported. Use default value '{PROJECT.project().gen.builder}@{builderVersionList[-1]}'")
                PROJECT.project().gen.builderVersion = builderVersionList[-1]

        self.builderVersionComboBoxGroupSettingCard.setSource(PROJECT.project().gen.builderVersion, builderVersionList)
        self.builderVersionComboBoxGroupSettingCard.setContent(PROJECT.project().gen.builder)

    def __updateToolchainsSettings(self):
        if self.builderGroup is None:
            return

        # It must not be an empty array.
        toolchains = SUMMARY.projectSummary().builder.get(PROJECT.project().gen.builder, {}).get(
            PROJECT.project().gen.builderVersion, {})
        if PROJECT.project().gen.toolchains == "":
            PROJECT.project().gen.toolchains = toolchains[-1]
        else:
            if PROJECT.project().gen.toolchains not in toolchains:
                # logger.warning(
                #     f"The builder '{PROJECT.project().gen.builder}@{PROJECT.project().gen.toolchains}' is not supported. Use default value '{PROJECT.project().gen.builder}@{toolchains[-1]}'")
                PROJECT.project().gen.toolchains = toolchains[-1]

        self.toolchainsComboBoxGroupSettingCard.setSource(PROJECT.project().gen.toolchains, toolchains)
        self.toolchainsComboBoxGroupSettingCard.setContent(PROJECT.project().gen.toolchains)

    def __updateToolchainsVersionSettings(self):
        if self.builderGroup is None or not PROJECT.project().gen.useToolchainsPackage:
            return

        toolchainsVersions = PACKAGE.index().versions('toolchains', PROJECT.project().gen.toolchains)
        if len(toolchainsVersions) != 0:
            if PROJECT.project().gen.toolchainsVersion == "":
                PROJECT.project().gen.toolchainsVersion = toolchainsVersions[-1]
            else:
                if PROJECT.project().gen.toolchainsVersion not in toolchainsVersions:
                    # logger.warning(
                    #     f"The toolchains '{PROJECT.project().gen.toolchains}@{PROJECT.project().gen.toolchainsVersion}' is not supported. Use default value '{PROJECT.project().gen.toolchains}@{toolchainsVersions[-1]}'")
                    PROJECT.project().gen.toolchainsVersion = toolchainsVersions[-1]
        else:
            logger.error(
                f"The toolchains {PROJECT.project().gen.toolchains!r} is not installed. Please install and then restart this software, You can find the corresponding package download URL here {SETTINGS.PACKAGE_LIST_URL!r}")
        self.toolchainsVersionComboBoxGroupSettingCard.setSource(PROJECT.project().gen.toolchainsVersion,
                                                                 toolchainsVersions)
        self.toolchainsVersionComboBoxGroupSettingCard.setContent(PROJECT.project().gen.toolchains)

    def __updateToolchainsPathSettings(self):
        if self.builderGroup is None or not PROJECT.project().gen.useToolchainsPackage:
            return

        toolchainsPath = PACKAGE.index().path("toolchains", PROJECT.project().gen.toolchains,
                                              PROJECT.project().gen.toolchainsVersion)

        self.toolchainsPathToolButtonSettingCard.setContent(toolchainsPath)
        self.toolchainsPathToolButtonSettingCard.contentLabel.setToolTip(toolchainsPath)
        if not os.path.isdir(toolchainsPath):
            message = self.tr("The Path is not directory")
            self.toolchainsPathToolButtonSettingCard.setStatusInfo(True, message)
        else:
            self.toolchainsPathToolButtonSettingCard.setStatusInfo(False, "")

    def __on_copyLibrarySwitchSettingCard_checkedChanged(self, checked: bool):
        PROJECT.project().gen.copyLibrary = checked

    def __on_halComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.hal = text
        self.__updateHalVersionSettings()

    def __on_halVersionComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.halVersion = text
        self.__updateHalPathSettings()

    def __on_halPathToolButtonSettingCard_clicked(self):
        self.__navigationToPackageView()

    def __updateHalSettings(self):
        if self.halGroup is None:
            return

        hals = SUMMARY.projectSummary().hals
        if len(hals) == 0:
            return

        if PROJECT.project().gen.hal == "":
            PROJECT.project().gen.hal = hals[-1]
        else:
            if PROJECT.project().gen.hal not in hals:
                logger.warning(
                    f"The hal {PROJECT.project().gen.hal!r} is not supported. Use default value {hals[-1]!r}")
                PROJECT.project().gen.hal = hals[-1]

        self.halComboBoxGroupSettingCard.setSource(PROJECT.project().gen.hal, hals)
        self.halComboBoxGroupSettingCard.setContent(PROJECT.project().gen.hal)

    def __updateHalVersionSettings(self):
        if self.halGroup is None:
            return

        halVersions = PACKAGE.index().versions('hal', PROJECT.project().gen.hal)
        if len(halVersions) != 0:
            if PROJECT.project().gen.halVersion == "":
                PROJECT.project().gen.halVersion = halVersions[-1]
            else:
                if PROJECT.project().gen.halVersion not in halVersions:
                    # logger.warning(
                    #     f"The hal '{PROJECT.project().gen.hal}@{PROJECT.project().gen.halVersion}' is not supported. Use default value '{PROJECT.project().gen.hal}@{halVersions[-1]}'")
                    PROJECT.project().gen.halVersion = halVersions[-1]
        else:
            logger.error(
                f"The hal {PROJECT.project().gen.hal!r} is not installed. Please install and then restart this software. You can find the corresponding package download URL here {SETTINGS.PACKAGE_LIST_URL!r}")

        self.halVersionComboBoxGroupSettingCard.setSource(PROJECT.project().gen.halVersion, halVersions)
        self.halVersionComboBoxGroupSettingCard.setContent(PROJECT.project().gen.halVersion)

    def __updateHalPathSettings(self):
        if self.halGroup is None:
            return

        halPath = PACKAGE.index().path("hal", PROJECT.project().gen.hal, PROJECT.project().gen.halVersion)

        self.halPathToolButtonSettingCard.setContent(halPath)
        self.halPathToolButtonSettingCard.contentLabel.setToolTip(halPath)
        if not os.path.isdir(halPath):
            message = self.tr("The Path is not directory")
            self.halPathToolButtonSettingCard.setStatusInfo(True, message)
        else:
            self.halPathToolButtonSettingCard.setStatusInfo(False, "")


class SettingView(Ui_SettingView, QWidget):
    __navigationViews = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.settingStackedWidget = QStackedWidget(self)
        self.settingStackedWidgetCardVerticalLayout.addWidget(self.settingStackedWidget)

        self.settingTreeCard.setFixedWidth(300)
        self.settingTree.header().setVisible(False)
        self.settingTree.selectionModel().selectionChanged.connect(self.__on_settingTree_selectionChanged)

        self.systemSettingView = SystemSettingView(self)
        self.generateSettingView = GenerateSettingView(self)

        self.systemSettingTreeWidgetItem = self.__addView(self.systemSettingView, Icon.LIST_SETTINGS,
                                                          self.tr("System Setting"))
        self.generateSettingTreeWidgetItem = self.__addView(self.generateSettingView, Icon.AI_GENERATE,
                                                            self.tr("Generate Setting"))

        Style.SETTING_VIEW.apply(self)

        self.settingTree.setCurrentItem(self.systemSettingTreeWidgetItem)

    def switchTo(self, key: str):
        if key not in self.__navigationViews:
            return

        self.settingTree.setCurrentItem(self.__navigationViews[key]['item'])

    def __addView(self, view: QWidget, icon: FluentIconBase, text: str) -> QTreeWidgetItem | None:
        if not view.objectName():
            raise ValueError("The object name of `view` can't be empty string.")

        if view.objectName() in self.__navigationViews:
            return None

        item = QTreeWidgetItem([text])
        item.setIcon(0, icon.icon())
        item.setData(0, Qt.ItemDataRole.StatusTipRole, view.objectName())
        self.settingTree.addTopLevelItem(item)

        self.settingStackedWidget.addWidget(view)

        self.__navigationViews[view.objectName()] = {'view': view, 'item': item}

        return item

    def __on_settingTree_selectionChanged(self, selected: QItemSelection, _: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            key = index.data(Qt.ItemDataRole.StatusTipRole)
            self.settingStackedWidget.setCurrentWidget(self.__navigationViews[key]['view'])
