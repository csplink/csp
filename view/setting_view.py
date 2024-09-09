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

from typing import Union

from PySide6.QtCore import Qt, QUrl, QItemSelection
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog, QTreeWidgetItem

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, PushSettingCard, HyperlinkCard,
                            PrimaryPushSettingCard, ScrollArea, ComboBoxSettingCard, ExpandLayout, FluentIconBase,
                            CustomColorSettingCard, setTheme, setThemeColor, InfoBar, SettingCard, LineEdit)

from .ui.ui_setting_view import Ui_SettingView

from common import (SETTINGS, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR, Style, Icon, PROJECT)


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

        self.databaseFolderCard = PushSettingCard(self.tr('Choose folder'), Icon.FOLDER, self.tr("Database directory"),
                                                  SETTINGS.get(SETTINGS.databaseFolder), group)
        self.databaseFolderCard.clicked.connect(self.__on_cardDatabaseFolder_clicked)

        group.addSettingCard(self.databaseFolderCard)

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

    def __on_cardDatabaseFolder_clicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.databaseFolder) == folder:
            return

        SETTINGS.set(SETTINGS.databaseFolder, folder)
        self.databaseFolderCard.setContent(folder)


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

        self.expandLayout = ExpandLayout(self.widgetScroll)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.groupLinker)

        self.enableTransparentBackground()

    def __createLinkerGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Folders Location"), self.widgetScroll)

        self.minHeapLineEditCard = SettingCard(Icon.FOLDER, self.tr("Minimum heap size"), PROJECT.defaultHeapSize,
                                               group)
        self.minHeapLineEdit = LineEdit()
        self.minHeapLineEditCard.hBoxLayout.addWidget(self.minHeapLineEdit, 0, Qt.AlignmentFlag.AlignRight)
        self.minHeapLineEditCard.hBoxLayout.addSpacing(16)
        # self.button.clicked.connect(self.clicked)
        # self.databaseFolderCard.clicked.connect(self.__on_cardDatabaseFolder_clicked)

        group.addSettingCard(self.minHeapLineEditCard)

        return group


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
