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

        self.__setupUi()

        self.zoomInBtn.pressed.connect(lambda: self.graphicsView.zoomIn(6))
        self.zoomResetBtn.pressed.connect(lambda: self.graphicsView.rescale())
        self.zoomOutBtn.pressed.connect(lambda: self.graphicsView.zoomOut(6))

        SETTINGS.themeChanged.connect(
            lambda theme: self.__updateGraphicsViewBackgroundColor()
        )

        if SUMMARY.projectSummary().package != "":
            if re.match(r"^LQFP\d+$", SUMMARY.projectSummary().package):
                items = LQFP().getItems(
                    PROJECT.project().vendor, PROJECT.project().targetChip
                )
            else:
                items = None
                title = self.tr("Error")  # type: ignore
                content = self.tr(  # type: ignore
                    "The package {!r} is not supported at this time.".format(
                        SUMMARY.projectSummary().package
                    )
                )
                message = MessageBox(title, content, self.window())
                message.setContentCopyable(True)
                message.cancelButton.setDisabled(True)
                message.raise_()
                message.exec()

            if items is not None:
                for item in items:
                    self.graphicsScene.addItem(item)

        self.graphicsView.rescale()

        Style.SOC_VIEW.apply(self)

        self.treeModule.selectionChanged.connect(self.__on_treeModule_selectionChanged)
        self.widgetControlDashboard.selectionChanged.connect(
            self.__on_widgetControlDashboard_selectionChanged
        )

    # region ui setup

    def __createTreeModuleView(self) -> SimpleCardWidget:
        self.treeModuleCard = SimpleCardWidget(self.mainSplitter)
        self.treeModule = TreeModule(self.treeModuleCard)
        self.treeModuleCardLayout = QHBoxLayout(self.treeModuleCard)
        self.treeModuleCardLayout.addWidget(self.treeModule)

        return self.treeModuleCard

    def __createManagerView(self) -> SimpleCardWidget:
        self.managerCard = SimpleCardWidget(self.mainSplitter)
        self.managerCardLayout = QVBoxLayout(self.managerCard)
        self.managerCardSplitter = QSplitter(self.managerCard)
        self.managerCardSplitter.setOrientation(Qt.Orientation.Vertical)
        self.managerCardControlStackedWidget = QStackedWidget(self.managerCardSplitter)
        self.managerCardControlStackedWidget.setFrameShape(QFrame.Shape.NoFrame)
        self.widgetModeManager = WidgetModeManager(self.managerCardSplitter)
        self.managerCardSplitter.addWidget(self.managerCardControlStackedWidget)
        self.managerCardSplitter.addWidget(self.widgetModeManager)
        self.managerCardLayout.addWidget(self.managerCardSplitter)

        self.widgetControlDashboard = WidgetControlDashboard(
            self.managerCardControlStackedWidget
        )
        self.widgetControlManager = WidgetControlManager(
            self.managerCardControlStackedWidget
        )
        self.managerCardControlStackedWidget.addWidget(self.widgetControlDashboard)
        self.managerCardControlStackedWidget.addWidget(self.widgetControlManager)

        self.managerCardSplitter.setSizes([300, 100])
        self.managerCardSplitter.setCollapsible(0, False)
        self.managerCardSplitter.setCollapsible(1, False)

        return self.managerCard

    def __createSocView(self) -> SimpleCardWidget:
        self.socCard = SimpleCardWidget(self.mainSplitter)
        self.socCardLayout = QVBoxLayout(self.socCard)
        self.graphicsView = GraphicsViewPanZoom(self.socCard)
        self.graphicsView.setFrameShape(QFrame.Shape.NoFrame)
        self.socCardLayout.addWidget(self.graphicsView)
        self.socCardToolLayout = QHBoxLayout()
        self.socCardLayout.addLayout(self.socCardToolLayout)
        self.socCardToolLayout.setSpacing(20)
        self.zoomInBtn = ToolButton(self.socCard)
        self.zoomResetBtn = ToolButton(self.socCard)
        self.zoomOutBtn = ToolButton(self.socCard)
        self.zoomInBtn.setIcon(Icon.ZOOM_IN)
        self.zoomResetBtn.setIcon(Icon.REFRESH)
        self.zoomOutBtn.setIcon(Icon.ZOOM_OUT)
        self.socCardToolLayout.addStretch(1)
        self.socCardToolLayout.addWidget(self.zoomInBtn)
        self.socCardToolLayout.addWidget(self.zoomResetBtn)
        self.socCardToolLayout.addWidget(self.zoomOutBtn)
        self.socCardToolLayout.addStretch(1)

        self.graphicsScene = QGraphicsScene(self.graphicsView)
        self.graphicsView.setScene(self.graphicsScene)

        self.__updateGraphicsViewBackgroundColor()

        return self.socCard

    def __setupUi(self):
        self.mainLayout = QVBoxLayout(self)
        self.mainSplitter = QSplitter(self)
        self.mainSplitter.setOrientation(Qt.Orientation.Horizontal)

        self.mainSplitter.addWidget(self.__createTreeModuleView())
        self.mainSplitter.addWidget(self.__createManagerView())
        self.mainSplitter.addWidget(self.__createSocView())

        self.mainLayout.addWidget(self.mainSplitter)

        self.mainSplitter.setSizes([100, 300, 300])
        self.mainSplitter.setCollapsible(0, False)
        self.mainSplitter.setCollapsible(1, False)

    # endregion

    def __updateGraphicsViewBackgroundColor(self):
        self.graphicsScene.setBackgroundBrush(
            QColor(50, 50, 50) if isDarkTheme() else QColor(253, 253, 253)
        )

    def __on_treeModule_selectionChanged(self, instance: str):
        ip = IP.projectIps().get(instance)
        if ip is None:
            logger.error(f'the ip instance:"{instance}" is invalid.')
            return

        if instance == SUMMARY.projectSummary().pinInstance():
            self.widgetControlDashboard.instance = instance
            self.widgetModeManager.setTarget(instance, "")
            self.managerCardControlStackedWidget.setCurrentWidget(
                self.widgetControlDashboard
            )
        else:
            self.widgetControlManager.setTarget(instance, "")
            self.widgetModeManager.setTarget(instance, "")
            self.managerCardControlStackedWidget.setCurrentWidget(
                self.widgetControlManager
            )

    def __on_widgetControlDashboard_selectionChanged(self, instance: str, target: str):
        self.widgetModeManager.setTarget(instance, target)
