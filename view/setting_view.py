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


class SettingView(ScrollArea):
    """ Setting interface """

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # setting label
        self.label_setting = QLabel(self.tr("Settings"), self)
        self.label_setting.setObjectName('label_setting')
        self.label_setting.move(36, 30)

        self.widget_scroll = QWidget()
        self.widget_scroll.setObjectName('widget_scroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widget_scroll)
        self.setWidgetResizable(True)
        self.setObjectName('view_setting')

        self.group_folders = self.__create_folders_group()
        self.group_style = self.__create_personalization_group()
        self.group_system = self.__create_system_group()
        self.group_update = self.__create_update_group()
        self.group_about = self.__create_about_group()

        self.expand_layout = ExpandLayout(self.widget_scroll)
        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)
        self.expand_layout.addWidget(self.group_folders)
        self.expand_layout.addWidget(self.group_style)
        self.expand_layout.addWidget(self.group_system)
        self.expand_layout.addWidget(self.group_update)
        self.expand_layout.addWidget(self.group_about)

        Style.VIEW_SETTING.apply(self)

        SETTINGS.appRestartSig.connect(self.__show_restart_tooltip)

    def __create_folders_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Folders Location"), self.widget_scroll)
        self.card_database_folder = PushSettingCard(self.tr('Choose folder'), FIF.FOLDER, self.tr("Database directory"),
                                                    SETTINGS.get(SETTINGS.database_folder), group)
        self.card_database_folder.clicked.connect(self.__on__card_database_folder__clicked)
        group.addSettingCard(self.card_database_folder)
        return group

    def __create_personalization_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('Personalization'), self.widget_scroll)
        self.card_theme = OptionsSettingCard(SETTINGS.theme_mode,
                                             FIF.BRUSH,
                                             self.tr('Application theme'),
                                             self.tr("Change the appearance of your application"),
                                             texts=[self.tr('Light'),
                                                    self.tr('Dark'),
                                                    self.tr('Use system setting')],
                                             parent=group)
        self.card_theme_color = CustomColorSettingCard(SETTINGS.theme_color, FIF.PALETTE, self.tr('Theme color'),
                                                       self.tr('Change the theme color of you application'), group)
        self.card_theme.optionChanged.connect(lambda ci: setTheme(SETTINGS.get(ci)))
        self.card_theme_color.colorChanged.connect(lambda c: setThemeColor(c))
        group.addSettingCard(self.card_theme)
        group.addSettingCard(self.card_theme_color)
        return group

    def __create_system_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('System'), self.widget_scroll)
        self.card_language = ComboBoxSettingCard(SETTINGS.language,
                                                 FIF.LANGUAGE,
                                                 self.tr('Language'),
                                                 self.tr('Set your preferred language for UI'),
                                                 texts=['简体中文', '繁體中文', 'English',
                                                        self.tr('Use system setting')],
                                                 parent=group)
        self.card_zoom = OptionsSettingCard(
            SETTINGS.dpi_scale,
            FIF.ZOOM,
            self.tr("Interface zoom"),
            self.tr("Change the size of widgets and fonts"),
            texts=["100%", "125%", "150%", "175%", "200%",
                   self.tr("Use system setting")],
            parent=group)
        group.addSettingCard(self.card_language)
        group.addSettingCard(self.card_zoom)
        return group

    def __create_update_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Software update"), self.widget_scroll)
        self.card_update_on_startup = SwitchSettingCard(
            FIF.UPDATE,
            self.tr('Check for updates when the application starts'),
            self.tr('The new version will be more stable and have more features'),
            configItem=SETTINGS.check_update_at_startup,
            parent=group)
        group.addSettingCard(self.card_update_on_startup)
        return group

    def __create_about_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr('About'), self.widget_scroll)
        self.card_help = HyperlinkCard(HELP_URL, self.tr('Open help page'), FIF.HELP, self.tr('Help'),
                                       self.tr('Discover new features and learn useful tips about csp'), group)
        self.card_feedback = PrimaryPushSettingCard(self.tr('Provide feedback'), FIF.FEEDBACK,
                                                    self.tr('Provide feedback'),
                                                    self.tr('Help us improve csp by providing feedback'), group)
        self.card_feedback.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(FEEDBACK_URL)))
        self.card_about = PrimaryPushSettingCard(
            self.tr('Check update'), FIF.INFO, self.tr('About'),
            f"© {self.tr('Copyright')} {YEAR}, {AUTHOR}. {self.tr('Version')} {VERSION}", group)
        group.addSettingCard(self.card_help)
        group.addSettingCard(self.card_feedback)
        group.addSettingCard(self.card_about)
        return group

    def __show_restart_tooltip(self):
        """ show restart tooltip """
        InfoBar.success(self.tr('Updated successfully'),
                        self.tr('Configuration takes effect after restart'),
                        duration=1500,
                        parent=self)

    def __on__card_database_folder__clicked(self):
        """ download folder card clicked slot """
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))
        if not folder or SETTINGS.get(SETTINGS.database_folder) == folder:
            return

        SETTINGS.set(SETTINGS.database_folder, folder)
        self.card_database_folder.setContent(folder)
