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
# @file        soc_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import re


from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsScene,
    QVBoxLayout,
    QSplitter,
    QHBoxLayout,
    QFrame,
    QStackedWidget,
)
from loguru import logger
from qfluentwidgets import isDarkTheme, MessageBox, SimpleCardWidget, ToolButton

from common import Style, Icon, PROJECT, SETTINGS, SUMMARY, IP
from widget import (
    LQFP,
    TreeModule,
    WidgetControlManager,
    WidgetModeManager,
    GraphicsViewPanZoom,
    WidgetControlDashboard,
)


class SocView(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("SocView")

        self.__setup_ui()

        self.zoom_in_btn.pressed.connect(lambda: self.graphics_view.zoom_in(6))
        self.zoom_reset_btn.pressed.connect(lambda: self.graphics_view.rescale())
        self.zoom_out_btn.pressed.connect(lambda: self.graphics_view.zoom_out(6))

        SETTINGS.themeChanged.connect(
            lambda theme: self.__update_graphics_view_background_color()
        )

        if SUMMARY.project_summary().package != "":
            if re.match(r"^LQFP\d+$", SUMMARY.project_summary().package):
                items = LQFP().get_items(
                    PROJECT.project().vendor, PROJECT.project().target_chip
                )
            else:
                items = None
                title = self.tr("Error")  # type: ignore
                content = self.tr(  # type: ignore
                    "The package {!r} is not supported at this time.".format(
                        SUMMARY.project_summary().package
                    )
                )
                message = MessageBox(title, content, self.window())
                message.setContentCopyable(True)
                message.cancelButton.setDisabled(True)
                message.raise_()
                message.exec()

            if items is not None:
                for item in items:
                    self.graphics_scene.addItem(item)

        self.graphics_view.rescale()

        Style.SOC_VIEW.apply(self)

        self.tree_module.selection_changed.connect(
            self.__on_tree_module_selection_changed
        )
        self.widget_control_dashboard.selection_changed.connect(
            self.__on_widgetControlDashboard_selectionChanged
        )

    # region ui setup

    def __create_tree_module_view(self) -> SimpleCardWidget:
        self.tree_module_card = SimpleCardWidget(self.main_splitter)
        self.tree_module = TreeModule(self.tree_module_card)
        self.tree_module_card_layout = QHBoxLayout(self.tree_module_card)
        self.tree_module_card_layout.addWidget(self.tree_module)

        return self.tree_module_card

    def __create_manager_view(self) -> SimpleCardWidget:
        self.manager_card = SimpleCardWidget(self.main_splitter)
        self.manager_card_layout = QVBoxLayout(self.manager_card)
        self.manager_card_splitter = QSplitter(self.manager_card)
        self.manager_card_splitter.setOrientation(Qt.Orientation.Vertical)
        self.manager_card_control_stacked_widget = QStackedWidget(
            self.manager_card_splitter
        )
        self.manager_card_control_stacked_widget.setFrameShape(QFrame.Shape.NoFrame)
        self.widget_mode_manager = WidgetModeManager(self.manager_card_splitter)
        self.manager_card_splitter.addWidget(self.manager_card_control_stacked_widget)
        self.manager_card_splitter.addWidget(self.widget_mode_manager)
        self.manager_card_layout.addWidget(self.manager_card_splitter)

        self.widget_control_dashboard = WidgetControlDashboard(
            self.manager_card_control_stacked_widget
        )
        self.widget_control_manager = WidgetControlManager(
            self.manager_card_control_stacked_widget
        )
        self.manager_card_control_stacked_widget.addWidget(
            self.widget_control_dashboard
        )
        self.manager_card_control_stacked_widget.addWidget(self.widget_control_manager)

        self.manager_card_splitter.setSizes([300, 100])
        self.manager_card_splitter.setCollapsible(0, False)
        self.manager_card_splitter.setCollapsible(1, False)

        return self.manager_card

    def __create_soc_view(self) -> SimpleCardWidget:
        self.soc_card = SimpleCardWidget(self.main_splitter)
        self.soc_card_layout = QVBoxLayout(self.soc_card)
        self.graphics_view = GraphicsViewPanZoom(self.soc_card)
        self.graphics_view.setFrameShape(QFrame.Shape.NoFrame)
        self.soc_card_layout.addWidget(self.graphics_view)
        self.soc_card_tool_layout = QHBoxLayout()
        self.soc_card_layout.addLayout(self.soc_card_tool_layout)
        self.soc_card_tool_layout.setSpacing(20)
        self.zoom_in_btn = ToolButton(self.soc_card)
        self.zoom_reset_btn = ToolButton(self.soc_card)
        self.zoom_out_btn = ToolButton(self.soc_card)
        self.zoom_in_btn.setIcon(Icon.ZOOM_IN)
        self.zoom_reset_btn.setIcon(Icon.REFRESH)
        self.zoom_out_btn.setIcon(Icon.ZOOM_OUT)
        self.soc_card_tool_layout.addStretch(1)
        self.soc_card_tool_layout.addWidget(self.zoom_in_btn)
        self.soc_card_tool_layout.addWidget(self.zoom_reset_btn)
        self.soc_card_tool_layout.addWidget(self.zoom_out_btn)
        self.soc_card_tool_layout.addStretch(1)

        self.graphics_scene = QGraphicsScene(self.graphics_view)
        self.graphics_view.setScene(self.graphics_scene)

        self.__update_graphics_view_background_color()

        return self.soc_card

    def __setup_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_splitter = QSplitter(self)
        self.main_splitter.setOrientation(Qt.Orientation.Horizontal)

        self.main_splitter.addWidget(self.__create_tree_module_view())
        self.main_splitter.addWidget(self.__create_manager_view())
        self.main_splitter.addWidget(self.__create_soc_view())

        self.main_layout.addWidget(self.main_splitter)

        self.main_splitter.setSizes([100, 300, 300])
        self.main_splitter.setCollapsible(0, False)
        self.main_splitter.setCollapsible(1, False)

    # endregion

    def __update_graphics_view_background_color(self):
        self.graphics_scene.setBackgroundBrush(
            QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253)
        )

    def __on_tree_module_selection_changed(self, instance: str):
        ip = IP.project_ips().get(instance)
        if ip is None:
            logger.error(f'the ip instance:"{instance}" is invalid.')
            return

        if instance == SUMMARY.project_summary().pin_instance():
            self.widget_control_dashboard.instance = instance
            self.widget_mode_manager.set_target(instance, "")
            self.manager_card_control_stacked_widget.setCurrentWidget(
                self.widget_control_dashboard
            )
        else:
            self.widget_control_manager.set_target(instance, "")
            self.widget_mode_manager.set_target(instance, "")
            self.manager_card_control_stacked_widget.setCurrentWidget(
                self.widget_control_manager
            )

    def __on_widgetControlDashboard_selectionChanged(self, instance: str, target: str):
        self.widget_mode_manager.set_target(instance, target)
