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

from qfluentwidgets import (SettingCardGroup, SwitchSettingCard, OptionsSettingCard, PushSettingCard, HyperlinkCard,
                            PrimaryPushSettingCard, ScrollArea, ComboBoxSettingCard, ExpandLayout,
                            CustomColorSettingCard, setTheme, setThemeColor)
from qfluentwidgets import FluentIcon as FIF
from qfluentwidgets import InfoBar
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtWidgets import QWidget, QLabel, QFileDialog

from common import SETTINGS, HELP_URL, FEEDBACK_URL, AUTHOR, VERSION, YEAR, Style


class SettingView(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scrollWidget = QWidget()
        self.expandLayout = ExpandLayout(self.scrollWidget)

        # setting label
        self.settingLabel = QLabel(self.tr("Settings"), self)

        # folders
        self.foldersGroup = SettingCardGroup(self.tr("Folders Location"), self.scrollWidget)
        self.databaseFolderCard = PushSettingCard(self.tr('Choose folder'), FIF.FOLDER, self.tr("Database directory"),
                                                  SETTINGS.get(SETTINGS.databaseFolder), self.foldersGroup)

        # personalization
        self.styleGroup = SettingCardGroup(self.tr('Personalization'), self.scrollWidget)
        self.themeCard = OptionsSettingCard(SETTINGS.themeMode,
                                            FIF.BRUSH,
                                            self.tr('Application theme'),
                                            self.tr("Change the appearance of your application"),
                                            texts=[self.tr('Light'),
                                                   self.tr('Dark'),
                                                   self.tr('Use system setting')],
                                            parent=self.styleGroup)
        self.themeColorCard = CustomColorSettingCard(SETTINGS.themeColor, FIF.PALETTE, self.tr('Theme color'),
                                                     self.tr('Change the theme color of you application'),
                                                     self.styleGroup)

        self.systemGroup = SettingCardGroup(self.tr('System'), self.scrollWidget)
        self.languageCard = ComboBoxSettingCard(SETTINGS.language,
                                                FIF.LANGUAGE,
                                                self.tr('Language'),
                                                self.tr('Set your preferred language for UI'),
                                                texts=['简体中文', '繁體中文', 'English',
                                                       self.tr('Use system setting')],
                                                parent=self.systemGroup)
        self.zoomCard = OptionsSettingCard(
            SETTINGS.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=["100%", "125%", "150%", "175%", "200%",
                   self.tr("Use system setting")],
            parent=self.systemGroup)

        # update software
        self.updateSoftwareGroup = SettingCardGroup(self.tr("Software update"), self.scrollWidget)
        self.updateOnStartUpCard = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=SETTINGS.checkUpdateAtStartUp,
            parent=self.updateSoftwareGroup)

        # application
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scrollWidget)
        self.helpCard = HyperlinkCard(HELP_URL, self.tr('Open help page'), FIF.HELP, self.tr('Help'),
                                      self.tr('Discover new features and learn useful tips about csp'), self.aboutGroup)
        self.feedbackCard = PrimaryPushSettingCard(self.tr('Provide feedback'), FIF.FEEDBACK,
                                                   self.tr('Provide feedback'),
                                                   self.tr('Help us improve csp by providing feedback'),
                                                   self.aboutGroup)
        self.aboutCard = PrimaryPushSettingCard(
            self.tr('Check update'), FIF.INFO, self.tr('About'),
            '© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " + self.tr('Version') + " " + VERSION, self.aboutGroup)

        self.__initWidget()

    def __initWidget(self):
        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.scrollWidget)
        self.setWidgetResizable(True)
        self.setObjectName('SettingView')

        # initialize style sheet
        self.scrollWidget.setObjectName('scrollWidget')
        self.settingLabel.setObjectName('settingLabel')
        Style.SETTING_VIEW.apply(self)

        # self.micaCard.setEnabled(isWin11())

        # initialize layout
        self.__initLayout()
        self.__connectSignalToSlot()

    def __initLayout(self):
        self.settingLabel.move(36, 30)

        # add cards to group
        self.foldersGroup.addSettingCard(self.databaseFolderCard)

        self.styleGroup.addSettingCard(self.themeCard)
        self.styleGroup.addSettingCard(self.themeColorCard)

        self.systemGroup.addSettingCard(self.languageCard)
        self.systemGroup.addSettingCard(self.zoomCard)

        self.updateSoftwareGroup.addSettingCard(self.updateOnStartUpCard)

        self.aboutGroup.addSettingCard(self.helpCard)
        self.aboutGroup.addSettingCard(self.feedbackCard)
        self.aboutGroup.addSettingCard(self.aboutCard)

        # add setting card group to layout
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)
        self.expandLayout.addWidget(self.foldersGroup)
        self.expandLayout.addWidget(self.styleGroup)
        self.expandLayout.addWidget(self.systemGroup)
        self.expandLayout.addWidget(self.updateSoftwareGroup)
        self.expandLayout.addWidget(self.aboutGroup)

    def __showRestartTooltip(self):
        """ show restart tooltip """
        InfoBar.success(self.tr('Updated successfully'),
                        self.tr('Configuration takes effect after restart'),
                        duration=1500,
                        parent=self)

    def __onDatabaseFolderCardClicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.databaseFolder) == folder:
            return

        SETTINGS.set(SETTINGS.databaseFolder, folder)
        self.databaseFolderCard.setContent(folder)

    def __connectSignalToSlot(self):
        """ connect signal to slot """
        SETTINGS.appRestartSig.connect(self.__showRestartTooltip)

        # folders
        self.databaseFolderCard.clicked.connect(self.__onDatabaseFolderCardClicked)

        # personalization
        self.themeCard.optionChanged.connect(lambda ci: setTheme(SETTINGS.get(ci)))
        self.themeColorCard.colorChanged.connect(lambda c: setThemeColor(c))

        # about
        self.feedbackCard.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
