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

import attr
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


@attr.s
class WidgetBaseManagerPrivateModel:
    property: str = attr.ib(default="", validator=attr.validators.instance_of(str))
    path: str = attr.ib(default="", validator=attr.validators.instance_of(str))
    value: str | int | float | bool = attr.ib(
        default="", validator=attr.validators.instance_of((str, int, float, bool))
    )
    typeof: str = attr.ib(default="", validator=attr.validators.instance_of(str))
    possibleValues: list = attr.ib(
        default=[], validator=attr.validators.instance_of(list)
    )
    readonly: bool = attr.ib(default=False, validator=attr.validators.instance_of(bool))
    description: str = attr.ib(default="", validator=attr.validators.instance_of(str))
    param: str = attr.ib(default="", validator=attr.validators.instance_of(str))
    parameter: IpType.ParameterUnitType = attr.ib(default=IpType.ParameterUnitType({}))
    parameters: dict = attr.ib(default={}, validator=attr.validators.instance_of(dict))


class WidgetBaseManagerEditorDelegate(TableItemDelegate):

    def __init__(self, data: list[WidgetBaseManagerPrivateModel], parent: QTableView):
        super().__init__(parent)

        self.__data = data

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        column = index.column()
        row = index.row()
        if column == 1 and self.__data[row].typeof == "boolean":
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
                            index, not self.__data[row].value, Qt.ItemDataRole.EditRole
                        )

        return super().editorEvent(event, model, option, index)

    def createEditor(
        self, parent: QWidget, option: QStyleOptionViewItem, index: QModelIndex
    ) -> QWidget | None:
        column = index.column()
        row = index.row()
        if column == 0:
            return None

        if self.__data[row].typeof == "string":
            lineEdit = LineEdit(parent)
            lineEdit.setProperty("transparent", False)
            lineEdit.setStyle(QApplication.style())
            lineEdit.setText(self.__data[row].value)  # type: ignore
            lineEdit.setValidator(
                QRegularExpressionValidator(
                    QRegularExpression("^[A-Za-z_][A-Za-z0-9_]+$")
                )
            )
            return lineEdit
        elif self.__data[row].typeof == "enum":
            comboBox = ComboBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(comboBox)
            comboBox.setStyle(QApplication.style())
            for value in self.__data[index.row()].possibleValues:
                comboBox.addItem(
                    IP.iptr(self.__data[index.row()].path.split("/")[-1], value)
                )
            comboBox.setCurrentText(
                IP.iptr(
                    self.__data[index.row()].path.split("/")[-1],
                    self.__data[index.row()].value,  # type: ignore
                )
            )
            return comboBox
        elif self.__data[row].typeof == "integer":
            spinBox = SpinBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(spinBox)
            parameter = self.__data[row].parameter
            if parameter.max > -1:
                spinBox.setMaximum(int(parameter.max))
                spinBox.setMinimum(int(parameter.min))
            spinBox.setValue(self.__data[row].value)  # type: ignore
            return spinBox
        elif self.__data[row].typeof == "float":
            spinBox = DoubleSpinBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(spinBox)
            parameter = self.__data[row].parameter
            if parameter.max > -1:
                spinBox.setMaximum(parameter.max)
                spinBox.setMinimum(parameter.min)
            spinBox.setValue(self.__data[row].value)  # type: ignore
            return spinBox
        else:
            logger.warning(f"unknown typeof {self.__data[row].typeof!r}")

        return None

    def setModelData(
        self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex
    ):
        column = index.column()
        row = index.row()
        if column == 0:
            return None

        if self.__data[row].typeof == "string":
            lineEdit: LineEdit = editor  # type: ignore
            model.setData(index, lineEdit.text(), Qt.ItemDataRole.EditRole)
        elif self.__data[row].typeof == "enum":
            comboBox: ComboBox = editor  # type: ignore
            model.setData(index, comboBox.currentText(), Qt.ItemDataRole.EditRole)
        elif self.__data[row].typeof == "integer":
            spinBox: SpinBox = editor  # type: ignore
            model.setData(index, spinBox.value(), Qt.ItemDataRole.EditRole)
        elif self.__data[row].typeof == "float":
            spinBox: SpinBox = editor  # type: ignore
            model.setData(index, spinBox.value(), Qt.ItemDataRole.EditRole)
        else:
            logger.warning(f"unknown typeof {self.__data[row].typeof!r}")


