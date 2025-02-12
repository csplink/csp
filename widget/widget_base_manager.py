#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the GNU General Public License v. 3 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.gnu.org/licenses/gpl-3.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2022-2024 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        widget_base_manager.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-12-25     xqyjlj       initial version
#

from enum import Enum

from PySide6.QtCore import (
    Qt,
    QRegularExpression,
    QModelIndex,
    QAbstractTableModel,
    QSortFilterProxyModel,
    QAbstractItemModel,
    QEvent,
    QRectF,
)
from PySide6.QtGui import QRegularExpressionValidator, QFont, QMouseEvent
from PySide6.QtWidgets import (
    QWidget,
    QHeaderView,
    QAbstractItemView,
    QStyleOptionViewItem,
    QApplication,
    QVBoxLayout,
    QTableView,
)
from loguru import logger
from qfluentwidgets import (
    LineEdit,
    TableItemDelegate,
    ComboBox,
    SpinBox,
    DoubleSpinBox,
    TableView,
)

from common import PROJECT, SETTINGS, SIGNAL_BUS, SUMMARY, IP, Style, IpType


class WidgetBaseManagerType(Enum):
    MODE = 0
    CONTROL = 1


class _PModel:

    def __init__(
        self,
        name: str,
        path: str,
        value: str | int | float | bool,
        possibleValues: list[str] = [],
        description: str = "",
        param: str = "",
        parameter: IpType.ParameterUnitType = IpType.ParameterUnitType({}),
    ):
        self.__name = name
        self.__path = path
        self.__value = value
        self.__possibleValues = possibleValues
        self.__description = description
        self.__param = param
        self.__parameter = parameter

        if len(self.__parameter.origin) > 0:
            self.__type = self.__parameter.type
            self.__readonly = self.__parameter.readonly
        else:
            self.__type = "string"
            self.__readonly = True

    # region getter/setter
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        self.__name = value

    @property
    def path(self) -> str:
        return self.__path

    @path.setter
    def path(self, value: str):
        self.__path = value

    @property
    def value(self) -> str | int | float | bool:
        return self.__value

    @value.setter
    def value(self, value: str | int | float | bool):
        self.__value = value

    @property
    def param(self) -> str:
        return self.__param

    @param.setter
    def param(self, value: str):
        self.__param = value

    @property
    def parameter(self) -> IpType.ParameterUnitType:
        return self.__parameter

    @parameter.setter
    def parameter(self, value: IpType.ParameterUnitType):
        self.__parameter = value

    @property
    def type(self) -> str:
        return self.__type

    @type.setter
    def type(self, value: str):
        self.__type = value

    @property
    def possibleValues(self) -> list[str]:
        return self.__possibleValues

    @possibleValues.setter
    def possibleValues(self, value: list[str]):
        self.__possibleValues = value

    @property
    def readonly(self) -> bool:
        return self.__readonly

    @readonly.setter
    def readonly(self, value: bool):
        self.__readonly = value

    @property
    def description(self) -> str:
        return self.__description

    @description.setter
    def description(self, value: str):
        self.__description = value

    # endregion


