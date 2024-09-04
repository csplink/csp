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

class Ui_viewStartup(object):
    def setupUi(self, viewStartup):
        if not viewStartup.objectName():
            viewStartup.setObjectName(u"viewStartup")
        viewStartup.resize(800, 600)
        self.gridLayout = QGridLayout(viewStartup)
        self.gridLayout.setObjectName(u"gridLayout")
        self.cardCommand = HeaderCardWidget(viewStartup)
        self.cardCommand.setObjectName(u"cardCommand")
        self.cardCommand.setFrameShape(QFrame.StyledPanel)
        self.cardCommand.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.cardCommand, 0, 0, 1, 1)

        self.cardContributors = HeaderCardWidget(viewStartup)
        self.cardContributors.setObjectName(u"cardContributors")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cardContributors.sizePolicy().hasHeightForWidth())
        self.cardContributors.setSizePolicy(sizePolicy)
        self.cardContributors.setFrameShape(QFrame.StyledPanel)
        self.cardContributors.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.cardContributors, 0, 1, 1, 1)

        self.cardProjectList = HeaderCardWidget(viewStartup)
        self.cardProjectList.setObjectName(u"cardProjectList")
        self.cardProjectList.setFrameShape(QFrame.StyledPanel)
        self.cardProjectList.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.cardProjectList, 1, 0, 1, 1)

        self.cardMore = HeaderCardWidget(viewStartup)
        self.cardMore.setObjectName(u"cardMore")
        self.cardMore.setFrameShape(QFrame.StyledPanel)
        self.cardMore.setFrameShadow(QFrame.Raised)

        self.gridLayout.addWidget(self.cardMore, 1, 1, 1, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(1, 1)
        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 1)

        self.retranslateUi(viewStartup)

        QMetaObject.connectSlotsByName(viewStartup)
    # setupUi

    def retranslateUi(self, viewStartup):
        viewStartup.setWindowTitle(QCoreApplication.translate("viewStartup", u"viewStartup", None))
    # retranslateUi

