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
        QListWidgetItem(self.settingList)
        QListWidgetItem(self.settingList)
        QListWidgetItem(self.settingList)
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
        self.label_builder = BodyLabel(self.builderPage)
        self.label_builder.setObjectName(u"label_builder")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_builder.sizePolicy().hasHeightForWidth())
        self.label_builder.setSizePolicy(sizePolicy1)

        self.horizontalLayout_3.addWidget(self.label_builder)

        self.combobox_builder = ComboBox(self.builderPage)
        self.combobox_builder.setObjectName(u"combobox_builder")

        self.horizontalLayout_3.addWidget(self.combobox_builder)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_builderVersion = BodyLabel(self.builderPage)
        self.label_builderVersion.setObjectName(u"label_builderVersion")
        sizePolicy1.setHeightForWidth(self.label_builderVersion.sizePolicy().hasHeightForWidth())
        self.label_builderVersion.setSizePolicy(sizePolicy1)

        self.horizontalLayout_6.addWidget(self.label_builderVersion)

        self.combobox_builder_version = ComboBox(self.builderPage)
        self.combobox_builder_version.setObjectName(u"combobox_builder_version")

        self.horizontalLayout_6.addWidget(self.combobox_builder_version)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(9)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_toolchains = BodyLabel(self.builderPage)
        self.label_toolchains.setObjectName(u"label_toolchains")
        sizePolicy1.setHeightForWidth(self.label_toolchains.sizePolicy().hasHeightForWidth())
        self.label_toolchains.setSizePolicy(sizePolicy1)

        self.horizontalLayout_5.addWidget(self.label_toolchains)

        self.combobox_toolchains = ComboBox(self.builderPage)
        self.combobox_toolchains.setObjectName(u"combobox_toolchains")

        self.horizontalLayout_5.addWidget(self.combobox_toolchains)


        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_toolchainsVersion = BodyLabel(self.builderPage)
        self.label_toolchainsVersion.setObjectName(u"label_toolchainsVersion")
        sizePolicy1.setHeightForWidth(self.label_toolchainsVersion.sizePolicy().hasHeightForWidth())
        self.label_toolchainsVersion.setSizePolicy(sizePolicy1)

        self.horizontalLayout_7.addWidget(self.label_toolchainsVersion)

        self.combobox_toolchains_version = ComboBox(self.builderPage)
        self.combobox_toolchains_version.setObjectName(u"combobox_toolchains_version")

        self.horizontalLayout_7.addWidget(self.combobox_toolchains_version)


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

        __sortingEnabled = self.settingList.isSortingEnabled()
        self.settingList.setSortingEnabled(False)
        ___qlistwidgetitem = self.settingList.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("GenCodeDialog", u"Builder Settings", None));
        ___qlistwidgetitem1 = self.settingList.item(1)
        ___qlistwidgetitem1.setText(QCoreApplication.translate("GenCodeDialog", u"Linker Settings", None));
        ___qlistwidgetitem2 = self.settingList.item(2)
        ___qlistwidgetitem2.setText(QCoreApplication.translate("GenCodeDialog", u"Package Settings", None));
        self.settingList.setSortingEnabled(__sortingEnabled)

        self.useToolchainsPackageCheckbox.setText(QCoreApplication.translate("GenCodeDialog", u"Use Toolchains Package", None))
        self.label_builder.setText(QCoreApplication.translate("GenCodeDialog", u"Builder", None))
        self.label_builderVersion.setText(QCoreApplication.translate("GenCodeDialog", u"Builder Version", None))
        self.label_toolchains.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains", None))
        self.label_toolchainsVersion.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains Version", None))
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