class WidgetBaseManagerEditorDelegate(TableItemDelegate):

    def __init__(self, dataModels: list[_PModel], parent: QTableView):
        super().__init__(parent)

        self.__dataModels = dataModels

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        column = index.column()
        row = index.row()

        dataModel = self.__dataModels[row]

        # for boolean type, click to toggle value (check box)
        if column == 1 and dataModel.type == "boolean":
            if (
                event.type() == QEvent.Type.MouseButtonRelease
                or event.type() == QEvent.Type.MouseButtonDblClick
            ):
                mouseEvent: QMouseEvent = event  # type: ignore
                if mouseEvent.button() == Qt.MouseButton.LeftButton:
                    x = option.rect.x() + 15  # type: ignore
                    y = option.rect.center().y() - 9.5  # type: ignore
                    rect = QRectF(x, y, 19, 19)
                    if rect.contains(mouseEvent.pos()):
                        return model.setData(
                            index,
                            not dataModel.value,
                            Qt.ItemDataRole.EditRole,
                        )

        return super().editorEvent(event, model, option, index)

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget | None:
        column = index.column()
        row = index.row()
        if column == 0:
            return None

        dataModel = self.__dataModels[row]

        if dataModel.type == "string":
            lineEdit = LineEdit(parent)
            lineEdit.setProperty("transparent", False)
            lineEdit.setStyle(QApplication.style())
            lineEdit.setText(dataModel.value)  # type: ignore
            lineEdit.setValidator(
                QRegularExpressionValidator(
                    QRegularExpression("^[A-Za-z_][A-Za-z0-9_]+$")
                )
            )
            return lineEdit
        elif dataModel.type == "enum":
            comboBox = ComboBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(comboBox)
            comboBox.setStyle(QApplication.style())
            for value in dataModel.possibleValues:
                comboBox.addItem(IP.iptr(dataModel.param, value))
            comboBox.setCurrentText(IP.iptr(dataModel.param, dataModel.value))  # type: ignore
            return comboBox
        elif dataModel.type == "integer":
            spinBox = SpinBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(spinBox)
            parameter = dataModel.parameter
            if parameter.max > -1:
                spinBox.setMaximum(int(parameter.max))
                spinBox.setMinimum(int(parameter.min))
            spinBox.setValue(dataModel.value)  # type: ignore
            return spinBox
        elif dataModel.type == "float":
            spinBox = DoubleSpinBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(spinBox)
            parameter = dataModel.parameter
            if parameter.max > -1:
                spinBox.setMaximum(parameter.max)
                spinBox.setMinimum(parameter.min)
            spinBox.setValue(dataModel.value)  # type: ignore
            return spinBox
        else:
            logger.warning(f"unknown type {dataModel.type!r}")

        return None

    def setModelData(
        self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex
    ):
        column = index.column()
        row = index.row()
        if column == 0:
            return

        dataModel = self.__dataModels[row]

        if dataModel.type == "string":
            lineEdit: LineEdit = editor  # type: ignore
            model.setData(index, lineEdit.text(), Qt.ItemDataRole.EditRole)
        elif dataModel.type == "enum":
            comboBox: ComboBox = editor  # type: ignore
            model.setData(index, comboBox.currentText(), Qt.ItemDataRole.EditRole)
        elif dataModel.type == "integer":
            spinBox: SpinBox = editor  # type: ignore
            model.setData(index, spinBox.value(), Qt.ItemDataRole.EditRole)
        elif dataModel.type == "float":
            spinBox: SpinBox = editor  # type: ignore
            model.setData(index, spinBox.value(), Qt.ItemDataRole.EditRole)
        else:
            logger.warning(f"unknown type {dataModel.type!r}")


