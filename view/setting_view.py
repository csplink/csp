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
        self.widget_scroll = QWidget()
        self.expandLayout = ExpandLayout(self.widget_scroll)

        # setting label
        self.label_setting = QLabel(self.tr("Settings"), self)

        # folders
        self.group_folders = SettingCardGroup(self.tr("Folders Location"), self.widget_scroll)
        self.card_databaseFolder = PushSettingCard(self.tr('Choose folder'), FIF.FOLDER, self.tr("Database directory"),
                                                   SETTINGS.get(SETTINGS.databaseFolder), self.group_folders)

        # personalization
        self.group_style = SettingCardGroup(self.tr('Personalization'), self.widget_scroll)
        self.card_theme = OptionsSettingCard(SETTINGS.themeMode,
                                             FIF.BRUSH,
                                             self.tr('Application theme'),
                                             self.tr("Change the appearance of your application"),
                                             texts=[self.tr('Light'),
                                                    self.tr('Dark'),
                                                    self.tr('Use system setting')],
                                             parent=self.group_style)
        self.card_themeColor = CustomColorSettingCard(SETTINGS.themeColor, FIF.PALETTE, self.tr('Theme color'),
                                                      self.tr('Change the theme color of you application'),
                                                      self.group_style)

        self.group_system = SettingCardGroup(self.tr('System'), self.widget_scroll)
        self.card_language = ComboBoxSettingCard(SETTINGS.language,
                                                 FIF.LANGUAGE,
                                                 self.tr('Language'),
                                                 self.tr('Set your preferred language for UI'),
                                                 texts=['简体中文', '繁體中文', 'English',
                                                        self.tr('Use system setting')],
                                                 parent=self.group_system)
        self.card_zoom = OptionsSettingCard(
            SETTINGS.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=["100%", "125%", "150%", "175%", "200%",
                   self.tr("Use system setting")],
            parent=self.group_system)

        # update software
        self.group_updateSoftware = SettingCardGroup(self.tr("Software update"), self.widget_scroll)
        self.card_updateOnStartUp = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=SETTINGS.checkUpdateAtStartUp,
            parent=self.group_updateSoftware)

        # application
        self.group_about = SettingCardGroup(self.tr('About'), self.widget_scroll)
        self.card_help = HyperlinkCard(HELP_URL, self.tr('Open help page'), FIF.HELP, self.tr('Help'),
                                       self.tr('Discover new features and learn useful tips about csp'),
                                       self.group_about)
        self.card_feedback = PrimaryPushSettingCard(self.tr('Provide feedback'), FIF.FEEDBACK,
                                                    self.tr('Provide feedback'),
                                                    self.tr('Help us improve csp by providing feedback'),
                                                    self.group_about)
        self.card_about = PrimaryPushSettingCard(
            self.tr('Check update'), FIF.INFO, self.tr('About'),
            f"© {self.tr('Copyright')} {YEAR}, {AUTHOR}. {self.tr('Version')} {VERSION}", self.group_about)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widget_scroll)
        self.setWidgetResizable(True)
        self.setObjectName('SettingView')

        # initialize style sheet
        self.widget_scroll.setObjectName('widget_scroll')
        self.label_setting.setObjectName('label_setting')
        Style.SETTING_VIEW.apply(self)

        # self.micaCard.setEnabled(isWin11())

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.label_setting.move(36, 30)

        # add cards to group
        self.group_folders.addSettingCard(self.card_databaseFolder)

        self.group_style.addSettingCard(self.card_theme)
        self.group_style.addSettingCard(self.card_themeColor)

        self.group_system.addSettingCard(self.card_language)
        self.group_system.addSettingCard(self.card_zoom)

        self.group_updateSoftware.addSettingCard(self.card_updateOnStartUp)

        self.group_about.addSettingCard(self.card_help)
        self.group_about.addSettingCard(self.card_feedback)
        self.group_about.addSettingCard(self.card_about)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.group_folders)
        self.expandLayout.addWidget(self.group_style)
        self.expandLayout.addWidget(self.group_system)
        self.expandLayout.addWidget(self.group_updateSoftware)
        self.expandLayout.addWidget(self.group_about)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(self.tr('Updated successfully'),
                        self.tr('Configuration takes effect after restart'),
                        duration=1500,
                        parent=self)

    def __onCard_databaseFolderClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.databaseFolder) == folder:
            return

        SETTINGS.set(SETTINGS.databaseFolder, folder)
        self.card_databaseFolder.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        SETTINGS.appRestartSig.connect(self.__showRestartTooltip)

        # folders
        self.card_databaseFolder.clicked.connect(self.__onCard_databaseFolderClicked)

        # personalization
        self.card_theme.optionChanged.connect(lambda ci: setTheme(SETTINGS.get(ci)))
        self.card_themeColor.colorChanged.connect(lambda c: setThemeColor(c))

        # about
        self.card_feedback.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
