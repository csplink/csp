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
    QListWidgetItem, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CaptionLabel, CheckBox, ComboBox,
    LineEdit, ListWidget, SimpleCardWidget, ToolButton)

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
        self.settingListCard = SimpleCardWidget(GenCodeDialog)
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


        self.horizontalLayout.addWidget(self.settingListCard)

        self.frame_1 = SimpleCardWidget(GenCodeDialog)
        self.frame_1.setObjectName(u"frame_1")
        self.frame_1.setFrameShape(QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame_1)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(9, 9, 9, 9)
        self.settingStackedWidget = QStackedWidget(self.frame_1)
        self.settingStackedWidget.setObjectName(u"settingStackedWidget")
        self.builderPage = QWidget()
        self.builderPage.setObjectName(u"builderPage")
        self.verticalLayout_3 = QVBoxLayout(self.builderPage)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.useToolchainsPackageCheckbox = CheckBox(self.builderPage)
        self.useToolchainsPackageCheckbox.setObjectName(u"useToolchainsPackageCheckbox")

        self.verticalLayout_3.addWidget(self.useToolchainsPackageCheckbox)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(20)
        self.gridLayout_3.setVerticalSpacing(9)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.builderLabel = BodyLabel(self.builderPage)
        self.builderLabel.setObjectName(u"builderLabel")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.builderLabel.sizePolicy().hasHeightForWidth())
        self.builderLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.builderLabel)

        self.builderComboBox = ComboBox(self.builderPage)
        self.builderComboBox.setObjectName(u"builderComboBox")

        self.horizontalLayout_3.addWidget(self.builderComboBox)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.builderVersionLabel = BodyLabel(self.builderPage)
        self.builderVersionLabel.setObjectName(u"builderVersionLabel")
        sizePolicy1.setHeightForWidth(self.builderVersionLabel.sizePolicy().hasHeightForWidth())
        self.builderVersionLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.builderVersionLabel)

        self.builderVersionComboBox = ComboBox(self.builderPage)
        self.builderVersionComboBox.setObjectName(u"builderVersionComboBox")

        self.horizontalLayout_6.addWidget(self.builderVersionComboBox)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(9)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.toolchainsLabel = BodyLabel(self.builderPage)
        self.toolchainsLabel.setObjectName(u"toolchainsLabel")
        sizePolicy1.setHeightForWidth(self.toolchainsLabel.sizePolicy().hasHeightForWidth())
        self.toolchainsLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.toolchainsLabel)

        self.toolchainsCombobox = ComboBox(self.builderPage)
        self.toolchainsCombobox.setObjectName(u"toolchainsCombobox")

        self.horizontalLayout_5.addWidget(self.toolchainsCombobox)


        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.toolchainsVersionLabel = BodyLabel(self.builderPage)
        self.toolchainsVersionLabel.setObjectName(u"toolchainsVersionLabel")
        sizePolicy1.setHeightForWidth(self.toolchainsVersionLabel.sizePolicy().hasHeightForWidth())
        self.toolchainsVersionLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.toolchainsVersionLabel)

        self.toolchainsVersionComboBox = ComboBox(self.builderPage)
        self.toolchainsVersionComboBox.setObjectName(u"toolchainsVersionComboBox")

        self.horizontalLayout_7.addWidget(self.toolchainsVersionComboBox)


        self.gridLayout_3.addLayout(self.horizontalLayout_7, 1, 1, 1, 1)


        self.verticalLayout_3.addLayout(self.gridLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.toolchainsPathLabel = BodyLabel(self.builderPage)
        self.toolchainsPathLabel.setObjectName(u"toolchainsPathLabel")
        sizePolicy1.setHeightForWidth(self.toolchainsPathLabel.sizePolicy().hasHeightForWidth())
        self.toolchainsPathLabel.setSizePolicy(sizePolicy1)

        self.horizontalLayout_8.addWidget(self.toolchainsPathLabel)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.toolchainsPathLineEdit = LineEdit(self.builderPage)
        self.toolchainsPathLineEdit.setObjectName(u"toolchainsPathLineEdit")
        self.toolchainsPathLineEdit.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.toolchainsPathLineEdit)

        self.toolchainsManagerBtn = ToolButton(self.builderPage)
        self.toolchainsManagerBtn.setObjectName(u"toolchainsManagerBtn")

        self.horizontalLayout_4.addWidget(self.toolchainsManagerBtn)


        self.horizontalLayout_8.addLayout(self.horizontalLayout_4)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.toolchainsFolderInvalidLabel = CaptionLabel(self.builderPage)
        self.toolchainsFolderInvalidLabel.setObjectName(u"toolchainsFolderInvalidLabel")
        self.toolchainsFolderInvalidLabel.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.verticalLayout_3.addWidget(self.toolchainsFolderInvalidLabel)

        self.verticalSpacer = QSpacerItem(20, 167, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.settingStackedWidget.addWidget(self.builderPage)
        self.linkerPage = QWidget()
        self.linkerPage.setObjectName(u"linkerPage")
        self.gridLayout_4 = QGridLayout(self.linkerPage)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.minStackLineEdit = LineEdit(self.linkerPage)
        self.minStackLineEdit.setObjectName(u"minStackLineEdit")

        self.gridLayout_4.addWidget(self.minStackLineEdit, 1, 1, 1, 1)

        self.minHeapSizeLabel = BodyLabel(self.linkerPage)
        self.minHeapSizeLabel.setObjectName(u"minHeapSizeLabel")
        sizePolicy.setHeightForWidth(self.minHeapSizeLabel.sizePolicy().hasHeightForWidth())
        self.minHeapSizeLabel.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.minHeapSizeLabel, 0, 0, 1, 1)

        self.minHeapLineEdit = LineEdit(self.linkerPage)
        self.minHeapLineEdit.setObjectName(u"minHeapLineEdit")

        self.gridLayout_4.addWidget(self.minHeapLineEdit, 0, 1, 1, 1)

        self.minStackSizeLabel = BodyLabel(self.linkerPage)
        self.minStackSizeLabel.setObjectName(u"minStackSizeLabel")
        sizePolicy.setHeightForWidth(self.minStackSizeLabel.sizePolicy().hasHeightForWidth())
        self.minStackSizeLabel.setSizePolicy(sizePolicy)

        self.gridLayout_4.addWidget(self.minStackSizeLabel, 1, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.gridLayout_4.addItem(self.verticalSpacer_2, 2, 0, 1, 1)

        self.settingStackedWidget.addWidget(self.linkerPage)
        self.packagePage = QWidget()
        self.packagePage.setObjectName(u"packagePage")
        self.verticalLayout_4 = QVBoxLayout(self.packagePage)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.copyLibraryCheckbox = CheckBox(self.packagePage)
        self.copyLibraryCheckbox.setObjectName(u"copyLibraryCheckbox")

        self.verticalLayout_4.addWidget(self.copyLibraryCheckbox)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(20)
        self.gridLayout_2.setVerticalSpacing(9)
        self.halVersionLabel = BodyLabel(self.packagePage)
        self.halVersionLabel.setObjectName(u"halVersionLabel")
        sizePolicy1.setHeightForWidth(self.halVersionLabel.sizePolicy().hasHeightForWidth())
        self.halVersionLabel.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.halVersionLabel, 0, 0, 1, 1)

        self.halVersionComboBox = ComboBox(self.packagePage)
        self.halVersionComboBox.setObjectName(u"halVersionComboBox")

        self.gridLayout_2.addWidget(self.halVersionComboBox, 0, 1, 1, 1)

        self.halPathLabel = BodyLabel(self.packagePage)
        self.halPathLabel.setObjectName(u"halPathLabel")
        sizePolicy1.setHeightForWidth(self.halPathLabel.sizePolicy().hasHeightForWidth())
        self.halPathLabel.setSizePolicy(sizePolicy1)

        self.gridLayout_2.addWidget(self.halPathLabel, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.halPathLineEdit = LineEdit(self.packagePage)
        self.halPathLineEdit.setObjectName(u"halPathLineEdit")
        self.halPathLineEdit.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.halPathLineEdit)

        self.packageManagerBtn = ToolButton(self.packagePage)
        self.packageManagerBtn.setObjectName(u"packageManagerBtn")

        self.horizontalLayout_2.addWidget(self.packageManagerBtn)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.halFolderInvalidLabel = CaptionLabel(self.packagePage)
        self.halFolderInvalidLabel.setObjectName(u"halFolderInvalidLabel")
        self.halFolderInvalidLabel.setStyleSheet(u"color: rgb(255, 0, 0);")

        self.verticalLayout_4.addWidget(self.halFolderInvalidLabel)

        self.verticalSpacer_3 = QSpacerItem(20, 200, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_4.addItem(self.verticalSpacer_3)

        self.settingStackedWidget.addWidget(self.packagePage)

        self.verticalLayout.addWidget(self.settingStackedWidget)


        self.horizontalLayout.addWidget(self.frame_1)


        self.retranslateUi(GenCodeDialog)

        QMetaObject.connectSlotsByName(GenCodeDialog)
    # setupUi

    def retranslateUi(self, GenCodeDialog):
        GenCodeDialog.setWindowTitle(QCoreApplication.translate("GenCodeDialog", u"GenCodeDialog", None))
        self.useToolchainsPackageCheckbox.setText(QCoreApplication.translate("GenCodeDialog", u"Use Toolchains Package", None))
        self.builderLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Builder", None))
        self.builderVersionLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Builder Version", None))
        self.toolchainsLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains", None))
        self.toolchainsVersionLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains Version", None))
        self.toolchainsPathLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains Path", None))
#if QT_CONFIG(tooltip)
        self.toolchainsManagerBtn.setToolTip(QCoreApplication.translate("GenCodeDialog", u"Package Manager", None))
#endif // QT_CONFIG(tooltip)
        self.toolchainsManagerBtn.setText("")
        self.toolchainsFolderInvalidLabel.setText(QCoreApplication.translate("GenCodeDialog", u"The Path is not directory", None))
        self.minHeapSizeLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Minimum Heap Size (Hex)", None))
        self.minStackSizeLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Minimum Stack Size (Hex)", None))
        self.copyLibraryCheckbox.setText(QCoreApplication.translate("GenCodeDialog", u"Copy the library files to the project directory", None))
        self.halVersionLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Package Version", None))
        self.halPathLabel.setText(QCoreApplication.translate("GenCodeDialog", u"Package Path", None))
#if QT_CONFIG(tooltip)
        self.packageManagerBtn.setToolTip(QCoreApplication.translate("GenCodeDialog", u"Package Manager", None))
#endif // QT_CONFIG(tooltip)
        self.packageManagerBtn.setText("")
        self.halFolderInvalidLabel.setText(QCoreApplication.translate("GenCodeDialog", u"The Path is not directory", None))
    # retranslateUi

