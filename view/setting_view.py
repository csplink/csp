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
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QFileDialog,
    QTreeWidgetItem,
    QStackedWidget,
)
from loguru import logger
from qfluentwidgets import (
    SettingCardGroup,
    SwitchSettingCard,
    OptionsSettingCard,
    PushSettingCard,
    HyperlinkCard,
    PrimaryPushSettingCard,
    ScrollArea,
    ComboBoxSettingCard,
    ExpandLayout,
    FluentIconBase,
    CustomColorSettingCard,
    setTheme,
    setThemeColor,
    InfoBar,
    ToolButton,
)

from common import SETTINGS, Style, Icon, PROJECT, PACKAGE, SIGNAL_BUS, SUMMARY
from utils import Converters
from widget import (
    LineEditPropertySettingCard,
    ComboBoxPropertySettingCard,
    SwitchPropertySettingCard,
    ToolButtonPropertySettingCard,
)
from .ui.setting_view_ui import Ui_SettingView


class SystemSettingView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("SystemSettingView")

        # setting label
        self.setting_label = QLabel(self.tr("System Setting"), self)  # type: ignore
        self.setting_label.setObjectName("settingLabel")
        self.setting_label.move(36, 30)

        self.widget_scroll = QWidget()
        self.widget_scroll.setObjectName("widgetScroll")

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widget_scroll)
        self.setWidgetResizable(True)

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

        SETTINGS.appRestartSig.connect(self.__show_restart_tooltip)
        self.enableTransparentBackground()

    def __create_folders_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Folders Location"), self.widget_scroll)  # type: ignore

        # ---------------------------------------------------------------------------------------------------------------
        self.package_folder_card = PushSettingCard(
            self.tr("Choose folder"),  # type: ignore
            Icon.FOLDER,
            self.tr("Package directory"),  # type: ignore
            SETTINGS.package_folder.value,
            group,
        )
        self.package_folder_card.clicked.connect(
            self.__on_repository_folder_card_clicked
        )
        # ---------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.package_folder_card)

        return group

    def __create_personalization_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Personalization"), self.widget_scroll)  # type: ignore

        self.theme_card = OptionsSettingCard(
            SETTINGS.theme_mode,
            Icon.PAINT,
            self.tr("Application theme"),  # type: ignore
            self.tr("Change the appearance of your application"),  # type: ignore
            texts=[self.tr("Light"), self.tr("Dark"), self.tr("Use system setting")],  # type: ignore
            parent=group,
        )
        self.theme_card.optionChanged.connect(lambda ci: setTheme(SETTINGS.get(ci)))

        self.theme_color_card = CustomColorSettingCard(
            SETTINGS.theme_color,
            Icon.PALETTE,
            self.tr("Theme color"),  # type: ignore
            self.tr("Change the theme color of you application"),  # type: ignore
            group,
        )
        self.theme_color_card.colorChanged.connect(lambda c: setThemeColor(c))

        self.alert_color_card = CustomColorSettingCard(
            SETTINGS.alert_color,
            Icon.PALETTE,
            self.tr("Alert color"),  # type: ignore
            self.tr("Change the alert color of you application"),  # type: ignore
            group,
        )

        group.addSettingCard(self.theme_card)
        group.addSettingCard(self.theme_color_card)
        group.addSettingCard(self.alert_color_card)

        return group

    def __create_system_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("System"), self.widget_scroll)  # type: ignore

        self.language_card = ComboBoxSettingCard(
            SETTINGS.language,
            Icon.GLOBAL,
            self.tr("Language"),  # type: ignore
            self.tr("Set your preferred language for UI"),  # type: ignore
            texts=["简体中文", "繁體中文", "English", self.tr("Use system setting")],  # type: ignore
            parent=group,
        )
        self.zoom_card = OptionsSettingCard(
            SETTINGS.dpi_scale,
            Icon.PICTURE_IN_PICTURE,
            self.tr("Interface zoom"),  # type: ignore
            self.tr("Change the size of widgets and fonts"),  # type: ignore
            texts=[
                "100%",
                "125%",
                "150%",
                "175%",
                "200%",
                self.tr("Use system setting"),  # type: ignore
            ],
            parent=group,
        )
        self.use_opengl_card = SwitchSettingCard(
            Icon.SPEED_UP,
            self.tr("Using opengl for acceleration"),  # type: ignore
            self.tr("Hardware acceleration for your applications"),  # type: ignore
            configItem=SETTINGS.is_use_opengl,
            parent=group,
        )
        self.opengl_samples_card = OptionsSettingCard(
            icon=Icon.NUMBERS,
            title=self.tr("OpenGL samples"),  # type: ignore
            content=self.tr("Set the preferred number of samples per pixel"),  # type: ignore
            configItem=SETTINGS.opengl_samples,
            texts=["4", "8", "12", "16"],
            parent=group,
        )

        group.addSettingCard(self.language_card)
        group.addSettingCard(self.zoom_card)
        group.addSettingCard(self.use_opengl_card)
        group.addSettingCard(self.opengl_samples_card)

        return group

    def __create_update_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("Software update"), self.widget_scroll)  # type: ignore

        self.update_at_startup_card = SwitchSettingCard(
            Icon.REFRESH,
            self.tr("Check for updates when the application starts"),  # type: ignore
            self.tr("The new version will be more stable and have more features"),  # type: ignore
            configItem=SETTINGS.is_update_at_startup,
            parent=group,
        )

        group.addSettingCard(self.update_at_startup_card)

        return group

    def __create_about_group(self) -> SettingCardGroup:
        group = SettingCardGroup(self.tr("About"), self.widget_scroll)  # type: ignore

        self.help_card = HyperlinkCard(
            SETTINGS.HELP_URL,
            self.tr("Open help page"),  # type: ignore
            Icon.QUESTION,
            self.tr("Help"),  # type: ignore
            self.tr("Discover new features and learn useful tips about CSP"),  # type: ignore
            group,
        )

        self.feedback_card = PrimaryPushSettingCard(
            self.tr("Provide feedback"),  # type: ignore
            Icon.FEEDBACK,
            self.tr("Provide feedback"),  # type: ignore
            self.tr("Help us improve CSP by providing feedback"),  # type: ignore
            group,
        )
        self.feedback_card.clicked.connect(
            lambda: QDesktopServices.openUrl(QUrl(SETTINGS.FEEDBACK_URL))
        )

        self.about_card = PrimaryPushSettingCard(
            self.tr("Check update"),  # type: ignore
            Icon.INFORMATION,
            self.tr("About"),  # type: ignore
            f"© {self.tr('Copyright')} {SETTINGS.YEAR}, {SETTINGS.AUTHOR}. {self.tr('Version')} {SETTINGS.VERSION}",  # type: ignore
            group,
        )

        group.addSettingCard(self.help_card)
        group.addSettingCard(self.feedback_card)
        group.addSettingCard(self.about_card)

        return group

    def __show_restart_tooltip(self):
        """show restart tooltip"""
        InfoBar.success(
            self.tr("Updated successfully"),  # type: ignore
            self.tr("Configuration takes effect after restart"),  # type: ignore
            duration=1500,
            parent=self,
        )

    def __on_repository_folder_card_clicked(self):
        """download folder card clicked slot"""
        folder = QFileDialog.getExistingDirectory(self, self.tr("Choose folder"))  # type: ignore
        if not folder or SETTINGS.get(SETTINGS.package_folder) == folder:
            return

        SETTINGS.set(SETTINGS.package_folder, folder)
        self.package_folder_card.setContent(folder)


