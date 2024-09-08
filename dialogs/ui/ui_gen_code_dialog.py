# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gen_code_dialog.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLayout, QListWidgetItem, QSizePolicy, QSpacerItem,
    QSplitter, QStackedWidget, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, LineEdit,
    ListWidget, SimpleCardWidget, ToolButton)

class Ui_GenCodeDialog(object):
    def setupUi(self, GenCodeDialog):
        if not GenCodeDialog.objectName():
            GenCodeDialog.setObjectName(u"GenCodeDialog")
        GenCodeDialog.resize(670, 367)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GenCodeDialog.sizePolicy().hasHeightForWidth())
        GenCodeDialog.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(GenCodeDialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(GenCodeDialog)
        self.splitter.setObjectName(u"splitter")
        self.splitter.setOrientation(Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        self.settingListCard = SimpleCardWidget(self.splitter)
        self.settingListCard.setObjectName(u"settingListCard")
        sizePolicy.setHeightForWidth(self.settingListCard.sizePolicy().hasHeightForWidth())
        self.settingListCard.setSizePolicy(sizePolicy)
        self.settingListCard.setFrameShape(QFrame.StyledPanel)
        self.settingListCard.setFrameShadow(QFrame.Raised)
        self.verticalLayout_cardWidget_file = QVBoxLayout(self.settingListCard)
        self.verticalLayout_cardWidget_file.setObjectName(u"verticalLayout_cardWidget_file")
        self.settingList = ListWidget(self.settingListCard)
        self.settingList.setObjectName(u"settingList")
        sizePolicy.setHeightForWidth(self.settingList.sizePolicy().hasHeightForWidth())
        self.settingList.setSizePolicy(sizePolicy)

        self.verticalLayout_cardWidget_file.addWidget(self.settingList)

        self.splitter.addWidget(self.settingListCard)
        self.frame_1 = SimpleCardWidget(self.splitter)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.settingStackedWidget = QStackedWidget(self.frame_1)
        self.settingStackedWidget.setObjectName(u"settingStackedWidget")
        self.builderPage = QWidget()
        self.builderPage.setObjectName(u"builderPage")
        self.verticalLayout_2 = QVBoxLayout(self.builderPage)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(10)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.toolchainsCombobox = ComboBox(self.builderPage)
        self.toolchainsCombobox.setObjectName(u"toolchainsCombobox")

        self.gridLayout.addWidget(self.toolchainsCombobox, 3, 1, 1, 1)

        self.toolchainsLabel = BodyLabel(self.builderPage)
        self.toolchainsLabel.setObjectName(u"toolchainsLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.toolchainsLabel.sizePolicy().hasHeightForWidth())
        self.toolchainsLabel.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.toolchainsLabel, 3, 0, 1, 1)

        self.toolchainsVersionComboBox = ComboBox(self.builderPage)
        self.toolchainsVersionComboBox.setObjectName(u"toolchainsVersionComboBox")

        self.gridLayout.addWidget(self.toolchainsVersionComboBox, 4, 1, 1, 1)

        self.builderLabel = BodyLabel(self.builderPage)
        self.builderLabel.setObjectName(u"builderLabel")
        sizePolicy1.setHeightForWidth(self.builderLabel.sizePolicy().hasHeightForWidth())
        self.builderLabel.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.builderLabel, 1, 0, 1, 1)

        self.toolchainsVersionLabel = BodyLabel(self.builderPage)
        self.toolchainsVersionLabel.setObjectName(u"toolchainsVersionLabel")
        sizePolicy1.setHeightForWidth(self.toolchainsVersionLabel.sizePolicy().hasHeightForWidth())
        self.toolchainsVersionLabel.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.toolchainsVersionLabel, 4, 0, 1, 1)

        self.builderComboBox = ComboBox(self.builderPage)
        self.builderComboBox.setObjectName(u"builderComboBox")

        self.gridLayout.addWidget(self.builderComboBox, 1, 1, 1, 1)

        self.toolchainsManagerBtn = ToolButton(self.builderPage)
        self.toolchainsManagerBtn.setObjectName(u"toolchainsManagerBtn")

        self.gridLayout.addWidget(self.toolchainsManagerBtn, 5, 2, 1, 1)

        self.builderVersionLabel = BodyLabel(self.builderPage)
        self.builderVersionLabel.setObjectName(u"builderVersionLabel")
        sizePolicy1.setHeightForWidth(self.builderVersionLabel.sizePolicy().hasHeightForWidth())
        self.builderVersionLabel.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.builderVersionLabel, 2, 0, 1, 1)

        self.builderVersionComboBox = ComboBox(self.builderPage)
        self.builderVersionComboBox.setObjectName(u"builderVersionComboBox")

        self.gridLayout.addWidget(self.builderVersionComboBox, 2, 1, 1, 1)

        self.toolchainsPathLabel = BodyLabel(self.builderPage)
        self.toolchainsPathLabel.setObjectName(u"toolchainsPathLabel")
        sizePolicy1.setHeightForWidth(self.toolchainsPathLabel.sizePolicy().hasHeightForWidth())
        self.toolchainsPathLabel.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.toolchainsPathLabel, 5, 0, 1, 1)

        self.toolchainsPathLineEdit = LineEdit(self.builderPage)
        self.toolchainsPathLineEdit.setObjectName(u"toolchainsPathLineEdit")
        self.toolchainsPathLineEdit.setReadOnly(True)

        self.gridLayout.addWidget(self.toolchainsPathLineEdit, 5, 1, 1, 1)

        self.useToolchainsPackageCheckbox = CheckBox(self.builderPage)
        self.useToolchainsPackageCheckbox.setObjectName(u"useToolchainsPackageCheckbox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.useToolchainsPackageCheckbox.sizePolicy().hasHeightForWidth())
        self.useToolchainsPackageCheckbox.setSizePolicy(sizePolicy2)

        self.gridLayout.addWidget(self.useToolchainsPackageCheckbox, 0, 1, 1, 1)

        self.builderLabel_2 = BodyLabel(self.builderPage)
        self.builderLabel_2.setObjectName(u"builderLabel_2")
        sizePolicy1.setHeightForWidth(self.builderLabel_2.sizePolicy().hasHeightForWidth())
        self.builderLabel_2.setSizePolicy(sizePolicy1)
        self.builderLabel_2.setMinimumSize(QSize(0, 21))

        self.gridLayout.addWidget(self.builderLabel_2, 0, 0, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(20, 167, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.settingStackedWidget.addWidget(self.builderPage)
        self.linkerPage = QWidget()
        self.linkerPage.setObjectName(u"linkerPage")
        self.verticalLayout_3 = QVBoxLayout(self.linkerPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setSpacing(10)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.minHeapSizeLabel = BodyLabel(self.linkerPage)
        self.minHeapSizeLabel.setObjectName(u"minHeapSizeLabel")
        sizePolicy.setHeightForWidth(self.minHeapSizeLabel.sizePolicy().hasHeightForWidth())
        self.minHeapSizeLabel.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.minHeapSizeLabel, 0, 0, 1, 1)

        self.minStackLineEdit = LineEdit(self.linkerPage)
        self.minStackLineEdit.setObjectName(u"minStackLineEdit")

        self.gridLayout_3.addWidget(self.minStackLineEdit, 1, 1, 1, 1)

        self.minHeapLineEdit = LineEdit(self.linkerPage)
        self.minHeapLineEdit.setObjectName(u"minHeapLineEdit")

        self.gridLayout_3.addWidget(self.minHeapLineEdit, 0, 1, 1, 1)

        self.minStackSizeLabel = BodyLabel(self.linkerPage)
        self.minStackSizeLabel.setObjectName(u"minStackSizeLabel")
        sizePolicy.setHeightForWidth(self.minStackSizeLabel.sizePolicy().hasHeightForWidth())
        self.minStackSizeLabel.setSizePolicy(sizePolicy)

        self.gridLayout_3.addWidget(self.minStackSizeLabel, 1, 0, 1, 1)

        self.toolchainsManagerBtn_2 = ToolButton(self.linkerPage)
        self.toolchainsManagerBtn_2.setObjectName(u"toolchainsManagerBtn_2")

        self.gridLayout_3.addWidget(self.toolchainsManagerBtn_2, 1, 2, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer_2)

        self.settingStackedWidget.addWidget(self.linkerPage)
        self.packagePage = QWidget()
        self.packagePage.setObjectName(u"packagePage")
        self.verticalLayout_4 = QVBoxLayout(self.packagePage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setSpacing(10)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.halPathLabel = BodyLabel(self.packagePage)
        self.halPathLabel.setObjectName(u"halPathLabel")
        sizePolicy1.setHeightForWidth(self.halPathLabel.sizePolicy().hasHeightForWidth())
        self.halPathLabel.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.halPathLabel, 2, 0, 1, 1)

        self.halVersionComboBox = ComboBox(self.packagePage)
        self.halVersionComboBox.setObjectName(u"halVersionComboBox")

        self.gridLayout_2.addWidget(self.halVersionComboBox, 1, 1, 1, 1)

        self.halVersionLabel = BodyLabel(self.packagePage)
        self.halVersionLabel.setObjectName(u"halVersionLabel")
        sizePolicy1.setHeightForWidth(self.halVersionLabel.sizePolicy().hasHeightForWidth())
        self.halVersionLabel.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.halVersionLabel, 1, 0, 1, 1)

        self.packageManagerBtn = ToolButton(self.packagePage)
        self.packageManagerBtn.setObjectName(u"packageManagerBtn")

        self.gridLayout_2.addWidget(self.packageManagerBtn, 2, 2, 1, 1)

        self.halPathLineEdit = LineEdit(self.packagePage)
        self.halPathLineEdit.setObjectName(u"halPathLineEdit")
        self.halPathLineEdit.setReadOnly(True)

        self.gridLayout_2.addWidget(self.halPathLineEdit, 2, 1, 1, 1)

        self.halVersionLabel_2 = BodyLabel(self.packagePage)
        self.halVersionLabel_2.setObjectName(u"halVersionLabel_2")
        sizePolicy1.setHeightForWidth(self.halVersionLabel_2.sizePolicy().hasHeightForWidth())
        self.halVersionLabel_2.setSizePolicy(sizePolicy1)
        self.halVersionLabel_2.setMinimumSize(QSize(0, 0))

        self.gridLayout_2.addWidget(self.halVersionLabel_2, 0, 0, 1, 1)

        self.copyLibraryCheckbox = CheckBox(self.packagePage)
        self.copyLibraryCheckbox.setObjectName(u"copyLibraryCheckbox")
        sizePolicy2.setHeightForWidth(self.copyLibraryCheckbox.sizePolicy().hasHeightForWidth())
        self.copyLibraryCheckbox.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.copyLibraryCheckbox, 0, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.verticalSpacer_3 = QSpacerItem(20, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.settingStackedWidget.addWidget(self.packagePage)

        self.verticalLayout.addWidget(self.settingStackedWidget)

        self.splitter.addWidget(self.frame_1)

        self.horizontalLayout.addWidget(self.splitter)


        self.retranslateUi(GenCodeDialog)

        self.settingStackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(GenCodeDialog)
    # setupUi

    def retranslateUi(self, GenCodeDialog):
        GenCodeDialog.setWindowTitle(QCoreApplication.translate("GenCodeDialog", u"GenCodeDialog", None))
        self.toolchainsLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains", None))
        self.builderLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Builder", None))
        self.toolchainsVersionLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains Version", None))
#if QT_CONFIG(tooltip)
        self.toolchainsManagerBtn.setToolTip(QCoreApplication.translate("GenCodeDialog", u"Package Manager", None))
#endif // QT_CONFIG(tooltip)
        self.toolchainsManagerBtn.setText("")
        self.builderVersionLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Builder Version", None))
        self.toolchainsPathLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains Path", None))
        self.useToolchainsPackageCheckbox.setText("")
        self.builderLabel_2.setText(QCoreApplication.translate("GenCodeDialog", u"Use Toolchains Package", None))
        self.minHeapSizeLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Minimum Heap Size (Hex)", None))
        self.minStackSizeLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Minimum Stack Size (Hex)", None))
#if QT_CONFIG(tooltip)
        self.toolchainsManagerBtn_2.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.toolchainsManagerBtn_2.setText("")
        self.halPathLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Package Path", None))
        self.halVersionLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Package Version", None))
#if QT_CONFIG(tooltip)
        self.packageManagerBtn.setToolTip(QCoreApplication.translate("GenCodeDialog", u"Package Manager", None))
#endif // QT_CONFIG(tooltip)
        self.packageManagerBtn.setText("")
        self.halVersionLabel_2.setText(QCoreApplication.translate("GenCodeDialog", u"Copy the library files to the project directory", None))
        self.copyLibraryCheckbox.setText("")
    # retranslateUi

