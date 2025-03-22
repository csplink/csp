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

from PySide6.QtCore import Qt, QRegularExpression, QEvent, QCoreApplication
from PySide6.QtGui import (
    QTransform,
    QMouseEvent,
    QWheelEvent,
    QContextMenuEvent,
    QResizeEvent,
    QRegularExpressionValidator,
    QSurfaceFormat,
    QPainter,
)
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import (
    QGraphicsView,
    QGraphicsItem,
    QGraphicsSceneWheelEvent,
    QGraphicsProxyWidget,
)
from loguru import logger
from qfluentwidgets import MessageBoxBase, SubtitleLabel, LineEdit, MenuAnimationType

from common import SETTINGS
from . import EnumClockTreeWidget
from .graphics_item_pin import GraphicsItemPin


class LabelMessageBox(MessageBoxBase):

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self.titleLabel = SubtitleLabel(self.tr("Set label"), self)  # type: ignore
        self.labelLineEdit = LineEdit(self)

        self.labelLineEdit.setText(text)
        self.labelLineEdit.setPlaceholderText(self.tr("Enter the user label"))  # type: ignore
        self.labelLineEdit.setClearButtonEnabled(True)
        self.labelLineEdit.setValidator(
            QRegularExpressionValidator(QRegularExpression("^[A-Za-z_][A-Za-z0-9_]+$"))
        )

        self.viewLayout.addWidget(self.titleLabel)
        self.viewLayout.addWidget(self.labelLineEdit)

        self.yesButton.setText(self.tr("OK"))  # type: ignore
        self.cancelButton.setText(self.tr("Cancel"))  # type: ignore

        self.widget.setMinimumWidth(360)


