# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'grid_property_ip.ui'
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

class Ui_GridPropertyIp(object):
    def setupUi(self, GridPropertyIp):
        if not GridPropertyIp.objectName():
            GridPropertyIp.setObjectName(u"GridPropertyIp")
        GridPropertyIp.resize(400, 300)
        self.verticalLayout = QVBoxLayout(GridPropertyIp)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.tableView_property = TableView(GridPropertyIp)
        self.tableView_property.setObjectName(u"tableView_property")

        self.verticalLayout.addWidget(self.tableView_property)


        self.retranslateUi(GridPropertyIp)

        QMetaObject.connectSlotsByName(GridPropertyIp)
    # setupUi

    def retranslateUi(self, GridPropertyIp):
        GridPropertyIp.setWindowTitle(QCoreApplication.translate("GridPropertyIp", u"GridPropertyIp", None))
    # retranslateUi

