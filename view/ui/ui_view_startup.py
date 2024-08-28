# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'view_startup.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QSizePolicy,
    QWidget)

from qfluentwidgets import SimpleCardWidget

class Ui_view_startup(object):
    def setupUi(self, view_startup):
        if not view_startup.objectName():
            view_startup.setObjectName(u"view_startup")
        view_startup.resize(400, 300)
        self.gridLayout = QGridLayout(view_startup)
        self.gridLayout.setObjectName(u"gridLayout")
        self.frame = SimpleCardWidget(view_startup)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.frame_2 = SimpleCardWidget(view_startup)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_2, 0, 1, 1, 1)

        self.frame_3 = SimpleCardWidget(view_startup)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_3, 1, 0, 1, 1)

        self.frame_4 = SimpleCardWidget(view_startup)
        self.frame_4.setObjectName(u"frame_4")
        self.frame_4.setFrameShape(QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.frame_4, 1, 1, 1, 1)


        self.retranslateUi(view_startup)

        QMetaObject.connectSlotsByName(view_startup)
    # setupUi

    def retranslateUi(self, view_startup):
        view_startup.setWindowTitle(QCoreApplication.translate("view_startup", u"view_startup", None))
    # retranslateUi