class GenerateSettingView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("GenerateSettingView")

        # setting label
        self.setting_label = QLabel(self.tr("Generate Setting"), self)  # type: ignore
        self.setting_label.setObjectName("settingLabel")
        self.setting_label.move(36, 30)

        self.widget_scroll = QWidget()
        self.widget_scroll.setObjectName("widgetScroll")

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widget_scroll)
        self.setWidgetResizable(True)

        self.linker_group = self.__create_linker_group()
        self.builder_group = self.__create_builder_group()
        self.hal_group = self.__create_hal_group()

        self.expand_layout = ExpandLayout(self.widget_scroll)
        self.expand_layout.setSpacing(28)
        self.expand_layout.setContentsMargins(36, 10, 36, 0)

        if self.linker_group is not None:
            self.expand_layout.addWidget(self.linker_group)
        if self.builder_group is not None:
            self.expand_layout.addWidget(self.builder_group)
            SIGNAL_BUS.package_updated.connect(self.__update_builder_settings)
            self.__update_builder_settings()
        if self.hal_group is not None:
            self.expand_layout.addWidget(self.hal_group)
            self.__update_hal_settings()

        self.enableTransparentBackground()

    def __create_builder_group(self) -> SettingCardGroup | None:
        # --------------------------------------------------------------------------------------------------------------
        if len(SUMMARY.project_summary().builder.keys()) == 0:
            return None

        group = SettingCardGroup(self.tr("Builder Settings"), self.widget_scroll)  # type: ignore

        # --------------------------------------------------------------------------------------------------------------
        self.builder_combo_box_group_setting_card = ComboBoxPropertySettingCard(
            icon=Icon.HAMMER,
            title=self.tr("Builder Tools"),  # type: ignore
            value="",
            values=[],
            content=" ",
            parent=group,
        )
        self.builder_combo_box_group_setting_card.current_text_changed.connect(
            self.__on_builderComboBoxGroupSettingCard_currentTextChanged
        )
        # --------------------------------------------------------------------------------------------------------------
        self.builder_version_combo_box_group_setting_card = ComboBoxPropertySettingCard(
            icon=Icon.DATABASE_2,
            title=self.tr("Builder Version"),  # type: ignore
            value="",
            values=[],
            content=" ",
            parent=group,
        )
        self.builder_version_combo_box_group_setting_card.current_text_changed.connect(
            self.__on_builderVersionComboBoxGroupSettingCard_currentTextChanged
        )
        # --------------------------------------------------------------------------------------------------------------
        self.toolchains_combo_box_group_setting_card = ComboBoxPropertySettingCard(
            icon=Icon.TOOLS,
            title=self.tr("Toolchains"),  # type: ignore
            value="",
            values=[],
            content=" ",
            parent=group,
        )
        self.toolchains_combo_box_group_setting_card.current_text_changed.connect(
            self.__on_toolchainsComboBoxGroupSettingCard_currentTextChanged
        )
        # --------------------------------------------------------------------------------------------------------------
        self.use_toolchains_package_switch_setting_card = SwitchPropertySettingCard(
            icon=Icon.CHECKBOX_MULTIPLE,
            title=self.tr("Use Toolchains Package"),  # type: ignore
            value=PROJECT.project().gen.use_toolchains_package,
            content=self.tr("Use the built-in toolchain of this software"),  # type: ignore
            parent=group,
        )
        self.use_toolchains_package_switch_setting_card.checked_changed.connect(
            self.__on_useToolchainsPackageSwitchSettingCard_checkedChanged
        )
        # --------------------------------------------------------------------------------------------------------------
        self.toolchains_version_combo_box_group_setting_card = (
            ComboBoxPropertySettingCard(
                icon=Icon.DATABASE_2,
                title=self.tr("Toolchains Version"),  # type: ignore
                value="",
                values=[],
                content=" ",
                parent=group,
            )
        )
        count = self.toolchains_version_combo_box_group_setting_card.hBoxLayout.count()
        self.toolchains_manager_btn = ToolButton()
        self.toolchains_manager_btn.setIcon(Icon.BOX)
        self.toolchains_version_combo_box_group_setting_card.hBoxLayout.insertWidget(
            count - 2, self.toolchains_manager_btn
        )
        self.toolchains_version_combo_box_group_setting_card.hBoxLayout.insertSpacing(
            count - 1, 16
        )
        self.toolchains_version_combo_box_group_setting_card.current_text_changed.connect(
            self.__on_toolchainsVersionComboBoxGroupSettingCard_currentTextChanged
        )
        self.toolchains_manager_btn.clicked.connect(
            self.__on_toolchainsManagerBtn_clicked
        )
        # --------------------------------------------------------------------------------------------------------------
        self.toolchains_path_tool_button_setting_card = ToolButtonPropertySettingCard(
            icon=Icon.FOLDER,
            title=self.tr("Toolchains Path"),  # type: ignore
            btn_icon=Icon.BOX,
            content=" ",
            parent=group,
        )
        self.toolchains_path_tool_button_setting_card.clicked.connect(
            self.__on_toolchains_path_tool_button_setting_card_clicked
        )
        # --------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.builder_combo_box_group_setting_card)
        group.addSettingCard(self.builder_version_combo_box_group_setting_card)
        group.addSettingCard(self.toolchains_combo_box_group_setting_card)
        group.addSettingCard(self.use_toolchains_package_switch_setting_card)
        group.addSettingCard(self.toolchains_version_combo_box_group_setting_card)
        group.addSettingCard(self.toolchains_path_tool_button_setting_card)

        if not PROJECT.project().gen.use_toolchains_package:
            self.toolchains_version_combo_box_group_setting_card.setEnabled(False)
            self.toolchains_path_tool_button_setting_card.setEnabled(False)

        return group

    def __create_linker_group(self) -> SettingCardGroup | None:
        if PROJECT.project().gen.linker.default_heap_size > -1:
            default_heap_size = PROJECT.project().gen.linker.default_heap_size
        elif SUMMARY.project_summary().linker.default_heap_size > -1:
            default_heap_size = SUMMARY.project_summary().linker.default_heap_size
        else:
            default_heap_size = -1
        PROJECT.project().gen.linker.default_heap_size = default_heap_size
        # --------------------------------------------------------------------------------------------------------------
        if PROJECT.project().gen.linker.default_stack_size > -1:
            default_stack_size = PROJECT.project().gen.linker.default_stack_size
        elif SUMMARY.project_summary().linker.default_stack_size > -1:
            default_stack_size = SUMMARY.project_summary().linker.default_stack_size
        else:
            default_stack_size = -1
        PROJECT.project().gen.linker.default_stack_size = default_stack_size
        # --------------------------------------------------------------------------------------------------------------

        group = SettingCardGroup(self.tr("Linker Settings"), self.widget_scroll)  # type: ignore

        # --------------------------------------------------------------------------------------------------------------
        if default_heap_size > -1:
            self.default_heap_line_edit_card = LineEditPropertySettingCard(
                icon=Icon.FOLDER,
                title=self.tr("Default Heap Size"),  # type: ignore
                value=hex(default_heap_size),
                content=hex(default_heap_size),
                validator=R"(^0x[0-9A-Fa-f]+$)",
                parent=group,
            )
            self.default_heap_line_edit_card.text_changed.connect(
                self.__on_defaultHeapLineEditCard_textChanged
            )
            PROJECT.project().gen.linker.default_heap_size_changed.connect(
                lambda old, new: self.default_heap_line_edit_card.setContent(hex(new))
            )
            group.addSettingCard(self.default_heap_line_edit_card)
        # --------------------------------------------------------------------------------------------------------------
        if default_stack_size > -1:
            self.default_stack_line_edit_card = LineEditPropertySettingCard(
                icon=Icon.FOLDER,
                title=self.tr("Default Stack Size"),  # type: ignore
                value=hex(default_stack_size),
                content=hex(default_stack_size),
                validator=R"(^0x[0-9A-Fa-f]+$)",
                parent=group,
            )
            self.default_stack_line_edit_card.text_changed.connect(
                self.__on_defaultStackLineEditCard_textChanged
            )
            PROJECT.project().gen.linker.default_stack_size_changed.connect(
                lambda old, new: self.default_stack_line_edit_card.setContent(hex(new))
            )
            group.addSettingCard(self.default_stack_line_edit_card)

        return group

    def __create_hal_group(self) -> SettingCardGroup | None:
        # --------------------------------------------------------------------------------------------------------------

        group = SettingCardGroup(self.tr("Hal Settings"), self.widget_scroll)  # type: ignore

        # --------------------------------------------------------------------------------------------------------------
        self.copy_library_switch_setting_card = SwitchPropertySettingCard(
            icon=Icon.CHECKBOX_MULTIPLE,
            title=self.tr("Copy Hal Library"),  # type: ignore
            value=PROJECT.project().gen.copy_library,
            content=self.tr("Copy the hal library files to the project directory"),  # type: ignore
            parent=group,
        )
        self.copy_library_switch_setting_card.checked_changed.connect(
            self.__on_copy_library_switch_setting_card_checked_changed
        )
        # --------------------------------------------------------------------------------------------------------------
        self.hal_combo_box_group_setting_card = ComboBoxPropertySettingCard(
            icon=Icon.HAMMER,
            title=self.tr("Hal Package"),  # type: ignore
            value="",
            values=[],
            content=" ",
            parent=group,
        )
        self.hal_combo_box_group_setting_card.current_text_changed.connect(
            self.__on_hal_combo_box_group_setting_card_current_text_changed
        )
        # --------------------------------------------------------------------------------------------------------------
        self.hal_version_combo_box_group_setting_card = ComboBoxPropertySettingCard(
            icon=Icon.DATABASE_2,
            title=self.tr("Hal Package Version"),  # type: ignore
            value="",
            values=[],
            content=" ",
            parent=group,
        )
        self.hal_version_combo_box_group_setting_card.current_text_changed.connect(
            self.__on_hal_version_combo_box_group_setting_card_current_text_changed
        )
        # --------------------------------------------------------------------------------------------------------------
        self.hal_path_tool_button_setting_card = ToolButtonPropertySettingCard(
            icon=Icon.FOLDER,
            title=self.tr("Hal Package Path"),  # type: ignore
            btn_icon=Icon.BOX,
            content=" ",
            parent=group,
        )
        self.hal_path_tool_button_setting_card.clicked.connect(
            self.__on_hal_path_tool_button_setting_card_clicked
        )
        # --------------------------------------------------------------------------------------------------------------

        group.addSettingCard(self.copy_library_switch_setting_card)
        group.addSettingCard(self.hal_combo_box_group_setting_card)
        group.addSettingCard(self.hal_version_combo_box_group_setting_card)
        group.addSettingCard(self.hal_path_tool_button_setting_card)

        return group

    def __on_defaultHeapLineEditCard_textChanged(self, text: str):
        ishex = Converters.ishex(text)
        if ishex:
            PROJECT.project().gen.linker.default_heap_size = int(text, 16)
        self.default_heap_line_edit_card.set_status_info(
            not ishex, self.tr("The Path is not directory")  # type: ignore
        )

    def __on_defaultStackLineEditCard_textChanged(self, text: str):
        ishex = Converters.ishex(text)
        if ishex:
            PROJECT.project().gen.linker.default_stack_size = int(text, 16)
        self.default_stack_line_edit_card.set_status_info(
            not ishex, self.tr("The Path is not directory")  # type: ignore
        )

    def __on_builderComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.builder = text
        self.__update_builder_version_settings()

    def __on_builderVersionComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.builder_version = text
        self.__update_toolchains_settings()

    def __on_useToolchainsPackageSwitchSettingCard_checkedChanged(self, checked: bool):
        PROJECT.project().gen.use_toolchains_package = checked
        self.toolchains_version_combo_box_group_setting_card.setEnabled(checked)
        self.toolchains_path_tool_button_setting_card.setEnabled(checked)
        if checked:
            self.__update_toolchains_version_settings()
        else:
            self.toolchains_version_combo_box_group_setting_card.clear()
            self.toolchains_path_tool_button_setting_card.clear()

    def __on_toolchainsComboBoxGroupSettingCard_currentTextChanged(self, text: str):
        PROJECT.project().gen.toolchains = text
        self.__update_toolchains_version_settings()

    def __on_toolchainsVersionComboBoxGroupSettingCard_currentTextChanged(
        self, text: str
    ):
        PROJECT.project().gen.toolchains_version = text
        self.__update_toolchains_path_settings()

    def __on_toolchainsManagerBtn_clicked(self):
        self.__navigation_to_package_view()

    def __on_toolchains_path_tool_button_setting_card_clicked(self):
        self.__navigation_to_package_view()

    def __navigation_to_package_view(self):
        SIGNAL_BUS.navigation_requested.emit("PackageView", "")

    def __update_builder_settings(self):
        if self.builder_group is None:
            return

        builder = SUMMARY.project_summary().builder
        builder_list = list(builder.keys())
        if len(builder_list) == 0:
            return

        if PROJECT.project().gen.builder == "":
            PROJECT.project().gen.builder = builder_list[-1]
        else:
            if PROJECT.project().gen.builder not in builder_list:
                logger.warning(
                    f"The builder {PROJECT.project().gen.builder} is not supported. Use default value {builder_list[-1]!r}"
                )
                PROJECT.project().gen.builder = builder_list[-1]

        self.builder_combo_box_group_setting_card.set_source(
            PROJECT.project().gen.builder, builder_list
        )
        self.builder_combo_box_group_setting_card.setContent(
            PROJECT.project().gen.builder
        )

    def __update_builder_version_settings(self):
        if self.builder_group is None:
            return

        builder_version = SUMMARY.project_summary().builder.get(
            PROJECT.project().gen.builder, {}
        )
        builder_version_list = list(
            builder_version.keys()
        )  # It must not be an empty array.

        if PROJECT.project().gen.builder_version == "":
            PROJECT.project().gen.builder_version = builder_version_list[-1]
        else:
            if PROJECT.project().gen.builder_version not in builder_version_list:
                # logger.warning(
                #     f"The builder '{PROJECT.project().gen.builder}@{PROJECT.project().gen.builderVersion}' is not supported. Use default value '{PROJECT.project().gen.builder}@{builderVersionList[-1]}'")
                PROJECT.project().gen.builder_version = builder_version_list[-1]

        self.builder_version_combo_box_group_setting_card.set_source(
            PROJECT.project().gen.builder_version, builder_version_list
        )
        self.builder_version_combo_box_group_setting_card.setContent(
            PROJECT.project().gen.builder
        )

    def __update_toolchains_settings(self):
        if self.builder_group is None:
            return

        # It must not be an empty array.
        toolchains = (
            SUMMARY.project_summary()
            .builder.get(PROJECT.project().gen.builder, {})
            .get(PROJECT.project().gen.builder_version, [])
        )
        if PROJECT.project().gen.toolchains == "":
            PROJECT.project().gen.toolchains = toolchains[-1]
        else:
            if PROJECT.project().gen.toolchains not in toolchains:
                # logger.warning(
                #     f"The builder '{PROJECT.project().gen.builder}@{PROJECT.project().gen.toolchains}' is not supported. Use default value '{PROJECT.project().gen.builder}@{toolchains[-1]}'")
                PROJECT.project().gen.toolchains = toolchains[-1]

        self.toolchains_combo_box_group_setting_card.set_source(
            PROJECT.project().gen.toolchains, toolchains
        )
        self.toolchains_combo_box_group_setting_card.setContent(
            PROJECT.project().gen.toolchains
        )

    def __update_toolchains_version_settings(self):
        if (
            self.builder_group is None
            or not PROJECT.project().gen.use_toolchains_package
        ):
            return

        toolchains_versions = PACKAGE.index().versions(
            "toolchains", PROJECT.project().gen.toolchains
        )
        if len(toolchains_versions) != 0:
            if PROJECT.project().gen.toolchains_version == "":
                PROJECT.project().gen.toolchains_version = toolchains_versions[-1]
            else:
                if PROJECT.project().gen.toolchains_version not in toolchains_versions:
                    # logger.warning(
                    #     f"The toolchains '{PROJECT.project().gen.toolchains}@{PROJECT.project().gen.toolchainsVersion}' is not supported. Use default value '{PROJECT.project().gen.toolchains}@{toolchainsVersions[-1]}'")
                    PROJECT.project().gen.toolchains_version = toolchains_versions[-1]
        else:
            logger.error(
                f"The toolchains {PROJECT.project().gen.toolchains!r} is not installed. Please install and then restart this software, You can find the corresponding package download URL here {SETTINGS.PACKAGE_LIST_URL!r}"
            )
        self.toolchains_version_combo_box_group_setting_card.set_source(
            PROJECT.project().gen.toolchains_version, toolchains_versions
        )
        self.toolchains_version_combo_box_group_setting_card.setContent(
            PROJECT.project().gen.toolchains
        )

    def __update_toolchains_path_settings(self):
        if (
            self.builder_group is None
            or not PROJECT.project().gen.use_toolchains_package
        ):
            return

        toolchains_path = PACKAGE.index().path(
            "toolchains",
            PROJECT.project().gen.toolchains,
            PROJECT.project().gen.toolchains_version,
        )

        self.toolchains_path_tool_button_setting_card.setContent(toolchains_path)
        self.toolchains_path_tool_button_setting_card.contentLabel.setToolTip(
            toolchains_path
        )
        if not os.path.isdir(toolchains_path):
            message = self.tr("The Path is not directory")  # type: ignore
            self.toolchains_path_tool_button_setting_card.set_status_info(True, message)
        else:
            self.toolchains_path_tool_button_setting_card.set_status_info(False, "")

    def __on_copy_library_switch_setting_card_checked_changed(self, checked: bool):
        PROJECT.project().gen.copy_library = checked

    def __on_hal_combo_box_group_setting_card_current_text_changed(self, text: str):
        PROJECT.project().gen.hal = text
        self.__update_hal_version_settings()

    def __on_hal_version_combo_box_group_setting_card_current_text_changed(
        self, text: str
    ):
        PROJECT.project().gen.hal_version = text
        self.__update_hal_path_settings()

    def __on_hal_path_tool_button_setting_card_clicked(self):
        self.__navigation_to_package_view()

    def __update_hal_settings(self):
        if self.hal_group is None:
            return

        hals = SUMMARY.project_summary().hals
        if len(hals) == 0:
            return

        if PROJECT.project().gen.hal == "":
            PROJECT.project().gen.hal = hals[-1]
        else:
            if PROJECT.project().gen.hal not in hals:
                logger.warning(
                    f"The hal {PROJECT.project().gen.hal!r} is not supported. Use default value {hals[-1]!r}"
                )
                PROJECT.project().gen.hal = hals[-1]

        self.hal_combo_box_group_setting_card.set_source(
            PROJECT.project().gen.hal, hals
        )
        self.hal_combo_box_group_setting_card.setContent(PROJECT.project().gen.hal)

    def __update_hal_version_settings(self):
        if self.hal_group is None:
            return

        hal_versions = PACKAGE.index().versions("hal", PROJECT.project().gen.hal)
        if len(hal_versions) != 0:
            if PROJECT.project().gen.hal_version == "":
                PROJECT.project().gen.hal_version = hal_versions[-1]
            else:
                if PROJECT.project().gen.hal_version not in hal_versions:
                    # logger.warning(
                    #     f"The hal '{PROJECT.project().gen.hal}@{PROJECT.project().gen.halVersion}' is not supported. Use default value '{PROJECT.project().gen.hal}@{halVersions[-1]}'")
                    PROJECT.project().gen.hal_version = hal_versions[-1]
        else:
            logger.error(
                f"The hal {PROJECT.project().gen.hal!r} is not installed. Please install and then restart this software. You can find the corresponding package download URL here {SETTINGS.PACKAGE_LIST_URL!r}"
            )

        self.hal_version_combo_box_group_setting_card.set_source(
            PROJECT.project().gen.hal_version, hal_versions
        )
        self.hal_version_combo_box_group_setting_card.setContent(
            PROJECT.project().gen.hal_version
        )

    def __update_hal_path_settings(self):
        if self.hal_group is None:
            return

        hal_path = PACKAGE.index().path(
            "hal", PROJECT.project().gen.hal, PROJECT.project().gen.hal_version
        )

        self.hal_path_tool_button_setting_card.setContent(hal_path)
        self.hal_path_tool_button_setting_card.contentLabel.setToolTip(hal_path)
        if not os.path.isdir(hal_path):
            message = self.tr("The Path is not directory")  # type: ignore
            self.hal_path_tool_button_setting_card.set_status_info(True, message)
        else:
            self.hal_path_tool_button_setting_card.set_status_info(False, "")


