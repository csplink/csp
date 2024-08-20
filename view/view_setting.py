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
# @file        view_setting.py
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


class view_setting(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # setting label
        self.u_label_setting = QLabel(self.tr("Settings"), self)
        self.u_label_setting.setObjectName('label_setting')
        self.u_label_setting.move(36, 30)

        self.u_widget_scroll = QWidget()
        self.u_widget_scroll.setObjectName('widget_scroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.u_widget_scroll)
        self.setWidgetResizable(True)
        self.setObjectName('view_setting')

        self.u_group_folders = self.__create_folders_group()
        self.u_group_style = self.__create_personalization_group()
        self.u_group_system = self.__create_system_group()
        self.u_group_update = self.__create_update_group()
        self.u_group_about = self.__create_about_group()

        self.u_expand_layout = ExpandLayout(self.u_widget_scroll)
        self.u_expand_layout.setSpacing(28)
        self.u_expand_layout.setContentsMargins(36, 10, 36, 0)
        self.u_expand_layout.addWidget(self.u_group_folders)
        self.u_expand_layout.addWidget(self.u_group_style)
        self.u_expand_layout.addWidget(self.u_group_system)
        self.u_expand_layout.addWidget(self.u_group_update)
        self.u_expand_layout.addWidget(self.u_group_about)

        Style.view_setting.apply(self)

        SETTINGS.appRestartSig.connect(self.__show_restart_tooltip)

    def __create_folders_group(self) -> SettingCardGroup:
        group_folders = SettingCardGroup(self.tr("Folders Location"), self.u_widget_scroll)
        self.u_card_database_folder = PushSettingCard(self.tr('Choose folder'), FIF.FOLDER,
                                                      self.tr("Database directory"),
                                                      SETTINGS.get(SETTINGS.databaseFolder), group_folders)
        self.u_card_database_folder.clicked.connect(self.__on__card_database_folder__clicked)
        group_folders.addSettingCard(self.u_card_database_folder)
        return group_folders

    def __create_personalization_group(self) -> SettingCardGroup:
        group_style = SettingCardGroup(self.tr('Personalization'), self.u_widget_scroll)
        self.u_card_theme = OptionsSettingCard(SETTINGS.themeMode,
                                               FIF.BRUSH,
                                               self.tr('Application theme'),
                                               self.tr("Change the appearance of your application"),
                                               texts=[self.tr('Light'),
                                                      self.tr('Dark'),
                                                      self.tr('Use system setting')],
                                               parent=group_style)
        self.u_card_theme_color = CustomColorSettingCard(SETTINGS.themeColor, FIF.PALETTE, self.tr('Theme color'),
                                                         self.tr('Change the theme color of you application'),
                                                         group_style)
        self.u_card_theme.optionChanged.connect(lambda ci: setTheme(SETTINGS.get(ci)))
        self.u_card_theme_color.colorChanged.connect(lambda c: setThemeColor(c))
        group_style.addSettingCard(self.u_card_theme)
        group_style.addSettingCard(self.u_card_theme_color)
        return group_style

    def __create_system_group(self) -> SettingCardGroup:
        group_system = SettingCardGroup(self.tr('System'), self.u_widget_scroll)
        self.u_card_language = ComboBoxSettingCard(SETTINGS.language,
                                                   FIF.LANGUAGE,
                                                   self.tr('Language'),
                                                   self.tr('Set your preferred language for UI'),
                                                   texts=['简体中文', '繁體中文', 'English',
                                                          self.tr('Use system setting')],
                                                   parent=group_system)
        self.u_card_zoom = OptionsSettingCard(
            SETTINGS.dpiScale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=["100%", "125%", "150%", "175%", "200%",
                   self.tr("Use system setting")],
            parent=group_system)
        group_system.addSettingCard(self.u_card_language)
        group_system.addSettingCard(self.u_card_zoom)
        return group_system

    def __create_update_group(self) -> SettingCardGroup:
        group_update = SettingCardGroup(self.tr("Software update"), self.u_widget_scroll)
        self.u_card_update_on_startup = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=SETTINGS.checkUpdateAtStartUp,
            parent=group_update)
        group_update.addSettingCard(self.u_card_update_on_startup)
        return group_update

    def __create_about_group(self) -> SettingCardGroup:
        group_about = SettingCardGroup(self.tr('About'), self.u_widget_scroll)
        self.u_card_help = HyperlinkCard(HELP_URL, self.tr('Open help page'), FIF.HELP, self.tr('Help'),
                                         self.tr('Discover new features and learn useful tips about csp'), group_about)
        self.u_card_feedback = PrimaryPushSettingCard(self.tr('Provide feedback'), FIF.FEEDBACK,
                                                      self.tr('Provide feedback'),
                                                      self.tr('Help us improve csp by providing feedback'), group_about)
        self.u_card_feedback.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
        self.u_card_about = PrimaryPushSettingCard(
            self.tr('Check update'), FIF.INFO, self.tr('About'),
            f"© {self.tr('Copyright')} {YEAR}, {AUTHOR}. {self.tr('Version')} {VERSION}", group_about)
        group_about.addSettingCard(self.u_card_help)
        group_about.addSettingCard(self.u_card_feedback)
        group_about.addSettingCard(self.u_card_about)
        return group_about

    def __show_restart_tooltip(self):
        """ show restart tooltip """
        InfoBar.success(self.tr('Updated successfully'),
                        self.tr('Configuration takes effect after restart'),
                        duration=1500,
                        parent=self)

    def __on__card_database_folder__clicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.databaseFolder) == folder:
            return

        SETTINGS.set(SETTINGS.databaseFolder, folder)
        self.u_card_database_folder.setContent(folder)
