# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'setting_view.ui'
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
    QSizePolicy, QStackedWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

from qfluentwidgets import (SimpleCardWidget, TreeWidget)

class Ui_SettingView(object):
    def setupUi(self, SettingView):
        if not SettingView.objectName():
            SettingView.setObjectName(u"SettingView")
        SettingView.resize(400, 300)
        self.horizontalLayout = QHBoxLayout(SettingView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.settingTreeCard = SimpleCardWidget(SettingView)
        self.settingTreeCard.setObjectName(u"settingTreeCard")
        self.settingTreeCard.setFrameShape(QFrame.StyledPanel)
        self.settingTreeCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout_cardWidget_file = QVBoxLayout(self.settingTreeCard)
        self.verticalLayout_cardWidget_file.setObjectName(u"verticalLayout_cardWidget_file")
        self.settingTree = TreeWidget(self.settingTreeCard)
        __qtreewidgetitem = QTreeWidgetItem()
        __qtreewidgetitem.setText(0, u"1");
        self.settingTree.setHeaderItem(__qtreewidgetitem)
        self.settingTree.setObjectName(u"settingTree")

        self.verticalLayout_cardWidget_file.addWidget(self.settingTree)


        self.horizontalLayout.addWidget(self.settingTreeCard)

        self.frame_2 = SimpleCardWidget(SettingView)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.settingStackedWidget = QStackedWidget(self.frame_2)
        self.settingStackedWidget.setObjectName(u"settingStackedWidget")

        self.verticalLayout.addWidget(self.settingStackedWidget)


        self.horizontalLayout.addWidget(self.frame_2)


        self.retranslateUi(SettingView)

        QMetaObject.connectSlotsByName(SettingView)
    # setupUi

    def retranslateUi(self, SettingView):
        SettingView.setWindowTitle(QCoreApplication.translate("SettingView", u"SettingView", None))
    # retranslateUi

