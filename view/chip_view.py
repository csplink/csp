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
# @file        chip_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-23     xqyjlj       initial version
#

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView

from view.ui.Ui_chip_view import Ui_chipView
from common.style import Style
from common.icon import Icon
from widget.graphics_item_chip_body import GraphicsItemChipBody


class chipView(Ui_chipView, QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.toolButtonZoomIn.setIcon(Icon.ZOOM_IN)
        self.toolButtonZoomReset.setIcon(Icon.REFRESH)
        self.toolButtonZoomOut.setIcon(Icon.ZOOM_OUT)

        # self.graphicsView.setSceneRect(sys.maxsize / 2, sys.maxsize / 2, sys.maxsize, sys.maxsize)

        scene = QGraphicsScene(self.graphicsView)

        item = GraphicsItemChipBody(2080, 2080, "TEST", "TEST", "LQFP144")
        scene.addItem(item)
        self.graphicsView.setScene(scene)

        Style.CHIP_VIEW.apply(self)
