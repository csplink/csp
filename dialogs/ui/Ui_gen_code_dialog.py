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
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

from qfluentwidgets import (BodyLabel, CheckBox, ComboBox, LineEdit,
    SimpleCardWidget, SubtitleLabel, TitleLabel, ToolButton)

class Ui_GenCodeDialog(object):
    def setupUi(self, GenCodeDialog):
        if not GenCodeDialog.objectName():
            GenCodeDialog.setObjectName(u"GenCodeDialog")
        GenCodeDialog.resize(900, 600)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(GenCodeDialog.sizePolicy().hasHeightForWidth())
        GenCodeDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(GenCodeDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_title = TitleLabel(GenCodeDialog)
        self.label_title.setObjectName(u"label_title")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_title.sizePolicy().hasHeightForWidth())
        self.label_title.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.label_title)

        self.label_titleBuilderSettings = SubtitleLabel(GenCodeDialog)
        self.label_titleBuilderSettings.setObjectName(u"label_titleBuilderSettings")

        self.verticalLayout.addWidget(self.label_titleBuilderSettings)

        self.frame_2 = SimpleCardWidget(GenCodeDialog)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.frame_2)
        self.verticalLayout_3.setSpacing(9)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.checkBox_useToolchainsPackage = CheckBox(self.frame_2)
        self.checkBox_useToolchainsPackage.setObjectName(u"checkBox_useToolchainsPackage")

        self.verticalLayout_3.addWidget(self.checkBox_useToolchainsPackage)

        self.widget_toolchainsPackage = QWidget(self.frame_2)
        self.widget_toolchainsPackage.setObjectName(u"widget_toolchainsPackage")
        self.verticalLayout_4 = QVBoxLayout(self.widget_toolchainsPackage)
        self.verticalLayout_4.setSpacing(9)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setHorizontalSpacing(20)
        self.gridLayout_3.setVerticalSpacing(9)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(9)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_builder = BodyLabel(self.widget_toolchainsPackage)
        self.label_builder.setObjectName(u"label_builder")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_builder.sizePolicy().hasHeightForWidth())
        self.label_builder.setSizePolicy(sizePolicy2)

        self.horizontalLayout_3.addWidget(self.label_builder)

        self.comboBox_builder = ComboBox(self.widget_toolchainsPackage)
        self.comboBox_builder.setObjectName(u"comboBox_builder")

        self.horizontalLayout_3.addWidget(self.comboBox_builder)


        self.gridLayout_3.addLayout(self.horizontalLayout_3, 0, 0, 1, 1)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setSpacing(9)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label_builderVersion = BodyLabel(self.widget_toolchainsPackage)
        self.label_builderVersion.setObjectName(u"label_builderVersion")
        sizePolicy2.setHeightForWidth(self.label_builderVersion.sizePolicy().hasHeightForWidth())
        self.label_builderVersion.setSizePolicy(sizePolicy2)

        self.horizontalLayout_6.addWidget(self.label_builderVersion)

        self.comboBox_builderVersion = ComboBox(self.widget_toolchainsPackage)
        self.comboBox_builderVersion.setObjectName(u"comboBox_builderVersion")

        self.horizontalLayout_6.addWidget(self.comboBox_builderVersion)


        self.gridLayout_3.addLayout(self.horizontalLayout_6, 0, 1, 1, 1)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setSpacing(9)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.label_toolchains = BodyLabel(self.widget_toolchainsPackage)
        self.label_toolchains.setObjectName(u"label_toolchains")
        sizePolicy2.setHeightForWidth(self.label_toolchains.sizePolicy().hasHeightForWidth())
        self.label_toolchains.setSizePolicy(sizePolicy2)

        self.horizontalLayout_5.addWidget(self.label_toolchains)

        self.comboBox_toolchains = ComboBox(self.widget_toolchainsPackage)
        self.comboBox_toolchains.setObjectName(u"comboBox_toolchains")

        self.horizontalLayout_5.addWidget(self.comboBox_toolchains)


        self.gridLayout_3.addLayout(self.horizontalLayout_5, 1, 0, 1, 1)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setSpacing(9)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_toolchainsVersion = BodyLabel(self.widget_toolchainsPackage)
        self.label_toolchainsVersion.setObjectName(u"label_toolchainsVersion")
        sizePolicy2.setHeightForWidth(self.label_toolchainsVersion.sizePolicy().hasHeightForWidth())
        self.label_toolchainsVersion.setSizePolicy(sizePolicy2)

        self.horizontalLayout_7.addWidget(self.label_toolchainsVersion)

        self.comboBox_toolchainsVersion = ComboBox(self.widget_toolchainsPackage)
        self.comboBox_toolchainsVersion.setObjectName(u"comboBox_toolchainsVersion")

        self.horizontalLayout_7.addWidget(self.comboBox_toolchainsVersion)


        self.gridLayout_3.addLayout(self.horizontalLayout_7, 1, 1, 1, 1)


        self.verticalLayout_4.addLayout(self.gridLayout_3)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setSpacing(9)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.label_toolchainsPath = BodyLabel(self.widget_toolchainsPackage)
        self.label_toolchainsPath.setObjectName(u"label_toolchainsPath")
        sizePolicy2.setHeightForWidth(self.label_toolchainsPath.sizePolicy().hasHeightForWidth())
        self.label_toolchainsPath.setSizePolicy(sizePolicy2)

        self.horizontalLayout_8.addWidget(self.label_toolchainsPath)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lineEdit_toolchainsPath = LineEdit(self.widget_toolchainsPackage)
        self.lineEdit_toolchainsPath.setObjectName(u"lineEdit_toolchainsPath")
        self.lineEdit_toolchainsPath.setReadOnly(True)

        self.horizontalLayout_4.addWidget(self.lineEdit_toolchainsPath)

        self.toolButton_toolchainsManager = ToolButton(self.widget_toolchainsPackage)
        self.toolButton_toolchainsManager.setObjectName(u"toolButton_toolchainsManager")

        self.horizontalLayout_4.addWidget(self.toolButton_toolchainsManager)


        self.horizontalLayout_8.addLayout(self.horizontalLayout_4)


        self.verticalLayout_4.addLayout(self.horizontalLayout_8)


        self.verticalLayout_3.addWidget(self.widget_toolchainsPackage)


        self.verticalLayout.addWidget(self.frame_2)

        self.label_titleLinkerSettings = SubtitleLabel(GenCodeDialog)
        self.label_titleLinkerSettings.setObjectName(u"label_titleLinkerSettings")
        sizePolicy1.setHeightForWidth(self.label_titleLinkerSettings.sizePolicy().hasHeightForWidth())
        self.label_titleLinkerSettings.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.label_titleLinkerSettings)

        self.frame = SimpleCardWidget(GenCodeDialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.frame)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(20)
        self.gridLayout.setVerticalSpacing(9)
        self.lineEdit_minHeapSize = LineEdit(self.frame)
        self.lineEdit_minHeapSize.setObjectName(u"lineEdit_minHeapSize")

        self.gridLayout.addWidget(self.lineEdit_minHeapSize, 0, 1, 1, 1)

        self.label_minStackSize = BodyLabel(self.frame)
        self.label_minStackSize.setObjectName(u"label_minStackSize")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.label_minStackSize.sizePolicy().hasHeightForWidth())
        self.label_minStackSize.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_minStackSize, 1, 0, 1, 1)

        self.label_minHeapSize = BodyLabel(self.frame)
        self.label_minHeapSize.setObjectName(u"label_minHeapSize")
        sizePolicy3.setHeightForWidth(self.label_minHeapSize.sizePolicy().hasHeightForWidth())
        self.label_minHeapSize.setSizePolicy(sizePolicy3)

        self.gridLayout.addWidget(self.label_minHeapSize, 0, 0, 1, 1)

        self.lineEdit_minStackSize = LineEdit(self.frame)
        self.lineEdit_minStackSize.setObjectName(u"lineEdit_minStackSize")

        self.gridLayout.addWidget(self.lineEdit_minStackSize, 1, 1, 1, 1)


        self.verticalLayout.addWidget(self.frame)

        self.label_titlePackageSettings = SubtitleLabel(GenCodeDialog)
        self.label_titlePackageSettings.setObjectName(u"label_titlePackageSettings")

        self.verticalLayout.addWidget(self.label_titlePackageSettings)

        self.frame_3 = SimpleCardWidget(GenCodeDialog)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_3)
        self.verticalLayout_2.setSpacing(9)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.checkBox_isCopyLibrary = CheckBox(self.frame_3)
        self.checkBox_isCopyLibrary.setObjectName(u"checkBox_isCopyLibrary")

        self.horizontalLayout.addWidget(self.checkBox_isCopyLibrary)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setHorizontalSpacing(20)
        self.gridLayout_2.setVerticalSpacing(9)
        self.label_halVersion = BodyLabel(self.frame_3)
        self.label_halVersion.setObjectName(u"label_halVersion")
        sizePolicy2.setHeightForWidth(self.label_halVersion.sizePolicy().hasHeightForWidth())
        self.label_halVersion.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.label_halVersion, 0, 0, 1, 1)

        self.comboBox_halVersion = ComboBox(self.frame_3)
        self.comboBox_halVersion.setObjectName(u"comboBox_halVersion")

        self.gridLayout_2.addWidget(self.comboBox_halVersion, 0, 1, 1, 1)

        self.label_packagePath = BodyLabel(self.frame_3)
        self.label_packagePath.setObjectName(u"label_packagePath")
        sizePolicy2.setHeightForWidth(self.label_packagePath.sizePolicy().hasHeightForWidth())
        self.label_packagePath.setSizePolicy(sizePolicy2)

        self.gridLayout_2.addWidget(self.label_packagePath, 1, 0, 1, 1)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lineEdit_halPath = LineEdit(self.frame_3)
        self.lineEdit_halPath.setObjectName(u"lineEdit_halPath")
        self.lineEdit_halPath.setReadOnly(True)

        self.horizontalLayout_2.addWidget(self.lineEdit_halPath)

        self.toolButton_packageManager = ToolButton(self.frame_3)
        self.toolButton_packageManager.setObjectName(u"toolButton_packageManager")

        self.horizontalLayout_2.addWidget(self.toolButton_packageManager)


        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 1, 1, 1)


        self.verticalLayout_2.addLayout(self.gridLayout_2)


        self.verticalLayout.addWidget(self.frame_3)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(GenCodeDialog)

        QMetaObject.connectSlotsByName(GenCodeDialog)
    # setupUi

    def retranslateUi(self, GenCodeDialog):
        GenCodeDialog.setWindowTitle(QCoreApplication.translate("GenCodeDialog", u"GenCodeDialog", None))
        self.label_title.setText(QCoreApplication.translate("GenCodeDialog", u"Generate Settings", None))
        self.label_titleBuilderSettings.setText(QCoreApplication.translate("GenCodeDialog", u"Builder Settings", None))
        self.checkBox_useToolchainsPackage.setText(QCoreApplication.translate("GenCodeDialog", u"Use toolchains package", None))
        self.label_builder.setText(QCoreApplication.translate("GenCodeDialog", u"Builder", None))
        self.label_builderVersion.setText(QCoreApplication.translate("GenCodeDialog", u"Builder Version", None))
        self.label_toolchains.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains", None))
        self.label_toolchainsVersion.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains Version", None))
        self.label_toolchainsPath.setText(QCoreApplication.translate("GenCodeDialog", u"Toolchains Path", None))
