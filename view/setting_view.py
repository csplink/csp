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

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QWidget, QLabel, QFileDialog

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, PushSettingCard, HyperlinkCard,
                            PrimaryPushSettingCard, ScrollArea, ComboBoxSettingCard, ExpandLayout,
                            CustomColorSettingCard, setTheme, setThemeColor)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar

from common import SETTINGS, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR, Style


class SettingView(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # setting label
        self.labelSetting = QLabel(self.tr("Settings"), self)
        self.labelSetting.setObjectName('label_setting')
        self.labelSetting.move(36, 30)

        self.widgetScroll = QWidget()
        self.widgetScroll.setObjectName('widget_scroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widgetScroll)
        self.setWidgetResizable(True)
        self.setObjectName('view_setting')

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

        Style.VIEW_SETTING.apply(self)

        SETTINGS.appRestartSig.connect(self.__showRestartTooltip)

    def __createFoldersGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Folders Location"), self.widgetScroll)
        self.cardDatabaseFolder = PushSettingCard(self.tr('Choose folder'), FIF.FOLDER, self.tr("Database directory"),
                                                  SETTINGS.get(SETTINGS.databaseFolder), group)
        self.cardDatabaseFolder.clicked.connect(self.__on_cardDatabaseFolder_clicked)
        group.addSettingCard(self.cardDatabaseFolder)
        return group

    def __createPersonalizationGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('Personalization'), self.widgetScroll)
        self.cardTheme = OptionsSettingCard(SETTINGS.themeMode,
                                            FIF.BRUSH,
                                            self.tr('Application theme'),
                                            self.tr("Change the appearance of your application"),
                                            texts=[self.tr('Light'),
                                                   self.tr('Dark'),
                                                   self.tr('Use system setting')],
                                            parent=group)
        self.cardThemeColor = CustomColorSettingCard(SETTINGS.themeColor, FIF.PALETTE, self.tr('Theme color'),
                                                     self.tr('Change the theme color of you application'), group)
        self.cardTheme.optionChanged.connect(lambda ci: setTheme(SETTINGS.get(ci)))
        self.cardThemeColor.colorChanged.connect(lambda c: setThemeColor(c))
        group.addSettingCard(self.cardTheme)
        group.addSettingCard(self.cardThemeColor)
        return group

    def __createSystemGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('System'), self.widgetScroll)
        self.cardLanguage = ComboBoxSettingCard(SETTINGS.language,
                                                FIF.LANGUAGE,
                                                self.tr('Language'),
                                                self.tr('Set your preferred language for UI'),
                                                texts=['简体中文', '繁體中文', 'English',
                                                       self.tr('Use system setting')],
                                                parent=group)
        self.cardZoom = OptionsSettingCard(
            SETTINGS.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=["100%", "125%", "150%", "175%", "200%",
                   self.tr("Use system setting")],
            parent=group)
        group.addSettingCard(self.cardLanguage)
        group.addSettingCard(self.cardZoom)
        return group

    def __createUpdateGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Software update"), self.widgetScroll)
        self.cardUpdateAtStartup = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=SETTINGS.checkUpdateAtStartup,
            parent=group)
        group.addSettingCard(self.cardUpdateAtStartup)
        return group

    def __createAboutGroup(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('About'), self.widgetScroll)
        self.cardHelp = HyperlinkCard(HELP_URL, self.tr('Open help page'), FIF.HELP, self.tr('Help'),
                                      self.tr('Discover new features and learn useful tips about csp'), group)
        self.cardFeedback = PrimaryPushSettingCard(self.tr('Provide feedback'), FIF.FEEDBACK,
                                                   self.tr('Provide feedback'),
                                                   self.tr('Help us improve csp by providing feedback'), group)
        self.cardFeedback.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
        self.cardAbout = PrimaryPushSettingCard(
            self.tr('Check update'), FIF.INFO, self.tr('About'),
            f"© {self.tr('Copyright')} {YEAR}, {AUTHOR}. {self.tr('Version')} {VERSION}", group)
        group.addSettingCard(self.cardHelp)
        group.addSettingCard(self.cardFeedback)
        group.addSettingCard(self.cardAbout)
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
        self.cardDatabaseFolder.setContent(folder)
