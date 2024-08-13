# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chip_view.ui'
##
## Created by: Qt User Interface Compiler version 6.6.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QSizePolicy,
    QSpacerItem, QSplitter, QVBoxLayout, QWidget)

from qfluentwidgets import (SimpleCardWidget, ToolButton)
from widget.graphics_view_pan_zoom import GraphicsViewPanZoom
from widget.grid_mode import GridMode
from widget.grid_property_ip import GridPropertyIp
from widget.tree_module import TreeModule

class Ui_ChipView(object):
    def setupUi(self, ChipView):
        if not ChipView.objectName():
            ChipView.setObjectName(u"ChipView")
        ChipView.resize(1219, 967)
        self.verticalLayout_3 = QVBoxLayout(ChipView)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.splitter_1 = QSplitter(ChipView)
        self.splitter_1.setObjectName(u"splitter_1")
        self.splitter_1.setOrientation(Qt.Horizontal)
        self.frame = SimpleCardWidget(self.splitter_1)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget = TreeModule(self.frame)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout_2.addWidget(self.widget)

        self.splitter_1.addWidget(self.frame)
        self.frame_3 = SimpleCardWidget(self.splitter_1)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter_2 = QSplitter(self.frame_3)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Vertical)
        self.widget_gridMode = GridMode(self.splitter_2)
        self.widget_gridMode.setObjectName(u"widget_gridMode")
        self.splitter_2.addWidget(self.widget_gridMode)
        self.widget_gridPropertyIp = GridPropertyIp(self.splitter_2)
        self.widget_gridPropertyIp.setObjectName(u"widget_gridPropertyIp")
        self.splitter_2.addWidget(self.widget_gridPropertyIp)

        self.verticalLayout.addWidget(self.splitter_2)

        self.splitter_1.addWidget(self.frame_3)

        self.horizontalLayout_3.addWidget(self.splitter_1)

        self.frame_2 = SimpleCardWidget(ChipView)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.graphicsView = GraphicsViewPanZoom(self.frame_2)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setFrameShape(QFrame.NoFrame)

        self.verticalLayout_2.addWidget(self.graphicsView)

        self.widget_2 = QWidget(self.frame_2)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(463, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.toolButton_zoomIn = ToolButton(self.widget_2)
        self.toolButton_zoomIn.setObjectName(u"toolButton_zoomIn")
        self.toolButton_zoomIn.setCursor(QCursor(Qt.ArrowCursor))

        self.horizontalLayout.addWidget(self.toolButton_zoomIn)

        self.toolButton_zoomReset = ToolButton(self.widget_2)
        self.toolButton_zoomReset.setObjectName(u"toolButton_zoomReset")

        self.horizontalLayout.addWidget(self.toolButton_zoomReset)

        self.toolButton_zoomOut = ToolButton(self.widget_2)
        self.toolButton_zoomOut.setObjectName(u"toolButton_zoomOut")

        self.horizontalLayout.addWidget(self.toolButton_zoomOut)

        self.horizontalSpacer_2 = QSpacerItem(462, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.widget_2)


        self.horizontalLayout_3.addWidget(self.frame_2)

        self.horizontalLayout_3.setStretch(0, 4)
        self.horizontalLayout_3.setStretch(1, 6)

        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.retranslateUi(ChipView)

        QMetaObject.connectSlotsByName(ChipView)
    # setupUi

    def retranslateUi(self, ChipView):
        ChipView.setWindowTitle(QCoreApplication.translate("ChipView", u"ChipView", None))
        self.toolButton_zoomIn.setText("")
        self.toolButton_zoomReset.setText("")
        self.toolButton_zoomOut.setText("")
    # retranslateUi