class GraphicsViewPanZoom(QGraphicsView):
    MIN_SCALE = 0
    MAX_SCALE = 1000
    RESOLUTION = 50

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.m_scale = (self.MIN_SCALE + self.MAX_SCALE) // 2
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
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing
            | QPainter.RenderHint.TextAntialiasing
            | QPainter.RenderHint.SmoothPixmapTransform
        )
        self.viewport().setCursor(Qt.CursorShape.ArrowCursor)
        # INT_MAX = 2147483647
        # INT_MIN = -2147483648
        # self.setSceneRect(INT_MIN / 2, INT_MIN / 2, INT_MAX, INT_MAX)

    def setupMatrix(self):
        scale = math.pow(
            2, (self.m_scale - (self.MIN_SCALE + self.MAX_SCALE) / 2) / self.RESOLUTION
        )
        matrix = QTransform()
        matrix.scale(scale, scale)
        # matrix.rotate(90)

        self.setTransform(matrix)

    def mousePressEvent(self, event: QMouseEvent):
        super().mousePressEvent(event)
        # if event.button() & Qt.MouseButton.LeftButton:
        #     item = self.itemAt(event.pos())
        #     if (
        #         item is not None
        #         and item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
        #     ):
        #         if isinstance(item, GraphicsItemPin):
        #             name = item.data(GraphicsItemPin.Data.NAME_DATA.value)
        #             functionKey = item.data(GraphicsItemPin.Data.FUNCTION_DATA.value)
        #             function = str(PROJECT.project().configs.get(functionKey, "None"))
        #             seqs = function.split(":")
        #             if len(seqs) == 2:
        #                 SIGNAL_BUS.modeManagerTriggered.emit(seqs[0], name)

    def mouseReleaseEvent(self, event: QMouseEvent):
        super().mouseReleaseEvent(event)
        if event.button() & Qt.MouseButton.LeftButton:
            self.viewport().setCursor(Qt.CursorShape.ArrowCursor)

    def wheelEvent(self, event: QWheelEvent):
        item = self.itemAt(event.position().toPoint())
        # TODO: There may be a more elegant solution
        if item is not None and item.flags() == (
            QGraphicsItem.GraphicsItemFlag.ItemIsFocusable
            | QGraphicsItem.GraphicsItemFlag.ItemUsesExtendedStyleOption
            | QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges
            | QGraphicsItem.GraphicsItemFlag.ItemIsPanel
        ):
            parentItem = item.parentItem()
            if parentItem is not None and isinstance(parentItem, QGraphicsProxyWidget):
                if isinstance(parentItem.widget(), EnumClockTreeWidget):
                    QCoreApplication.sendEvent(
                        self.scene(), self.QWheelEvent2QGraphicsSceneWheelEvent(event)
                    )
                    return

        scrollAmount = event.angleDelta()
        if scrollAmount.y() > 0:
            self.zoomIn(6)
        else:
            self.zoomOut(6)

    def contextMenuEvent(self, event: QContextMenuEvent):
        super().contextMenuEvent(event)
        item = self.itemAt(event.pos())
        if item is not None and item.flags():
            if item.flags() & QGraphicsItem.GraphicsItemFlag.ItemIsFocusable:
                menu = item.data(GraphicsItemPin.Data.MENU_DATA.value)
                if menu is not None:
                    menu.exec(
                        event.globalPos(), False, MenuAnimationType.FADE_IN_DROP_DOWN
                    )

    def resizeEvent(self, event: QResizeEvent):
        super().resizeEvent(event)
        xHeight = event.size().height() - event.oldSize().height()
        if xHeight != 0:
            self.rescale()

    def QWheelEvent2QGraphicsSceneWheelEvent(
        self, event: QWheelEvent
    ) -> QGraphicsSceneWheelEvent:
        wheelEvent = QGraphicsSceneWheelEvent(QEvent.Type.GraphicsSceneWheel)
        wheelEvent.setScenePos(self.mapToScene(event.position().toPoint()))
        wheelEvent.setScreenPos(event.globalPosition().toPoint())
        wheelEvent.setButtons(event.buttons())
        wheelEvent.setModifiers(event.modifiers())
        horizontal = abs(event.angleDelta().x()) > abs(event.angleDelta().y())
        wheelEvent.setDelta(
            event.angleDelta().x() if horizontal else event.angleDelta().y()
        )
        wheelEvent.setPixelDelta(event.pixelDelta())
        wheelEvent.setPhase(event.phase())
        wheelEvent.setInverted(event.isInverted())
        wheelEvent.setOrientation(
            Qt.Orientation.Horizontal if horizontal else Qt.Orientation.Vertical
        )
        wheelEvent.setAccepted(False)
        wheelEvent.setTimestamp(event.timestamp())
        return wheelEvent

    def zoomIn(self, value: int):
        self.m_scale += value
        if self.m_scale >= self.MAX_SCALE:
            self.m_scale = self.MAX_SCALE

        self.setupMatrix()

    def zoomOut(self, value: int):
        self.m_scale -= value
        if self.m_scale <= self.MIN_SCALE:
            self.m_scale = self.MIN_SCALE

        self.setupMatrix()

    def zoom(self, value):
        if value <= 0:
            return
        self.m_scale = math.log(value, 2) * self.RESOLUTION + (
            self.MIN_SCALE + self.MAX_SCALE / 2
        )
        if self.m_scale >= self.MAX_SCALE:
            self.m_scale = self.MAX_SCALE

        if self.m_scale <= self.MIN_SCALE:
            self.m_scale = self.MIN_SCALE

        self.setupMatrix()

    def rescale(self):
        scene = self.scene()

        if scene is not None:
            sceneWidth = scene.itemsBoundingRect().width()
            sceneHeight = scene.itemsBoundingRect().height()
            viewWidth = self.width()
            viewHeight = self.height()

            if sceneWidth == 0:
                logger.error(f"the scene width is 0.")
                return

            if sceneHeight == 0:
                logger.error(f"the scene height is 0.")
                return

            scaleWidth = viewWidth / sceneWidth
            scaleHeight = viewHeight / sceneHeight

            self.centerOn(sceneWidth / 2, sceneHeight / 2)
            self.zoom(min(scaleWidth, scaleHeight))