class WidgetBaseManagerModel(QAbstractTableModel):
    def __init__(
        self,
        dataModels: list[_PModel],
        type_: WidgetBaseManagerType,
        parent=None,
    ):
        super().__init__(parent)

        self.__dataModels = dataModels
        self.__type = type_
        self.__pinInstance = SUMMARY.projectSummary().pinInstance()
        self.__ip = None
        self.__configs: dict[str, IpType.ControlModeUnitType] = {}

        self.__preBuildParameters = {
            "name": IpType.ParameterUnitType(
                {
                    "type": "string",
                    "readonly": True,
                }
            ),
            "label": IpType.ParameterUnitType(
                {
                    "type": "string",
                    "readonly": False,
                }
            ),
        }

        self.__font = QFont("JetBrains Mono")
        self.__font.setPixelSize(12)

    # region overrides
    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.__dataModels)

    def columnCount(self, parent: QModelIndex) -> int:
        return 2

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        column = index.column()
        row = index.row()

        dataModel = self.__dataModels[row]

        if (
            role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole
        ):  # 0, 2
            if column == 0:
                return dataModel.name
            elif column == 1:
                if dataModel.type == "boolean":
                    return None
                return IP.iptr(dataModel.param, dataModel.value)  # type: ignore
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            if column == 1:
                return dataModel.description
            else:
                return ""
        elif role == Qt.ItemDataRole.StatusTipRole:  # 4
            return None
        elif role == Qt.ItemDataRole.FontRole:  # 6
            return self.__font
        elif role == Qt.ItemDataRole.TextAlignmentRole:  # 7
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        elif role == Qt.ItemDataRole.BackgroundRole:  # 8
            return None
        elif role == Qt.ItemDataRole.ForegroundRole:  # 9
            return None
        elif role == Qt.ItemDataRole.CheckStateRole:  # 10
            if column == 1:
                if dataModel.type == "boolean":
                    return (
                        Qt.CheckState.Checked
                        if dataModel.value
                        else Qt.CheckState.Unchecked
                    )
        elif role == Qt.ItemDataRole.SizeHintRole:  # 13
            return None
        else:
            return None

    def setData(self, index: QModelIndex, value: object, role: int) -> bool:
        column = index.column()
        row = index.row()

        dataModel = self.__dataModels[row]

        if role == Qt.ItemDataRole.EditRole and column == 1:
            if dataModel.type == "string":
                PROJECT.project().configs.set(dataModel.path, value)
                dataModel.value = value  # type: ignore
            elif dataModel.type == "enum":
                val = IP.iptr2(dataModel.param, value)  # type: ignore
                PROJECT.project().configs.set(dataModel.path, val)
                dataModel.value = value  # type: ignore
            elif dataModel.type == "integer":
                PROJECT.project().configs.set(dataModel.path, value)
                dataModel.value = value  # type: ignore
            elif dataModel.type == "float":
                PROJECT.project().configs.set(dataModel.path, value)
                dataModel.value = value  # type: ignore
            elif dataModel.type == "boolean":
                PROJECT.project().configs.set(dataModel.path, value)
                dataModel.value = value  # type: ignore
            else:
                logger.warning(f"unknown type {dataModel.type} with value {value}")
                return False
            return True
        else:
            return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        flag = super().flags(index)
        if index.column() == 0:
            if self.__dataModels[index.row()].type == "boolean":
                flag &= Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsUserTristate
        elif index.column() == 1:
            if self.__dataModels[index.row()].readonly:
                flag &= ~Qt.ItemFlag.ItemIsEnabled
            else:
                flag |= Qt.ItemFlag.ItemIsEditable
        return flag

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ) -> object:
        return None

    # endregion

    def setTarget(self, instance: str, target: str):
        self.__dataModels.clear()

        if self.__ip:
            self.__ip.parameterItemUpdated.disconnect(self.__on_ip_parameterItemUpdated)

        ip = IP.projectIps().get(instance)
        if ip is None:
            logger.error(f"the ip instance:{instance!r} is invalid.")
            self.modelReset.emit()
            return

        self.__ip = ip

        if self.__type == WidgetBaseManagerType.MODE:
            if self.__pinInstance == instance:
                function: str = PROJECT.project().configs.get(f"pin/{target}/function", "")  # type: ignore
                seqs = function.split(":")

                if len(seqs) == 2 and seqs[0] == self.__pinInstance:
                    key = seqs[1]
                else:
                    mode: str = PROJECT.project().configs.get(f"pin/{target}/mode", "")  # type: ignore
                    seqs = mode.split(":")
                    if len(seqs) != 2:
                        self.modelReset.emit()
                        self.__ip.parameterItemUpdated.connect(
                            self.__on_ip_parameterItemUpdated
                        )
                        return
                    key = seqs[1]

                configs = ip.pinModes.get(key, {})
            else:
                configs = ip.modes

            if self.__pinInstance == instance:
                self.__dataModels.extend(
                    [
                        _PModel(
                            name=self.tr("Name"),  # type: ignore
                            path="",
                            value=target,
                            parameter=self.__preBuildParameters["name"],
                        ),
                        _PModel(
                            name=self.tr("Label"),  # type: ignore
                            path=f"pin/{target}/label",
                            value=PROJECT.project().configs.get(f"pin/{target}/label", ""),  # type: ignore
                            parameter=self.__preBuildParameters["label"],
                        ),
                    ]
                )
        else:
            configs = ip.controls

        self.__configs = configs

        if ip.parameters:
            for param, cfg in configs.items():
                if ip.parameters[param].visible:
                    path = (
                        f"{instance}/{target}/{param}"
                        if target
                        else f"{instance}/{param}"
                    )
                    self.__dataModels.append(self.__createPModel(path, param))

        self.modelReset.emit()
        self.__ip.parameterItemUpdated.connect(self.__on_ip_parameterItemUpdated)

    def __getParams(self) -> dict[str, int]:
        params = {}
        for i in range(len(self.__dataModels)):
            params[self.__dataModels[i].param] = i
        return params

    def __on_ip_parameterItemUpdated(self, names: list[str]):
        if self.__ip is None:
            return

        for param, index in self.__getParams().items():
            if param in names:
                originModel = self.__dataModels[index]
                model = self.__createPModel(originModel.path, param)
                originModel.name = model.name
                originModel.value = model.value
                originModel.type = model.type
                originModel.possibleValues = model.possibleValues
                originModel.readonly = model.readonly
                originModel.description = model.description
                originModel.param = param
                originModel.parameter = model.parameter

                self.dataChanged.emit(
                    self.createIndex(index, 0), self.createIndex(index, 1)
                )

    def __createPModel(self, path: str, param: str) -> _PModel:
        local = SETTINGS.get(SETTINGS.language).value.name()
        val = PROJECT.project().configs.get(path)
        config = self.__configs[param]
        parameter = self.__ip.parameters[param]  # type: ignore
        if val is None:
            val = config.default
            PROJECT.project().configs.set(path, val)
        else:
            if parameter.type == "enum":
                if val not in parameter.values:
                    # logger.warning(
                    #     f'The enum item {val!r} is not supported. Use default value {parameter.default!r}')
                    val = parameter.default
                    PROJECT.project().configs.set(path, val)
            elif parameter.type == "integer" or parameter.type == "float":
                if not isinstance(val, int) and not isinstance(val, float):
                    logger.warning(
                        f"The value type {val!r}({type(val).__name__!r}) is invalid. Use default value {parameter.default!r}. ({parameter.type!r} is required)"
                    )
                    val = parameter.default
                elif parameter.max > -1:
                    if val > parameter.max or val < parameter.min:
                        # logger.warning(
                        #     f'The {parameter.type!r} item {val} is not supported. Use default value {parameter.default!r}')
                        val = parameter.default
            elif parameter.type == "boolean":
                if not isinstance(val, bool):
                    logger.warning(
                        f"The value type {val!r}({type(val).__name__!r}) is invalid. Use default value {parameter.default!r}. ({parameter.type!r} is required)"
                    )
                    val = parameter.default
            else:
                logger.warning(f"unknown type {parameter.type!r}")

        return _PModel(
            name=parameter.display.get(local),
            path=path,
            value=val,  # type: ignore
            possibleValues=config.values,
            description=parameter.description.get(local),
            param=param,
            parameter=parameter,
        )


