# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'clock_tree_view.ui'
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
    QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import ToolButton
from widget.graphics_view_pan_zoom import GraphicsViewPanZoom

class Ui_ClockTreeView(object):
    def setupUi(self, ClockTreeView):
        if not ClockTreeView.objectName():
            ClockTreeView.setObjectName(u"ClockTreeView")
        ClockTreeView.resize(986, 678)
        self.verticalLayout = QVBoxLayout(ClockTreeView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.graphicsView = GraphicsViewPanZoom(ClockTreeView)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setFrameShape(QFrame.NoFrame)

        self.verticalLayout.addWidget(self.graphicsView)

        self.widget_2 = QWidget(ClockTreeView)
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


        self.verticalLayout.addWidget(self.widget_2)


        self.retranslateUi(ClockTreeView)

        QMetaObject.connectSlotsByName(ClockTreeView)
    # setupUi

    def retranslateUi(self, ClockTreeView):
        ClockTreeView.setWindowTitle(QCoreApplication.translate("ClockTreeView", u"ClockTreeView", None))
        self.zoomInBtn.setText("")
        self.zoomResetBtn.setText("")
        self.zoomOutBtn.setText("")
    # retranslateUi