class SettingView(Ui_SettingView, QWidget):
    __navigation_views = {}

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)

        self.setting_stacked_widget = QStackedWidget(self)
        self.settingStackedWidgetCardVerticalLayout.addWidget(
            self.setting_stacked_widget
        )

        self.settingTreeCard.setFixedWidth(300)
        self.settingTree.header().setVisible(False)
        self.settingTree.selectionModel().selectionChanged.connect(
            self.__on_settingTree_selectionChanged
        )

        self.system_setting_view = SystemSettingView(self)
        self.generate_setting_view = GenerateSettingView(self)

        self.system_setting_tree_widget_item = self.__add_view(
            self.system_setting_view, Icon.LIST_SETTINGS, self.tr("System Setting")  # type: ignore
        )
        self.generate_setting_tree_widget_item = self.__add_view(
            self.generate_setting_view, Icon.AI_GENERATE, self.tr("Generate Setting")  # type: ignore
        )

        Style.SETTING_VIEW.apply(self)

        if self.system_setting_tree_widget_item is not None:
            self.settingTree.setCurrentItem(self.system_setting_tree_widget_item)

    def switch_to(self, key: str):
        if key not in self.__navigation_views:
            return

        self.settingTree.setCurrentItem(self.__navigation_views[key]["item"])

    def __add_view(
        self, view: QWidget, icon: FluentIconBase, text: str
    ) -> QTreeWidgetItem | None:
        if not view.objectName():
            raise ValueError("The object name of `view` can't be empty string.")

        if view.objectName() in self.__navigation_views:
            return None

        item = QTreeWidgetItem([text])
        item.setIcon(0, icon.icon())
        item.setData(0, Qt.ItemDataRole.StatusTipRole, view.objectName())
        self.settingTree.addTopLevelItem(item)

        self.setting_stacked_widget.addWidget(view)

        self.__navigation_views[view.objectName()] = {"view": view, "item": item}

        return item

    def __on_settingTree_selectionChanged(
        self, selected: QItemSelection, _: QItemSelection
    ):
        indexes = selected.indexes()
        if len(indexes) > 0:
            index = indexes[0]
            key = index.data(Qt.ItemDataRole.StatusTipRole)
            self.setting_stacked_widget.setCurrentWidget(
                self.__navigation_views[key]["view"]
            )
