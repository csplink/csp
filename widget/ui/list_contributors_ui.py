# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'list_contributors.ui'
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
from PySide6.QtWidgets import (QApplication, QSizePolicy, QVBoxLayout, QWidget)

from qfluentwidgets import ScrollArea

class Ui_ListContributors(object):
    def setupUi(self, ListContributors):
        if not ListContributors.objectName():
            ListContributors.setObjectName(u"ListContributors")
        ListContributors.resize(400, 300)
        self.verticalLayout = QVBoxLayout(ListContributors)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = ScrollArea(ListContributors)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 398, 298))
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)


        self.retranslateUi(ListContributors)

        QMetaObject.connectSlotsByName(ListContributors)
    # setupUi

    def retranslateUi(self, ListContributors):
        ListContributors.setWindowTitle(QCoreApplication.translate("ListContributors", u"ListContributors", None))
    # retranslateUi

