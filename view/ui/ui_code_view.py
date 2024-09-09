# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'code_view.ui'
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
    QPlainTextEdit, QSizePolicy, QStackedWidget, QTreeWidgetItem,
    QVBoxLayout, QWidget)

from qfluentwidgets import (SimpleCardWidget, TreeWidget)
from widget.plain_text_edit_code import PlainTextEditCode

class Ui_CodeView(object):
    def setupUi(self, CodeView):
        if not CodeView.objectName():
            CodeView.setObjectName(u"CodeView")
        CodeView.resize(790, 567)
        self.horizontalLayout = QHBoxLayout(CodeView)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.fileCard = SimpleCardWidget(CodeView)
        self.fileCard.setObjectName(u"fileCard")
        self.fileCard.setFrameShape(QFrame.StyledPanel)
        self.fileCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout_cardWidget_file = QVBoxLayout(self.fileCard)
        self.verticalLayout_cardWidget_file.setObjectName(u"verticalLayout_cardWidget_file")
        self.fileTree = TreeWidget(self.fileCard)
        self.fileTree.setObjectName(u"fileTree")

        self.verticalLayout_cardWidget_file.addWidget(self.fileTree)


        self.horizontalLayout.addWidget(self.fileCard)

        self.frame_2 = SimpleCardWidget(CodeView)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.codeStackedWidget = QStackedWidget(self.frame_2)
        self.codeStackedWidget.setObjectName(u"codeStackedWidget")
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.verticalLayout_3 = QVBoxLayout(self.page)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.plainTextEdit = PlainTextEditCode(self.page)
        self.plainTextEdit.setObjectName(u"plainTextEdit")
        font = QFont()
        font.setFamilies([u"JetBrains Mono"])
        font.setPointSize(10)
        self.plainTextEdit.setFont(font)
        self.plainTextEdit.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.plainTextEdit.setReadOnly(True)

        self.verticalLayout_3.addWidget(self.plainTextEdit)

        self.codeStackedWidget.addWidget(self.page)

        self.verticalLayout.addWidget(self.codeStackedWidget)


        self.horizontalLayout.addWidget(self.frame_2)


        self.retranslateUi(CodeView)

        QMetaObject.connectSlotsByName(CodeView)
    # setupUi

    def retranslateUi(self, CodeView):
        CodeView.setWindowTitle(QCoreApplication.translate("CodeView", u"CodeView", None))
    # retranslateUi

