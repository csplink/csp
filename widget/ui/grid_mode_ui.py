# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grid_mode.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

from widget.grid_mode_io import GridModeIo

class Ui_GridMode(object):
    def setupUi(self, GridMode):
        if not GridMode.objectName():
            GridMode.setObjectName(u"GridMode")
        GridMode.resize(400, 300)
        self.verticalLayout = QVBoxLayout(GridMode)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(GridMode)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.verticalLayout_2 = QVBoxLayout(self.page_1)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.widget_gridModeIo = GridModeIo(self.page_1)
        self.widget_gridModeIo.setObjectName(u"widget_gridModeIo")

        self.verticalLayout_2.addWidget(self.widget_gridModeIo)

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.verticalLayout.addWidget(self.stackedWidget)


        self.retranslateUi(GridMode)

        QMetaObject.connectSlotsByName(GridMode)
    # setupUi

    def retranslateUi(self, GridMode):
        GridMode.setWindowTitle(QCoreApplication.translate("GridMode", u"GridMode", None))
    # retranslateUi

