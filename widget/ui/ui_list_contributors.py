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

class Ui_list_contributors(object):
    def setupUi(self, list_contributors):
        if not list_contributors.objectName():
            list_contributors.setObjectName(u"list_contributors")
        list_contributors.resize(400, 300)
        self.verticalLayout = QVBoxLayout(list_contributors)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.scroll_area = ScrollArea(list_contributors)
        self.scroll_area.setObjectName(u"scroll_area")
        self.scroll_area.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 398, 298))
        self.scroll_area.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scroll_area)


        self.retranslateUi(list_contributors)

        QMetaObject.connectSlotsByName(list_contributors)
    # setupUi

    def retranslateUi(self, list_contributors):
        list_contributors.setWindowTitle(QCoreApplication.translate("list_contributors", u"list_contributors", None))
    # retranslateUi

