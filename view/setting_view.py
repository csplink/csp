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

from PySide6.QtCore import Qt, QUrl, QItemSelection
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QTreeWidgetItem

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, PushSettingCard, HyperlinkCard,
                            PrimaryPushSettingCard, ScrollArea, ComboBoxSettingCard, ExpandLayout, FluentIconBase,
                            CustomColorSettingCard, setTheme, setThemeColor, InfoBar, MessageBox, ToolButton)

from .ui.ui_setting_view import Ui_SettingView

from common import (SETTINGS, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR, Style, Icon, PROJECT, PACKAGE,
                    PACKAGE_LIST_URL)
from utils import converters
from widget import (LineEditPropertySettingCard, ComboBoxPropertySettingCard, SwitchPropertySettingCard,
                    ToolButtonPropertySettingCard)


class SystemSettingView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

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

        #---------------------------------------------------------------------------------------------------------------
        self.databaseFolderCard = PushSettingCard(self.tr('Choose folder'), Icon.FOLDER, self.tr("Database directory"),
                                                  SETTINGS.databaseFolder.value, group)
        self.databaseFolderCard.clicked.connect(self.__on_databaseFolderCard_clicked)
        #---------------------------------------------------------------------------------------------------------------
        self.repositoryFolderCard = PushSettingCard(self.tr('Choose folder'), Icon.FOLDER,
                                                    self.tr("Repository directory"), SETTINGS.repositoryFolder.value,
                                                    group)
        self.repositoryFolderCard.clicked.connect(self.__on_repositoryFolderCard_clicked)
        #---------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.databaseFolderCard)
        group.addSettingCard(self.repositoryFolderCard)

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

        self.themeColorCard = CustomColorSettingCard(SETTINGS.themeColor, Icon.PALETTE, self.tr('Theme color'),
                                                     self.tr('Change the theme color of you application'), group)
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))

        self.alertColorCard = CustomColorSettingCard(SETTINGS.alertColor, Icon.PALETTE, self.tr('Alert color'),
                                                     self.tr('Change the alert color of you application'), group)

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
            texts=["100%", "125%", "150%", "175%", "200%",
                   self.tr("Use system setting")],
            parent=group)

        group.addSettingCard(self.languageCard)
        group.addSettingCard(self.zoomCard)

        return group

    def __createUpdateGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Software update"), self.widgetScroll)

        self.updateAtStartupCard = SwitchSettingCard(
            Icon.REFRESH,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=SETTINGS.checkUpdateAtStartup,
            parent=group)

        group.addSettingCard(self.updateAtStartupCard)

        return group

    def __createAboutGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('About'), self.widgetScroll)

        self.helpCard = HyperlinkCard(HELP_URL, self.tr('Open help page'), Icon.QUESTION, self.tr('Help'),
                                      self.tr('Discover new features and learn useful tips about csp'), group)

        self.feedbackCard = PrimaryPushSettingCard(self.tr('Provide feedback'), Icon.FEEDBACK,
                                                   self.tr('Provide feedback'),
                                                   self.tr('Help us improve csp by providing feedback'), group)
        self.feedbackCard.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))

        self.aboutCard = PrimaryPushSettingCard(
            self.tr('Check update'), Icon.INFORMATION, self.tr('About'),
            f"© {self.tr('Copyright')} {YEAR}, {AUTHOR}. {self.tr('Version')} {VERSION}", group)

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

    def __on_databaseFolderCard_clicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.databaseFolder) == folder:
            return

        SETTINGS.set(SETTINGS.databaseFolder, folder)
        self.databaseFolderCard.setContent(folder)

    def __on_repositoryFolderCard_clicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.repositoryFolder) == folder:
            return

        SETTINGS.set(SETTINGS.repositoryFolder, folder)
        self.repositoryFolderCard.setContent(folder)


