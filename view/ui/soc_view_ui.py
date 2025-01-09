# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'soc_view.ui'
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
from widget.tree_module import TreeModule
from widget.widget_control_manager import WidgetControlManager
from widget.widget_mode_manager import WidgetModeManager

class Ui_SocView(object):
    def setupUi(self, SocView):
        if not SocView.objectName():
            SocView.setObjectName(u"SocView")
        SocView.resize(836, 547)
        self.verticalLayout_3 = QVBoxLayout(SocView)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.modulePropertySocSplitter = QSplitter(SocView)
        self.modulePropertySocSplitter.setObjectName(u"modulePropertySocSplitter")
        self.modulePropertySocSplitter.setOrientation(Qt.Horizontal)
        self.frame = SimpleCardWidget(self.modulePropertySocSplitter)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.widget = TreeModule(self.frame)
        self.widget.setObjectName(u"widget")

        self.horizontalLayout_2.addWidget(self.widget)

        self.modulePropertySocSplitter.addWidget(self.frame)
        self.frame_3 = SimpleCardWidget(self.modulePropertySocSplitter)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.modePropertySplitter = QSplitter(self.frame_3)
        self.modePropertySplitter.setObjectName(u"modePropertySplitter")
        self.modePropertySplitter.setOrientation(Qt.Vertical)
        self.gridModeWidget = WidgetControlManager(self.modePropertySplitter)
        self.gridModeWidget.setObjectName(u"gridModeWidget")
        self.modePropertySplitter.addWidget(self.gridModeWidget)
        self.widgetModeManagerWidget = WidgetModeManager(self.modePropertySplitter)
        self.widgetModeManagerWidget.setObjectName(u"widgetModeManagerWidget")
        self.modePropertySplitter.addWidget(self.widgetModeManagerWidget)

        self.verticalLayout.addWidget(self.modePropertySplitter)

        self.modulePropertySocSplitter.addWidget(self.frame_3)
        self.frame_2 = SimpleCardWidget(self.modulePropertySocSplitter)
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

        self.zoomInBtn = ToolButton(self.widget_2)
        self.zoomInBtn.setObjectName(u"zoomInBtn")
        self.zoomInBtn.setCursor(QCursor(Qt.ArrowCursor))

        self.horizontalLayout.addWidget(self.zoomInBtn)

        self.zoomResetBtn = ToolButton(self.widget_2)
        self.zoomResetBtn.setObjectName(u"zoomResetBtn")

        self.horizontalLayout.addWidget(self.zoomResetBtn)

        self.zoomOutBtn = ToolButton(self.widget_2)
        self.zoomOutBtn.setObjectName(u"zoomOutBtn")

        self.horizontalLayout.addWidget(self.zoomOutBtn)

        self.horizontalSpacer_2 = QSpacerItem(462, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.modulePropertySocSplitter.addWidget(self.frame_2)

        self.verticalLayout_3.addWidget(self.modulePropertySocSplitter)


        self.retranslateUi(SocView)

        QMetaObject.connectSlotsByName(SocView)
    # setupUi

    def retranslateUi(self, SocView):
        SocView.setWindowTitle(QCoreApplication.translate("SocView", u"SocView", None))
        self.zoomInBtn.setText("")
        self.zoomResetBtn.setText("")
        self.zoomOutBtn.setText("")
    # retranslateUi

