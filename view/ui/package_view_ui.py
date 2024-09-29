# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'package_view.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QHeaderView,
    QSizePolicy, QTreeWidgetItem, QVBoxLayout, QWidget)

from qfluentwidgets import (SimpleCardWidget, TreeWidget)

class Ui_PackageView(object):
    def setupUi(self, PackageView):
        if not PackageView.objectName():
            PackageView.setObjectName(u"PackageView")
        PackageView.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(PackageView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.packageTreeCard = SimpleCardWidget(PackageView)
        self.packageTreeCard.setObjectName(u"packageTreeCard")
        self.packageTreeCard.setFrameShape(QFrame.StyledPanel)
        self.packageTreeCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout_cardWidget_file = QVBoxLayout(self.packageTreeCard)
        self.verticalLayout_cardWidget_file.setObjectName(u"verticalLayout_cardWidget_file")
        self.packageTree = TreeWidget(self.packageTreeCard)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.packageTree.setHeaderItem(__qtreewidgetitem)
        self.packageTree.setObjectName(u"packageTree")

        self.verticalLayout_cardWidget_file.addWidget(self.packageTree)


        self.horizontalLayout.addWidget(self.packageTreeCard)

        self.packageInfoCard = SimpleCardWidget(PackageView)
        self.packageInfoCard.setObjectName(u"packageInfoCard")
        self.packageInfoCard.setFrameShape(QFrame.StyledPanel)
        self.packageInfoCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.packageInfoCard)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout.addWidget(self.packageInfoCard)


        self.retranslateUi(PackageView)

        QMetaObject.connectSlotsByName(PackageView)
    # setupUi

    def retranslateUi(self, PackageView):
        PackageView.setWindowTitle(QCoreApplication.translate("PackageView", u"PackageView", None))
    # retranslateUi

