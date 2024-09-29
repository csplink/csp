# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grid_mode_io.ui'
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
from PySide6.QtWidgets import (QApplication, QHeaderView, QSizePolicy, QVBoxLayout,
    QWidget)

from qfluentwidgets import TableView

class Ui_GridModeIo(object):
    def setupUi(self, GridModeIo):
        if not GridModeIo.objectName():
            GridModeIo.setObjectName(u"GridModeIo")
        GridModeIo.resize(654, 355)
        self.verticalLayout = QVBoxLayout(GridModeIo)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.tableView_io = TableView(GridModeIo)
        self.tableView_io.setObjectName(u"tableView_io")

        self.verticalLayout.addWidget(self.tableView_io)


        self.retranslateUi(GridModeIo)

        QMetaObject.connectSlotsByName(GridModeIo)
    # setupUi

    def retranslateUi(self, GridModeIo):
        GridModeIo.setWindowTitle(QCoreApplication.translate("GridModeIo", u"GridModeIo", None))
    # retranslateUi

