# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_project_view.ui'
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
    QSizePolicy, QSplitter, QStackedWidget, QVBoxLayout,
    QWidget)

from qfluentwidgets import (Pivot, TableView, TreeView)

class Ui_NewProjectView(object):
    def setupUi(self, NewProjectView):
        if not NewProjectView.objectName():
            NewProjectView.setObjectName(u"NewProjectView")
        NewProjectView.resize(1098, 698)
        self.verticalLayout = QVBoxLayout(NewProjectView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.mainSplitter = QSplitter(NewProjectView)
        self.mainSplitter.setObjectName(u"mainSplitter")
        self.mainSplitter.setOrientation(Qt.Horizontal)
        self.treeView = TreeView(self.mainSplitter)
        self.treeView.setObjectName(u"treeView")
        self.mainSplitter.addWidget(self.treeView)
        self.socSplitter = QSplitter(self.mainSplitter)
        self.socSplitter.setObjectName(u"socSplitter")
        self.socSplitter.setOrientation(Qt.Vertical)
        self.socInfoCard = QFrame(self.socSplitter)
        self.socInfoCard.setObjectName(u"socInfoCard")
        self.socInfoCard.setFrameShape(QFrame.NoFrame)
        self.socInfoCard.setFrameShadow(QFrame.Raised)
        self.socInfoCardVerticalLayout = QVBoxLayout(self.socInfoCard)
        self.socInfoCardVerticalLayout.setObjectName(u"socInfoCardVerticalLayout")
        self.socInfoCardVerticalLayout.setContentsMargins(9, 9, 9, 9)
        self.tabBar = Pivot(self.socInfoCard)
        self.tabBar.setObjectName(u"tabBar")

        self.socInfoCardVerticalLayout.addWidget(self.tabBar)

        self.stackedWidget = QStackedWidget(self.socInfoCard)
        self.stackedWidget.setObjectName(u"stackedWidget")

        self.socInfoCardVerticalLayout.addWidget(self.stackedWidget)

        self.socSplitter.addWidget(self.socInfoCard)
        self.socTableCard = QFrame(self.socSplitter)
        self.socTableCard.setObjectName(u"socTableCard")
        self.socTableCard.setFrameShape(QFrame.NoFrame)
        self.socTableCard.setFrameShadow(QFrame.Raised)
        self.socTableCardVerticalLayout = QVBoxLayout(self.socTableCard)
        self.socTableCardVerticalLayout.setObjectName(u"socTableCardVerticalLayout")
        self.socTableCardVerticalLayout.setContentsMargins(9, 9, 9, 9)
        self.tableView = TableView(self.socTableCard)
        self.tableView.setObjectName(u"tableView")

        self.socTableCardVerticalLayout.addWidget(self.tableView)

        self.socSplitter.addWidget(self.socTableCard)
        self.mainSplitter.addWidget(self.socSplitter)

        self.verticalLayout.addWidget(self.mainSplitter)

        self.btnGroup = QFrame(NewProjectView)
        self.btnGroup.setObjectName(u"btnGroup")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnGroup.sizePolicy().hasHeightForWidth())
        self.btnGroup.setSizePolicy(sizePolicy)
        self.btnGroup.setFrameShape(QFrame.NoFrame)
        self.btnGroup.setFrameShadow(QFrame.Raised)
        self.btnGroupHorizontalLayout = QHBoxLayout(self.btnGroup)
        self.btnGroupHorizontalLayout.setObjectName(u"btnGroupHorizontalLayout")
        self.btnGroupHorizontalLayout.setContentsMargins(0, 9, 0, 9)

        self.verticalLayout.addWidget(self.btnGroup)


        self.retranslateUi(NewProjectView)

        QMetaObject.connectSlotsByName(NewProjectView)
    # setupUi

    def retranslateUi(self, NewProjectView):
        NewProjectView.setWindowTitle(QCoreApplication.translate("NewProjectView", u"NewProjectView", None))
    # retranslateUi

