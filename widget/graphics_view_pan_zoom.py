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

from PySide6.QtCore import Qt, QRegularExpression
from PySide6.QtGui import (QTransform, QMouseEvent, QWheelEvent, QContextMenuEvent, QKeyEvent,
                           QResizeEvent, QRegularExpressionValidator, QSurfaceFormat, QPainter)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import QGraphicsView, QGraphicsItem
from loguru import logger
from qfluentwidgets import (MessageBoxBase, SubtitleLabel, LineEdit, MenuAnimationType)

from common import PROJECT, SIGNAL_BUS, SETTINGS
from .graphics_item_pin import GraphicsItemPin


class LabelMessageBox(MessageBoxBase):

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr('Set label'), self)
        self.labelLineEdit = LineEdit(self)

        self.labelLineEdit.setText(text)
        self.labelLineEdit.setPlaceholderText(self.tr('Enter the user label'))
        self.labelLineEdit.setClearButtonEnabled(True)
        self.labelLineEdit.setValidator(QRegularExpressionValidator(QRegularExpression("^[A-Za-z_][A-Za-z0-9_]+$")))

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.labelLineEdit)

        self.yesButton.setText(self.tr('OK'))
        self.cancelButton.setText(self.tr('Cancel'))

        self.widget.setMinimumWidth(360)


class GraphicsViewPanZoom(QGraphicsView):
    MIN_SCALE = 0
    MAX_SCALE = 1000
    RESOLUTION = 50
    SCALE = (MIN_SCALE + MAX_SCALE) // 2
    __key = 0

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        if SETTINGS.isUseOpenGL.value:
            self.m_opengl = QOpenGLWidget(self)
            fmt = QSurfaceFormat()
            fmt.setSamples(SETTINGS.openGLSamples.value)
            self.m_opengl.setFormat(fmt)

            self.setViewport(self.m_opengl)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setAcceptDrops(False)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setOptimizationFlags(QGraphicsView.OptimizationFlag.DontSavePainterState)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.SmartViewportUpdate)
        self.setRenderHints(QPainter.RenderHint.Antialiasing |
                            QPainter.RenderHint.TextAntialiasing |
                            QPainter.RenderHint.SmoothPixmapTransform)
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        INT_MAX = 2147483647
        INT_MIN = -2147483648
        self.setSceneRect(INT_MIN / 2, INT_MIN / 2, INT_MAX, INT_MAX)

    def setupMatrix(self):
        scale = math.pow(2, (self.SCALE - (self.MIN_SCALE + self.MAX_SCALE) / 2) / self.RESOLUTION)
        matrix = QTransform()
        matrix.scale(scale, scale)
        # matrix.rotate(90)

        self.setTransform(matrix)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        if event.button() & Qt.MouseButton.LeftButton:
            # self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
            item = self.itemAt(event.pos())
            if item is not None and item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
                if self.__key != 0:
                    if self.__key == Qt.Key.Key_Control:
                        self.__key = 0
                        key = item.data(GraphicsItemPin.Data.LABEL_DATA.value)
                        w = LabelMessageBox(PROJECT.project().configs.get(key, ""), self.window())
                        if w.exec():
                            PROJECT.project().configs.set(key, w.labelLineEdit.text())
                else:
                    name = item.data(GraphicsItemPin.Data.NAME_DATA.value)
                    function: str = PROJECT.project().configs.get(item.data(GraphicsItemPin.Data.FUNCTION_DATA.value),
                                                                  "")
                    seqs = function.split('-')
                    if len(seqs) == 2:
                        SIGNAL_BUS.gridPropertyIpTriggered.emit(seqs[0], name)
                    else:
                        logger.error(f"Function name error, {name}:{function}")

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() & Qt.MouseButton.LeftButton:
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def wheelEvent(self, event: QWheelEvent):
        # super().wheelEvent(event)
        scroll_amount = event.angleDelta()
        if scroll_amount.y() > 0:
            self.zoomIn(6)
        else:
            self.zoomOut(6)

    # def mouseDoubleClickEvent(self, event: QMouseEvent):
    #     super().mouseDoubleClickEvent(event)
    #     if event.button() & Qt.MouseButton.LeftButton:
    #         item = self.itemAt(event.pos())
    #         if item != None and item.flags():
    #             if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
    #                 key = item.data(GraphicsItemPin.Data.LABEL_KEY.value)
    #                 w = LabelMessageBox(PROJECT.config(key, ""), self.window())
    #                 if w.exec():
    #                     PROJECT.setConfig(key, w.lineEdit_label.text())

    def contextMenuEvent(self, event: QContextMenuEvent):
        super().contextMenuEvent(event)
        item = self.itemAt(event.pos())
        if item is not None and item.flags():
            if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
                menu = item.data(GraphicsItemPin.Data.MENU_DATA.value)
                if menu is not None:
                    menu.exec(event.globalPos(), False, MenuAnimationType.FADE_IN_DROP_DOWN)

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        xHeight = event.size().height() - event.oldSize().height()
        if xHeight != 0:
            self.rescale()

    def keyPressEvent(self, event: QKeyEvent):
        super().keyPressEvent(event)
        self.__key = event.key()

    def keyReleaseEvent(self, event: QKeyEvent):
        super().keyReleaseEvent(event)
        self.__key = 0

    def zoomIn(self, value: int):
        self.SCALE += value
        if self.SCALE >= self.MAX_SCALE:
            self.SCALE = self.MAX_SCALE

        self.setupMatrix()

    def zoomOut(self, value: int):
        self.SCALE -= value
        if self.SCALE <= self.MIN_SCALE:
            self.SCALE = self.MIN_SCALE

        self.setupMatrix()

    def zoom(self, value):
        self.SCALE = math.log(value, 2) * self.RESOLUTION + (self.MIN_SCALE + self.MAX_SCALE / 2)
        if self.SCALE >= self.MAX_SCALE:
            self.SCALE = self.MAX_SCALE

        if self.SCALE <= self.MIN_SCALE:
            self.SCALE = self.MIN_SCALE

        self.setupMatrix()

    def rescale(self):
        scene = self.scene()

        if scene is not None:
            sceneWidth = scene.itemsBoundingRect().width()
            sceneHeight = scene.itemsBoundingRect().height()
            viewWidth = self.width()
            viewHeight = self.height()

            scaleWidth = viewWidth / sceneWidth
            scaleHeight = viewHeight / sceneHeight

            self.centerOn(sceneWidth / 2, sceneHeight / 2)
            self.zoom(min(scaleWidth, scaleHeight))
