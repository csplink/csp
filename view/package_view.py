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
# @file        package_view.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-09-23     xqyjlj       initial version
#

import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QCoreApplication, Signal, QPoint, QRect, QSize, QEvent, QObject
from PySide6.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QLayout, QLayoutItem
from qfluentwidgets import (ScrollArea, ExpandGroupSettingCard, PushButton, TransparentToolButton,
                            IconInfoBadge, InfoBadgePosition, RoundMenu, Action)

from common import Style, Icon, PACKAGE


class ExpandLayout(QLayout):
    """ Expand layout """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.__items = []
        self.__widgets = []

    def addWidget(self, widget: QWidget):
        if widget in self.__widgets:
            return
        self.__widgets.append(widget)
        widget.installEventFilter(self)

    def clear(self):
        while len(self.__widgets) > 0:
            widget: QWidget = self.__widgets.pop()
            widget.hide()
            widget.deleteLater()

    def addItem(self, item: QLayoutItem):
        self.__items.append(item)

    def count(self) -> int:
        return len(self.__items)

    def itemAt(self, index: int) -> QLayoutItem:
        if 0 <= index < len(self.__items):
            return self.__items[index]

        return None

    def takeAt(self, index) -> QLayoutItem:
        if 0 <= index < len(self.__items):
            self.__widgets.pop(index)
            return self.__items.pop(index)

        return None

    def expandingDirections(self) -> Qt.Orientation:
        return Qt.Orientation.Vertical

    def hasHeightForWidth(self) -> bool:
        return True

    def heightForWidth(self, width) -> int:
        """ get the minimal height according to width """
        return self.__doLayout(QRect(0, 0, width, 0), False)

    def setGeometry(self, rect: QRect):
        super().setGeometry(rect)
        self.__doLayout(rect, True)

    def sizeHint(self) -> QSize:
        return self.minimumSize()

    def minimumSize(self) -> QSize:
        size = QSize()

        for w in self.__widgets:
            size = size.expandedTo(w.minimumSize())

        m = self.contentsMargins()
        size += QSize(m.left() + m.right(), m.top() + m.bottom())

        return size

    def __doLayout(self, rect: QRect, move: bool) -> int:
        """ adjust widgets position according to the window size """
        margin = self.contentsMargins()
        x = rect.x() + margin.left()
        y = rect.y() + margin.top()
        width = rect.width() - margin.left() - margin.right()

        for i, w in enumerate(self.__widgets):
            if w.isHidden():
                continue

            y += (i > 0) * self.spacing()
            if move:
                w.setGeometry(QRect(QPoint(x, y), QSize(width, w.height())))

            y += w.height()

        return y - rect.y()

    def eventFilter(self, obj: QObject, e: QEvent):
        if obj in self.__widgets:
            if e.type() == QEvent.Resize:
                ds = e.size() - e.oldSize()  # type:QSize
                if ds.height() != 0 and ds.width() == 0:
                    w = self.parentWidget()
                    w.resize(w.width(), w.height() + ds.height())

        return super().eventFilter(obj, e)


