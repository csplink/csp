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

import math

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QTransform, QMouseEvent, QWheelEvent, QSurfaceFormat, QContextMenuEvent
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QOpenGLWidget, QMenu

from widget.graphics_item_pin import GraphicsItemPin


class GraphicsViewPanZoom(QGraphicsView):
    selectedItemClicked = pyqtSignal(QGraphicsItem)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.m_min_scale = 0
        self.m_max_scale = 1000
        self.m_resolution = 50
        self.m_scale = (self.m_min_scale + self.m_max_scale) / 2
        self.m_pressed = False

        self.m_opengl = QOpenGLWidget(self)
        fmt = QSurfaceFormat()
        fmt.setSamples(10)
        self.m_opengl.setFormat(fmt)

        self.setViewport(self.m_opengl)
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
        INT_MAX = 2147483647
        INT_MIN = -2147483648
        self.setSceneRect(INT_MIN / 2, INT_MIN / 2, INT_MAX, INT_MAX)

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
                self.selectedItemClicked.emit(item)

    def mouseMoveEvent(self, event: QMouseEvent):
        super().mouseMoveEvent(event)
        if self.m_pressed:
            self.viewport().setCursor(Qt.CursorShape.ClosedHandCursor)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        self.m_pressed = False
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def wheelEvent(self, event: QWheelEvent):
        # super().wheelEvent(event)
        scroll_amount = event.angleDelta()
        if scroll_amount.y() > 0:
            self.zoomIn(6)
        else:
            self.zoomOut(6)

    def contextMenuEvent(self, event: QContextMenuEvent):
        super().contextMenuEvent(event)
        item = self.itemAt(event.pos())
        if item != None and item.flags():
            if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
                menu = item.data(GraphicsItemPin.Data.MENU.value)
                if menu != None:
                    menu.exec(event.globalPos())

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

    def zoom(self, value):
        self.m_scale = math.log(value, 2) * self.m_resolution + (self.m_min_scale + self.m_max_scale / 2)
        if (self.m_scale >= self.m_max_scale):
            self.m_scale = self.m_max_scale

        if (self.m_scale <= self.m_min_scale):
            self.m_scale = self.m_min_scale

        self.setupMatrix()

    def resize(self):
        graphicsScene = self.scene()
        if (graphicsScene != None):

            graphicsSceneWidth = graphicsScene.itemsBoundingRect().width()
            graphicsSceneHeight = graphicsScene.itemsBoundingRect().height()
            viewWidth = self.width()
            viewHeight = self.height()
            sceneMax = graphicsSceneWidth if graphicsSceneWidth > graphicsSceneHeight else graphicsSceneHeight
            viewMin = viewHeight if viewWidth > viewHeight else viewWidth
            scale = viewMin / sceneMax

            self.centerOn(graphicsSceneWidth / 2, graphicsSceneHeight / 2)
            self.zoom(scale)
