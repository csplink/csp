# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tree_module.ui'
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
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QHeaderView, QSizePolicy,
    QWidget)

from qfluentwidgets import TreeView

class Ui_TreeModule(object):
    def setupUi(self, TreeModule):
        if not TreeModule.objectName():
            TreeModule.setObjectName(u"TreeModule")
        TreeModule.resize(529, 481)
        self.horizontalLayout = QHBoxLayout(TreeModule)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.treeView_modules = TreeView(TreeModule)
        self.treeView_modules.setObjectName(u"treeView_modules")

        self.horizontalLayout.addWidget(self.treeView_modules)


        self.retranslateUi(TreeModule)

        QMetaObject.connectSlotsByName(TreeModule)
    # setupUi

    def retranslateUi(self, TreeModule):
        TreeModule.setWindowTitle(QCoreApplication.translate("TreeModule", u"TreeModule", None))
    # retranslateUi

