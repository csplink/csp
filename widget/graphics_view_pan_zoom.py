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
# @file        graphics_view_pan_zoom.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-24     xqyjlj       initial version
#

import math, sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtOpenGL import QGLWidget, QGLFormat, QGL
from PyQt5.QtGui import QPainter, QTransform, QMouseEvent, QWheelEvent, QSurfaceFormat
from PyQt5.QtWidgets import QWidget, QGraphicsScene, QGraphicsView, QGraphicsItem, QOpenGLWidget


class GraphicsViewPanZoom(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.signalsSelectedItemClicked = pyqtSignal(QGraphicsItem)

        self.m_min_scale = 0
        self.m_max_scale = 1000
        self.m_resolution = 50
        self.m_scale = (self.m_min_scale + self.m_max_scale) / 2
        self.m_pressed = False

        # self.m_opengl = QOpenGLWidget(self)
        # fmt = QSurfaceFormat()
        # fmt.setSamples(10)
        # self.m_opengl.setFormat(fmt)

        # self.setViewport(self.m_opengl)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setInteractive(False)
        self.setAcceptDrops(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setOptimizationFlags(QGraphicsView.OptimizationFlag.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setRenderHints(QPainter.RenderHint.Antialiasing | QPainter.RenderHint.TextAntialiasing
                            | QPainter.RenderHint.SmoothPixmapTransform
                            | QPainter.RenderHint.Qt4CompatiblePainting
                            | QPainter.RenderHint.LosslessImageRendering)
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        # self.setSceneRect(4000 / 2, 4000 / 2, 4000, 4000)
        # self.setSceneRect(sys.maxsize / 2, sys.maxsize / 2, sys.maxsize, sys.maxsize)

    def setupMatrix(self):
        scale = math.pow(2, (self.m_scale - (self.m_min_scale + self.m_max_scale) / 2) / self.m_resolution)
        matrix = QTransform()
        matrix.scale(scale, scale)
        # matrix.rotate(90)

        self.setTransform(matrix)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        self.m_pressed = True
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

        item = self.itemAt(event.pos())
        if item != None:
            if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
                self.signalsSelectedItemClicked.emit()

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if self.m_pressed:
            self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        self.m_pressed = False
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def wheelEvent(self, event: QWheelEvent):
        scroll_amount = event.angleDelta()
        if scroll_amount.y() > 0:
            self.zoomIn(6)
        else:

            self.zoomOut(6)

    def zoomIn(self, value: int):
        self.m_scale += value
        if self.m_scale >= self.m_max_scale:
            self.m_scale = self.m_max_scale

        self.setupMatrix()

    def zoomOut(self, value: int):
        self.m_scale -= value
        if self.m_scale <= self.m_min_scale:
            self.m_scale = self.m_min_scale

        self.setupMatrix()