#if QT_CONFIG(tooltip)
        self.toolButton_toolchainsManager.setToolTip(QCoreApplication.translate("GenCodeDialog", u"Package Manager", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_toolchainsManager.setText("")
        self.label_titleLinkerSettings.setText(QCoreApplication.translate("GenCodeDialog", u"Linker Settings", None))
        self.label_minStackSize.setText(QCoreApplication.translate("GenCodeDialog", u"Minimum Stack Size (Hex)", None))
        self.label_minHeapSize.setText(QCoreApplication.translate("GenCodeDialog", u"Minimum Heap Size (Hex)", None))
        self.label_titlePackageSettings.setText(QCoreApplication.translate("GenCodeDialog", u"Package Settings", None))
        self.checkBox_isCopyLibrary.setText(QCoreApplication.translate("GenCodeDialog", u"Copy the library files to the project directory", None))
        self.label_halVersion.setText(QCoreApplication.translate("GenCodeDialog", u"Package Version", None))
        self.label_packagePath.setText(QCoreApplication.translate("GenCodeDialog", u"Package Path", None))
#if QT_CONFIG(tooltip)
        self.toolButton_packageManager.setToolTip(QCoreApplication.translate("GenCodeDialog", u"Package Manager", None))
#endif // QT_CONFIG(tooltip)
        self.toolButton_packageManager.setText("")
    # retranslateUi