class VersionInfoWidget(QWidget):
    flushed = Signal()

    def __init__(self, kind: str, name: str, version: str, date: str | None, existed: bool, parent=None):
        super().__init__(parent=parent)
        self.__path = PACKAGE.path(kind, name, version)
        self.__version = version
        self.__kind = kind
        self.__name = name
        self.versionLabel = QLabel(version, self)
        self.pathLabel = QLabel(self.__path or '', self)
        self.pathLabel.setToolTip(self.__path)
        self.pathLabel.setObjectName('pathLabel')
        self.dateLabel = QLabel(date or '', self)
        self.detailBtn = PushButton(QCoreApplication.translate("VersionInfoWidget", "Detail"), self)
        self.menuBtn = TransparentToolButton(Icon.MORE, self)
        self.menuBtn.clicked.connect(lambda: self.__createMenu().exec(
            self.menuBtn.mapToGlobal(QPoint(0, self.menuBtn.height())), ani=True))
        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(70)

        Style.PACKAGE_VIEW.apply(self)

        path = self.pathLabel.fontMetrics().elidedText(self.__path, Qt.TextElideMode.ElideRight, 600)
        self.pathLabel.setText(path)

        # initialize layout
        self.hBoxLayout.setSpacing(0)
        self.hBoxLayout.setContentsMargins(16, 0, 0, 0)
        self.hBoxLayout.setAlignment(Qt.AlignVCenter)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)

        self.hBoxLayout.addLayout(self.vBoxLayout)
        self.vBoxLayout.addWidget(self.versionLabel, 0, Qt.AlignLeft)
        self.vBoxLayout.addWidget(self.pathLabel, 0, Qt.AlignLeft)

        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)

        self.hBoxLayout.addWidget(self.dateLabel, 1, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)
        self.hBoxLayout.addStretch(1)

        self.hBoxLayout.addWidget(self.detailBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.hBoxLayout.addWidget(self.menuBtn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(16)

        self.badge = IconInfoBadge.error(icon=Icon.CLOSE_LARGE,
                                         parent=self.pathLabel.parent(),
                                         target=self.pathLabel,
                                         position=InfoBadgePosition.TOP_RIGHT)
        if not existed:
            self.detailBtn.hide()
            self.dateLabel.hide()
            self.menuBtn.hide()
            self.setToolTip(QCoreApplication.translate('VersionInfoWidget', 'The package not found'))
        else:
            self.badge.hide()

    def __createMenu(self) -> RoundMenu:
        menu = RoundMenu(parent=self)

        self.uninstallAction = Action(Icon.UNINSTALL, QCoreApplication.translate("VersionInfoWidget", 'Uninstall'))
        self.uninstallAction.triggered.connect(self.__uninstallPackage)
        menu.addAction(self.uninstallAction)

        return menu

    def __uninstallPackage(self):
        status = PACKAGE.uninstall(self.__kind, self.__name, self.__version)
        if not status:
            pass
        self.flushed.emit()


class PackageView(ScrollArea):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("PackageView")

        # setting label
        self.titleLabel = QLabel(QCoreApplication.translate("PackageView", "Package"), self)
        self.titleLabel.setObjectName('titleLabel')
        self.titleLabel.move(36, 30)

        self.widgetScroll = QWidget()
        self.widgetScroll.setObjectName('widgetScroll')

        self.resize(1000, 800)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setViewportMargins(0, 80, 0, 20)
        self.setWidget(self.widgetScroll)
        self.setWidgetResizable(True)

        self.expandLayout = ExpandLayout(self.widgetScroll)
        self.expandLayout.setSpacing(28)
        self.expandLayout.setContentsMargins(36, 10, 36, 0)

        # self.flush()

        self.enableTransparentBackground()

        Style.PACKAGE_VIEW.apply(self)

    def flush(self):
        self.expandLayout.clear()
        groups = self.__createGroups("toolchains")
        for group in groups:
            self.expandLayout.addWidget(group)
        self.widgetScroll.setLayout(self.expandLayout)

    def __createGroups(self, kind: str):
        groups = []
        package = PACKAGE.index.origin.get(kind, {})
        for name, value in package.items():
            group = ExpandGroupSettingCard(Icon.FOLDER.icon(), name, "", self.widgetScroll)
            for version, path in value.items():
                pdsc = PACKAGE.getPackageDescription(path)
                if pdsc is not None:
                    path_info = Path(path)
                    time = datetime.datetime.fromtimestamp(path_info.stat().st_mtime).strftime('%Y/%m/%d')
                    time = QCoreApplication.translate("PackageView", "Install time: %1").replace("%1", time)
                    info = VersionInfoWidget(kind, name, version, time, True, group)
                else:
                    info = VersionInfoWidget(kind, name, version, None, False, group)
                group.addGroupWidget(info)
            groups.append(group)
        return groups