class GenerateSettingView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # setting label
        self.settingLabel = QLabel(self.tr("Generate Setting"), self)
        self.settingLabel.setObjectName('settingLabel')
        self.settingLabel.move(36, 30)

        self.widgetScroll = QWidget()
        self.widgetScroll.setObjectName('widgetScroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widgetScroll)
        self.setWidgetResizable(True)

        self.groupLinker = self.__createLinkerGroup()
        self.groupBuilder = self.__createBuilderGroup()

        self.expandLayout = ExpandLayout(self.widgetScroll)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)

        if self.groupLinker != None: self.expandLayout.addWidget(self.groupLinker)
        if self.groupBuilder != None: self.expandLayout.addWidget(self.groupBuilder)

        self.enableTransparentBackground()

    def __createBuilderGroup(self) -> SettingCardGroup:
        #---------------------------------------------------------------------------------------------------------------
        builder = PROJECT.summary.builder
        builderList = builder.keys()
        if len(builderList) == 0:
            return None

        if PROJECT.builder == "":
            PROJECT.builder = builderList[0]
        else:
            if PROJECT.builder not in builderList:
                title = self.tr('Warning')
                content = self.tr("The builder %1 is not supported. Use default value '%2'").replace(
                    "%1", PROJECT.builder).replace("%2", builderList[0])
                message = MessageBox(title, content, self.window())
                message.setContentCopyable(True)
                message.raise_()
                message.exec()
                PROJECT.builder = builderList[0]
        #-----------------------------------------------------------------------
        builderVersion = builder.get(PROJECT.builder, {})
        builderVersionList = builderVersion.keys()  # It must not be an empty array.

        if PROJECT.builderVersion == "":
            PROJECT.builderVersion = builderVersionList[0]
        else:
            if PROJECT.builderVersion not in builderVersionList:
                title = self.tr('Warning')
                content = self.tr("The builder %1 is not supported. Use default value '%2'").replace(
                    "%1", f"{PROJECT.builderVersion}@{PROJECT.builderVersion}").replace(
                        "%2", f"{PROJECT.builderVersion}@{builderVersionList[0]}")
                message = MessageBox(title, content, self.window())
                message.setContentCopyable(True)
                message.raise_()
                message.exec()
                PROJECT.builderVersion = builderVersionList[0]
        #-----------------------------------------------------------------------
        toolchains = builderVersion.get(PROJECT.builderVersion, {})  # It must not be an empty array.
        if PROJECT.toolchains == "":
            PROJECT.toolchains = toolchains[0]
        else:
            if PROJECT.toolchains not in toolchains:
                title = self.tr('Warning')
                content = self.tr("The builder %1 is not supported. Use default value '%2'").replace(
                    "%1", f"{PROJECT.builder}@{PROJECT.toolchains}").replace("%2", f"{PROJECT.builder}@{toolchains[0]}")
                message = MessageBox(title, content, self.window())
                message.setContentCopyable(True)
                message.raise_()
                message.exec()
                PROJECT.toolchains = toolchains[0]
        #-----------------------------------------------------------------------
        toolchainsVersions = PACKAGE.toolchains.get(PROJECT.toolchains, {}).keys()
        if len(toolchainsVersions) != 0:
            if PROJECT.toolchainsVersion == "":
                PROJECT.toolchainsVersion = toolchainsVersions[0]
            else:
                if PROJECT.toolchainsVersion not in toolchainsVersions:
                    title = self.tr('Warning')
                    content = self.tr("The toolchains %1 is not supported. Use default value '%2'").replace(
                        "%1", f"{PROJECT.toolchains}@{PROJECT.toolchainsVersion}").replace(
                            "%2", f"{PROJECT.toolchains}@{toolchainsVersions[0]}")
                    message = MessageBox(title, content, self.window())
                    message.setContentCopyable(True)
                    message.raise_()
                    message.exec()
                    PROJECT.toolchainsVersion = toolchainsVersions[0]
        else:
            title = self.tr('Error')
            content = self.tr(
                "The toolchains %1 is not installed. Please install and then restart this software.").replace(
                    "%1", PROJECT.toolchains)
            message = MessageBox(title, content, self.window())
            message.setContentCopyable(True)
            message.raise_()
            if message.exec():
                QDesktopServices.openUrl(QUrl(PACKAGE_LIST_URL))

        #---------------------------------------------------------------------------------------------------------------

        group = SettingCardGroup(self.tr("Builder Settings"), self.widgetScroll)

        #---------------------------------------------------------------------------------------------------------------
        self.builderComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.HAMMER,
                                                                           title=self.tr("Builder Tools"),
                                                                           value=PROJECT.builder,
                                                                           values=builderList,
                                                                           content=PROJECT.builder,
                                                                           parent=group)
        #---------------------------------------------------------------------------------------------------------------
        self.builderVersionComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.DATABASE_2,
                                                                                  title=self.tr("Builder Version"),
                                                                                  value=PROJECT.builderVersion,
                                                                                  values=builderVersionList,
                                                                                  content=PROJECT.builderVersion,
                                                                                  parent=group)
        #---------------------------------------------------------------------------------------------------------------
        self.useToolchainsPackageSwitchSettingCard = SwitchPropertySettingCard(
            icon=Icon.CHECKBOX_MULTIPLE,
            title=self.tr("Use Toolchains Package"),
            value=PROJECT.useToolchainsPackage,
            content=self.tr("Use the built-in toolchain of this software."),
            parent=group)
        #---------------------------------------------------------------------------------------------------------------
        self.toolchainsComboBoxGroupSettingCard = ComboBoxPropertySettingCard(icon=Icon.TOOLS,
                                                                              title=self.tr("Toolchains"),
                                                                              value=PROJECT.toolchains,
                                                                              values=toolchains,
                                                                              content=PROJECT.toolchains,
                                                                              parent=group)
        #---------------------------------------------------------------------------------------------------------------
        self.toolchainsVersionComboBoxGroupSettingCard = ComboBoxPropertySettingCard(
            icon=Icon.DATABASE_2,
            title=self.tr("Toolchains Version"),
            value=PROJECT.toolchainsVersion,
            values=toolchainsVersions,
            content=PROJECT.toolchainsVersion,
            parent=group)
        count = self.toolchainsVersionComboBoxGroupSettingCard.hBoxLayout.count()
        self.toolchainsManagerBtn = ToolButton()
        self.toolchainsManagerBtn.setIcon(Icon.BOX)
        self.toolchainsVersionComboBoxGroupSettingCard.hBoxLayout.insertWidget(count - 2, self.toolchainsManagerBtn)
        self.toolchainsVersionComboBoxGroupSettingCard.hBoxLayout.insertSpacing(count - 1, 16)
        #---------------------------------------------------------------------------------------------------------------
        toolchainsPath = PACKAGE.path("toolchains", PROJECT.toolchains, PROJECT.toolchainsVersion)
        self.toolchainsPathToolButtonCard = ToolButtonPropertySettingCard(icon=Icon.FOLDER,
                                                                          title=self.tr("Toolchains Path"),
                                                                          btnIcon=Icon.BOX,
                                                                          content=toolchainsPath,
                                                                          parent=group)
        #---------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.builderComboBoxGroupSettingCard)
        group.addSettingCard(self.builderVersionComboBoxGroupSettingCard)
        group.addSettingCard(self.useToolchainsPackageSwitchSettingCard)
        group.addSettingCard(self.toolchainsComboBoxGroupSettingCard)
        group.addSettingCard(self.toolchainsVersionComboBoxGroupSettingCard)
        group.addSettingCard(self.toolchainsPathToolButtonCard)

        return group

    def __createLinkerGroup(self) -> SettingCardGroup:
        if converters.ishex(PROJECT.defaultHeapSize):
            defaultHeapSize = PROJECT.defaultHeapSize
        elif converters.ishex(PROJECT.summary.defaultHeapSize):
            defaultHeapSize = PROJECT.summary.defaultHeapSize
        else:
            return None
        #---------------------------------------------------------------------------------------------------------------
        if converters.ishex(PROJECT.defaultStackSize):
            defaultStackSize = PROJECT.defaultStackSize
        elif converters.ishex(PROJECT.summary.defaultStackSize):
            defaultStackSize = PROJECT.summary.defaultStackSize
        else:
            return None
        #---------------------------------------------------------------------------------------------------------------

        group = SettingCardGroup(self.tr("Linker Settings"), self.widgetScroll)

        #---------------------------------------------------------------------------------------------------------------
        self.defaultHeapLineEditCard = LineEditPropertySettingCard(icon=Icon.FOLDER,
                                                                   title=self.tr("Default heap size"),
                                                                   value=defaultHeapSize,
                                                                   content=defaultHeapSize,
                                                                   validator=R"(^0x[0-9A-Fa-f]+$)",
                                                                   parent=group)
        self.defaultHeapLineEditCard.textChanged.connect(self.__on_defaultHeapLineEditCard_textChanged)
        PROJECT.defaultHeapSizeChanged.connect(lambda t: self.defaultHeapLineEditCard.setContent(t))
        #---------------------------------------------------------------------------------------------------------------
        self.defaultStackLineEditCard = LineEditPropertySettingCard(icon=Icon.FOLDER,
                                                                    title=self.tr("Default stack size"),
                                                                    value=defaultStackSize,
                                                                    content=defaultStackSize,
                                                                    validator=R"(^0x[0-9A-Fa-f]+$)",
                                                                    parent=group)
        self.defaultStackLineEditCard.textChanged.connect(self.__on_defaultStackLineEditCard_textChanged)
        PROJECT.defaultStackSizeChanged.connect(lambda t: self.defaultStackLineEditCard.setContent(t))
        #---------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.defaultHeapLineEditCard)
        group.addSettingCard(self.defaultStackLineEditCard)

        return group

    def __on_defaultHeapLineEditCard_textChanged(self, text: str):
        ishex = converters.ishex(text)
        if ishex:
            PROJECT.defaultHeapSize = text
        self.defaultHeapLineEditCard.setStatusInfo(not ishex, self.tr("The Path is not directory"))

    def __on_defaultStackLineEditCard_textChanged(self, text: str):
        ishex = converters.ishex(text)
        if ishex:
            PROJECT.defaultStackSize = text
        self.defaultStackLineEditCard.setStatusInfo(not ishex, self.tr("The Path is not directory"))


class SettingView(Ui_SettingView, QWidget):

    __navigationViews = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.settingTreeCard.setFixedWidth(300)
        self.settingTree.header().setVisible(False)
        self.settingTree.selectionModel().selectionChanged.connect(self.__on_settingTree_selectionChanged)

        self.systemSettingView = SystemSettingView(self)
        self.generateSettingView = GenerateSettingView(self)

        self.__addView(self.systemSettingView, Icon.LIST_SETTINGS, self.tr("System Setting"))
        self.__addView(self.generateSettingView, Icon.FOLDER_TRANSFER, self.tr("Generate Setting"))

        Style.VIEW_SETTING.apply(self)

    def __addView(self, view: QWidget, icon: FluentIconBase, text: str):
        if text in self.__navigationViews:
            return

        item = QTreeWidgetItem([text])
        item.setIcon(0, icon.icon())
        self.settingTree.addTopLevelItem(item)

        self.settingStackedWidget.addWidget(view)

        self.__navigationViews[text] = view

    def __on_settingTree_selectionChanged(self, selected: QItemSelection, deselected: QItemSelection):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            key = index.data(Qt.ItemDataRole.DisplayRole)
            self.settingStackedWidget.setCurrentWidget(self.__navigationViews[key])
