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

from qfluentwidgets import HeaderCardWidget

class Ui_view_startup(object):
    def setupUi(self, view_startup):
        if not view_startup.objectName():
            view_startup.setObjectName(u"view_startup")
        view_startup.resize(400, 300)
        self.gridLayout = QGridLayout(view_startup)
        self.gridLayout.setObjectName(u"gridLayout")
        self.card_command = HeaderCardWidget(view_startup)
        self.card_command.setObjectName(u"card_command")
        self.card_command.setFrameShape(QFrame.StyledPanel)
        self.card_command.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.card_command, 0, 0, 1, 1)

        self.card_developer = HeaderCardWidget(view_startup)
        self.card_developer.setObjectName(u"card_developer")
        self.card_developer.setFrameShape(QFrame.StyledPanel)
        self.card_developer.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.card_developer, 0, 1, 1, 1)

        self.card_project_list = HeaderCardWidget(view_startup)
        self.card_project_list.setObjectName(u"card_project_list")
        self.card_project_list.setFrameShape(QFrame.StyledPanel)
        self.card_project_list.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.card_project_list, 1, 0, 1, 1)

        self.card_more = HeaderCardWidget(view_startup)
        self.card_more.setObjectName(u"card_more")
        self.card_more.setFrameShape(QFrame.StyledPanel)
        self.card_more.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.card_more, 1, 1, 1, 1)


        self.retranslateUi(view_startup)

        QMetaObject.connectSlotsByName(view_startup)
    # setupUi

    def retranslateUi(self, view_startup):
        view_startup.setWindowTitle(QCoreApplication.translate("view_startup", u"view_startup", None))
    # retranslateUi

