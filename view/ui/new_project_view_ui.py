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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialogButtonBox, QFrame,
    QHeaderView, QSizePolicy, QSplitter, QVBoxLayout,
    QWidget)

from qfluentwidgets import (SimpleCardWidget, TreeView)

class Ui_NewProjectView(object):
    def setupUi(self, NewProjectView):
        if not NewProjectView.objectName():
            NewProjectView.setObjectName(u"NewProjectView")
        NewProjectView.resize(1098, 698)
        self.verticalLayout = QVBoxLayout(NewProjectView)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.splitter_2 = QSplitter(NewProjectView)
        self.splitter_2.setObjectName(u"splitter_2")
        self.splitter_2.setOrientation(Qt.Horizontal)
        self.treeView = TreeView(self.splitter_2)
        self.treeView.setObjectName(u"treeView")
        self.splitter_2.addWidget(self.treeView)
        self.socSplitter = QSplitter(self.splitter_2)
        self.socSplitter.setObjectName(u"socSplitter")
        self.socSplitter.setOrientation(Qt.Vertical)
        self.socInfoCard = SimpleCardWidget(self.socSplitter)
        self.socInfoCard.setObjectName(u"socInfoCard")
        self.socInfoCard.setFrameShape(QFrame.StyledPanel)
        self.socInfoCard.setFrameShadow(QFrame.Raised)
        self.socInfoCardVerticalLayout = QVBoxLayout(self.socInfoCard)
        self.socInfoCardVerticalLayout.setObjectName(u"socInfoCardVerticalLayout")
        self.socSplitter.addWidget(self.socInfoCard)
        self.socTableCard = SimpleCardWidget(self.socSplitter)
        self.socTableCard.setObjectName(u"socTableCard")
        self.socTableCard.setFrameShape(QFrame.StyledPanel)
        self.socTableCard.setFrameShadow(QFrame.Raised)
        self.socTableCardVerticalLayout = QVBoxLayout(self.socTableCard)
        self.socTableCardVerticalLayout.setObjectName(u"socTableCardVerticalLayout")
        self.socSplitter.addWidget(self.socTableCard)
        self.splitter_2.addWidget(self.socSplitter)

        self.verticalLayout.addWidget(self.splitter_2)

        self.buttonBox = QDialogButtonBox(NewProjectView)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(NewProjectView)

        QMetaObject.connectSlotsByName(NewProjectView)
    # setupUi

    def retranslateUi(self, NewProjectView):
        NewProjectView.setWindowTitle(QCoreApplication.translate("NewProjectView", u"NewProjectView", None))
    # retranslateUi

