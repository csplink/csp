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

from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import (QPainter, QTransform, QMouseEvent, QWheelEvent, QSurfaceFormat, QContextMenuEvent,
                         QResizeEvent, QRegExpValidator)
from PyQt5.QtWidgets import QGraphicsView, QGraphicsItem, QOpenGLWidget

from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit)

from .graphics_item_pin import GraphicsItemPin
from common import PROJECT


class CommentMessageBox(MessageBoxBase):

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr('Set label'), self)
        self.labelLineEdit = LineEdit(self)

        self.labelLineEdit.setText(text)
        self.labelLineEdit.setPlaceholderText(self.tr('Enter the user label'))
        self.labelLineEdit.setClearButtonEnabled(True)
        self.labelLineEdit.setValidator(QRegExpValidator(QRegExp("^[A-Za-z_][A-Za-z0-9_]+$")))

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.labelLineEdit)

        self.widget.setMinimumWidth(360)


class GraphicsViewPanZoom(QGraphicsView):
    selectedItemClicked = pyqtSignal(QGraphicsItem)
    resize_cnt = 0

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

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        item = self.itemAt(event.pos())
        if item != None and item.flags():
            if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
                key = item.data(GraphicsItemPin.Data.LABEL.value)
                w = CommentMessageBox(PROJECT.config(key, ""), self.window())
                if w.exec():
                    PROJECT.setConfig(key, w.labelLineEdit.text())

    def contextMenuEvent(self, event: QContextMenuEvent):
        super().contextMenuEvent(event)
        item = self.itemAt(event.pos())
        if item != None and item.flags():
            if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
                menu = item.data(GraphicsItemPin.Data.MENU.value)
                if menu != None:
                    menu.exec(event.globalPos())

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        if self.resize_cnt < 3:
            self.resize_cnt += 1
            self.resize()

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
        graphics_scene = self.scene()

        if (graphics_scene != None):
            graphics_scene_width = graphics_scene.itemsBoundingRect().width()
            graphics_scene_height = graphics_scene.itemsBoundingRect().height()
            view_width = self.width()
            view_height = self.height()
            scene_max = graphics_scene_width if graphics_scene_width > graphics_scene_height else graphics_scene_height
            view_min = view_height if view_width > view_height else view_width
            if scene_max == 0:
                return

            scale = view_min / scene_max

            self.centerOn(graphics_scene_width / 2, graphics_scene_height / 2)
            self.zoom(scale)