class WidgetBaseManager(QWidget):

    def __init__(self, type_: WidgetBaseManagerType, parent=None):
        super().__init__(parent)

        # ----------------------------------------------------------------------
        self.vLayout = QVBoxLayout(self)
        self.vLayout.setContentsMargins(9, 9, 9, 9)
        self.tableView_property = TableView(self)
        self.tableView_property.horizontalHeader().hide()
        self.vLayout.addWidget(self.tableView_property)
        # ----------------------------------------------------------------------

        self.__type = type_
        self.__dataModels: list[_PModel] = []
        self.__instance = ""
        self.__target = ""

        proxyModel = QSortFilterProxyModel(self)
        self.m_model = WidgetBaseManagerModel(self.__dataModels, self.__type, self)
        proxyModel.setSourceModel(self.m_model)
        self.tableView_property.setModel(proxyModel)
        self.tableView_property.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.tableView_property.verticalHeader().setVisible(False)
        self.tableView_property.setBorderVisible(True)
        self.tableView_property.setBorderRadius(8)
        self.tableView_property.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.tableView_property.setItemDelegateForColumn(
            1,
            WidgetBaseManagerEditorDelegate(self.__dataModels, self.tableView_property),
        )

    # region getter/setter

    @property
    def instance(self) -> str:
        return self.__instance

    @property
    def target(self) -> str:
        return self.__target

    # endregion

    def setTarget(self, instance: str, target: str):
        self.__instance = instance
        self.__target = target
        self.m_model.setTarget(instance, target)