class WidgetBaseManagerModel(QAbstractTableModel):

    def __init__(
        self,
        data: list[WidgetBaseManagerPrivateModel],
        type_: WidgetBaseManagerType,
        parent=None,
    ):
        super().__init__(parent)

        self.__data = data
        self.__type = type_
        self.__pinInstance = ""
        self.__ip = None
        self.__configs: dict[str, IpType.ControlModeUnitType] = {}
        self.__instance = ""

        self.__font = QFont("JetBrains Mono")
        self.__font.setPixelSize(12)

        self.__pinInstance = SUMMARY.projectSummary().pinInstance()

        SIGNAL_BUS.controlManagerTriggered.connect(self.__on_x_controlManagerTriggered)
        SIGNAL_BUS.modeManagerTriggered.connect(self.__on_x_modeManagerTriggered)

    # noinspection PyMethodOverriding
    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.__data)

    # noinspection PyMethodOverriding
    def columnCount(self, parent: QModelIndex) -> int:
        return 2

    # noinspection PyMethodOverriding
    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> object:
        if (
            role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole
        ):  # 0, 2
            if index.column() == 0:
                return self.__data[index.row()].property
            elif index.column() == 1:
                if self.__data[index.row()].typeof == "boolean":
                    return None
                return IP.iptr(
                    self.__data[index.row()].param, self.__data[index.row()].value  # type: ignore
                )
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            if index.column() == 1:
                return self.__data[index.row()].description
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
            if index.column() == 1:
                if self.__data[index.row()].typeof == "boolean":
                    return (
                        Qt.CheckState.Checked
                        if self.__data[index.row()].value
                        else Qt.CheckState.Unchecked
                    )
        elif role == Qt.ItemDataRole.SizeHintRole:  # 13
            return None
        else:
            return None

    # noinspection PyMethodOverriding
    def setData(self, index: QModelIndex, value: object, role: int) -> bool:
        if role == Qt.ItemDataRole.EditRole:
            if self.__data[index.row()].typeof == "string":
                path = self.__data[index.row()].path
                PROJECT.project().configs.set(path, value)
                self.__data[index.row()].value = value  # type: ignore
            elif self.__data[index.row()].typeof == "enum":
                path = self.__data[index.row()].path
                PROJECT.project().configs.set(
                    path, IP.iptr2(path.split("/")[-1], value)  # type: ignore
                )
                self.__data[index.row()].value = value  # type: ignore
            elif self.__data[index.row()].typeof == "integer":
                path = self.__data[index.row()].path
                PROJECT.project().configs.set(path, value)
                self.__data[index.row()].value = value  # type: ignore
            elif self.__data[index.row()].typeof == "float":
                path = self.__data[index.row()].path
                PROJECT.project().configs.set(path, value)
                self.__data[index.row()].value = value  # type: ignore
            elif self.__data[index.row()].typeof == "boolean":
                path = self.__data[index.row()].path
                PROJECT.project().configs.set(path, value)
                self.__data[index.row()].value = value  # type: ignore
            else:
                logger.warning(
                    f"unknown typeof {self.__data[index.row()].typeof} with value {value}"
                )
                return False
            return True
        else:
            return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        flag = super().flags(index)
        if index.column() == 0:
            if self.__data[index.row()].typeof == "boolean":
                flag &= Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsUserTristate
        elif index.column() == 1:
            if self.__data[index.row()].readonly:
                flag &= ~Qt.ItemFlag.ItemIsEnabled
            else:
                flag |= Qt.ItemFlag.ItemIsEditable
        return flag

    # noinspection PyMethodOverriding
    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ) -> object:
        return None

    def __on_x_controlManagerTriggered(self, instance: str, widget: str):
        self.__instance = instance

    def __on_x_modeManagerTriggered(self, instance: str, value: str):
        if self.__instance != instance:
            return

        self.__data.clear()
        if self.__ip is not None:
            self.__ip.parameterItemUpdated.disconnect(self.__on_ip_parameterItemUpdated)

        ip = IP.projectIps().get(instance)
        if ip is None:
            logger.error(f"the ip instance:{instance!r} is invalid.")
            self.modelReset.emit()
            return

        self.__ip = ip

        if self.__type == WidgetBaseManagerType.MODE:
            if self.__pinInstance == instance:
                function: str = PROJECT.project().configs.get(  # type: ignore
                    f"pin/{value}/function", ""
                )
                if len(function) == 0:
                    self.modelReset.emit()
                    self.__ip.parameterItemUpdated.connect(
                        self.__on_ip_parameterItemUpdated
                    )
                    return

                cfgs = ip.pinModes[function.split(":")[1]]
            else:
                cfgs = ip.modes

            if self.__pinInstance == instance:
                self.__data.append(
                    WidgetBaseManagerPrivateModel(
                        property=self.tr("Name"),  # type: ignore
                        path="",
                        value=value,
                        typeof="string",
                        possibleValues=[],
                        readonly=True,
                        description="",
                    )
                )
                path = f"pin/{value}/label"
                self.__data.append(
                    WidgetBaseManagerPrivateModel(
                        property=self.tr("Label"),  # type: ignore
                        path=path,
                        value=PROJECT.project().configs.get(path, ""),  # type: ignore
                        typeof="string",
                        possibleValues=[],
                        readonly=False,
                        description="",
                    )
                )
        else:
            cfgs = ip.controls

        self.__configs = cfgs

        if len(ip.parameters) > 0:
            for param, cfg in cfgs.items():
                if ip.parameters[param].visible:
                    if len(value) != 0:
                        path = f"{instance}/{value}/{param}"
                    else:
                        path = f"{instance}/{param}"
                    self.__data.append(self.__genPrivateModel(path, param))

        self.modelReset.emit()
        self.__ip.parameterItemUpdated.connect(self.__on_ip_parameterItemUpdated)

    def __getParams(self) -> dict[str, int]:
        params = {}
        for i in range(len(self.__data)):
            params[self.__data[i].param] = i
        return params

    def __on_ip_parameterItemUpdated(self, names: list[str]):
        for param, index in self.__getParams().items():
            if param in names:
                originModel = self.__data[index]
                model = self.__genPrivateModel(originModel.path, param)
                originModel.property = model.property
                originModel.value = model.value
                originModel.typeof = model.typeof
                originModel.possibleValues = model.possibleValues
                originModel.readonly = model.readonly
                originModel.description = model.description
                originModel.param = param
                originModel.parameter = model.parameter

                self.dataChanged.emit(
                    self.createIndex(index, 0), self.createIndex(index, 1)
                )

    def __genPrivateModel(self, path: str, param: str) -> WidgetBaseManagerPrivateModel:
        if self.__ip is None:
            return WidgetBaseManagerPrivateModel()

        local = SETTINGS.get(SETTINGS.language).value.name()
        val = PROJECT.project().configs.get(path)
        config = self.__configs[param]
        parameter = self.__ip.parameters[param]
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
                logger.warning(f"unknown typeof {parameter.type!r}")

        return WidgetBaseManagerPrivateModel(
            property=parameter.display.get(local),
            path=path,
            value=val,  # type: ignore
            typeof=parameter.type,
            possibleValues=config.values,
            readonly=parameter.readonly,
            description=parameter.description.get(local),
            param=param,
            parameter=parameter,
            parameters=self.__ip.parameters,
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
        data: list[WidgetBaseManagerPrivateModel] = []

        proxyModel = QSortFilterProxyModel(self)
        model = WidgetBaseManagerModel(data, self.__type, self)
        proxyModel.setSourceModel(model)
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
            1, WidgetBaseManagerEditorDelegate(data, self.tableView_property)
        )
