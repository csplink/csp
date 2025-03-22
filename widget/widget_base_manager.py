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

from typing import Any
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
from PySide6.QtGui import (
    QRegularExpressionValidator,
    QFont,
    QMouseEvent,
    QColor,
    QBrush,
)
from PySide6.QtWidgets import (
    QWidget,
    QHeaderView,
    QAbstractItemView,
    QStyleOptionViewItem,
    QApplication,
    QVBoxLayout,
    QTableView,
    QComboBox,
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


class WidgetBaseManagerWorkType(Enum):
    NORMAL_MODE = 0
    PIN_MODE = 1
    CONTROL = 2


class _PModel:

    def __init__(
        self,
        name: str,
        path: str,
        value: str | int | float | bool,
        possible_values: list[str] = [],
        description: str = "",
        param: str = "",
        parameter: IpType.ParameterUnitType = IpType.ParameterUnitType({}, None),
    ):
        self.__name = name
        self.__path = path
        self.__value = value
        self.__possible_values = possible_values
        self.__description = description
        self.__param = param
        self.__parameter = parameter
        self.__property = {}

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
    def possible_values(self) -> list[str]:
        return self.__possible_values

    @possible_values.setter
    def possible_values(self, value: list[str]):
        self.__possible_values = value

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

    def set_property(self, name: str, value: Any):
        self.__property[name] = value

    def get_property(self, name: str, default: Any = None) -> Any:
        return self.__property.get(name, default)


class WidgetBaseManagerEditorDelegate(TableItemDelegate):

    def __init__(self, data_models: list[_PModel], parent: QTableView):
        super().__init__(parent)

        self.__data_models = data_models

    # region overrides

    def editorEvent(
        self,
        event: QEvent,
        model: QAbstractItemModel,
        option: QStyleOptionViewItem,
        index: QModelIndex,
    ) -> bool:
        column = index.column()
        row = index.row()

        data_model = self.__data_models[row]

        # for boolean type, click to toggle value (check box)
        if column == 1 and data_model.type == "boolean":
            if (
                event.type() == QEvent.Type.MouseButtonRelease
                or event.type() == QEvent.Type.MouseButtonDblClick
            ):
                mouse_event: QMouseEvent = event  # type: ignore
                if mouse_event.button() == Qt.MouseButton.LeftButton:
                    x = option.rect.x() + 15  # type: ignore
                    y = option.rect.center().y() - 9.5  # type: ignore
                    rect = QRectF(x, y, 19, 19)
                    if rect.contains(mouse_event.pos()):
                        return model.setData(
                            index,
                            not data_model.value,
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

        data_model = self.__data_models[row]

        if data_model.type == "string":
            line_edit = LineEdit(parent)
            line_edit.setProperty("transparent", False)
            line_edit.setStyle(QApplication.style())
            line_edit.setText(data_model.value)  # type: ignore
            line_edit.setValidator(
                QRegularExpressionValidator(
                    QRegularExpression("^[A-Za-z_][A-Za-z0-9_]+$")
                )
            )
            return line_edit
        elif data_model.type == "enum":
            combo_box = QComboBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(combo_box)
            # combo_box.setStyle(QApplication.style())
            for value in data_model.possible_values:
                combo_box.addItem(IP.iptr(data_model.param, value))
            combo_box.setCurrentText(IP.iptr(data_model.param, data_model.value))  # type: ignore
            return combo_box
        elif data_model.type == "integer":
            spin_box = SpinBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(spin_box)
            parameter = data_model.parameter
            if parameter.max > -1:
                spin_box.setMaximum(int(parameter.max))
                spin_box.setMinimum(int(parameter.min))
            spin_box.setValue(data_model.value)  # type: ignore
            return spin_box
        elif data_model.type == "float":
            spin_box = DoubleSpinBox(parent)
            Style.WIDGET_BASE_MANAGER.apply(spin_box)
            parameter = data_model.parameter
            if parameter.max > -1:
                spin_box.setMaximum(parameter.max)
                spin_box.setMinimum(parameter.min)
            spin_box.setValue(data_model.value)  # type: ignore
            return spin_box
        else:
            logger.warning(f"unknown type {data_model.type!r}")

        return None

    def setModelData(
        self, editor: QWidget, model: QAbstractItemModel, index: QModelIndex
    ):
        column = index.column()
        row = index.row()
        if column == 0:
            return

        data_model = self.__data_models[row]

        if data_model.type == "string":
            line_edit: LineEdit = editor  # type: ignore
            model.setData(index, line_edit.text(), Qt.ItemDataRole.EditRole)
        elif data_model.type == "enum":
            combo_box: ComboBox = editor  # type: ignore
            model.setData(index, combo_box.currentText(), Qt.ItemDataRole.EditRole)
        elif data_model.type == "integer":
            spin_box: SpinBox = editor  # type: ignore
            model.setData(index, spin_box.value(), Qt.ItemDataRole.EditRole)
        elif data_model.type == "float":
            spin_box: SpinBox = editor  # type: ignore
            model.setData(index, spin_box.value(), Qt.ItemDataRole.EditRole)
        else:
            logger.warning(f"unknown type {data_model.type!r}")

    # endregion


class WidgetBaseManagerModel(QAbstractTableModel):
    def __init__(
        self,
        data_models: list[_PModel],
        type_: WidgetBaseManagerType,
        parent=None,
    ):
        super().__init__(parent)

        self.__data_models = data_models
        self.__type = type_
        self.__pin_instance = SUMMARY.project_summary().pin_instance()
        self.__ip = None
        self.__work_type = WidgetBaseManagerWorkType.CONTROL

        self.__pre_build_parameters = {
            "name": IpType.ParameterUnitType(
                {
                    "type": "string",
                    "readonly": True,
                },
                None,
            ),
            "label": IpType.ParameterUnitType(
                {
                    "type": "string",
                    "readonly": False,
                },
                None,
            ),
        }

        self.__font = QFont("JetBrains Mono")
        self.__font.setPixelSize(12)

    # region overrides

    def rowCount(self, parent: QModelIndex) -> int:
        return len(self.__data_models)

    def columnCount(self, parent: QModelIndex) -> int:
        return 2

    def data(self, index: QModelIndex, role: Qt.ItemDataRole) -> Any:
        column = index.column()
        row = index.row()

        if len(self.__data_models) == 0:
            return

        data_model = self.__data_models[row]

        if (
            role == Qt.ItemDataRole.DisplayRole or role == Qt.ItemDataRole.EditRole
        ):  # 0, 2
            if column == 0:
                return data_model.name
            elif column == 1:
                if data_model.type == "boolean":
                    return None
                return IP.iptr(data_model.param, data_model.value)  # type: ignore
        elif role == Qt.ItemDataRole.DecorationRole:  # 1
            return None
        elif role == Qt.ItemDataRole.ToolTipRole:  # 3
            if column == 1:
                return data_model.description
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
            if not self.flags(index) & Qt.ItemFlag.ItemIsEnabled:
                brush = QBrush()
                brush.setColor(QColor(133, 133, 133))
                return brush
            return None
        elif role == Qt.ItemDataRole.CheckStateRole:  # 10
            if column == 1:
                if data_model.type == "boolean":
                    return (
                        Qt.CheckState.Checked
                        if data_model.value
                        else Qt.CheckState.Unchecked
                    )
        elif role == Qt.ItemDataRole.SizeHintRole:  # 13
            return None
        else:
            return None

    def setData(self, index: QModelIndex, value: object, role: int) -> bool:
        column = index.column()
        row = index.row()

        if len(self.__data_models) == 0:
            return False

        data_model = self.__data_models[row]

        if role == Qt.ItemDataRole.EditRole and column == 1:
            if data_model.type == "string":
                PROJECT.project().configs.set(data_model.path, value)
                data_model.value = value  # type: ignore
            elif data_model.type == "enum":
                val = IP.iptr2(data_model.param, value)  # type: ignore
                PROJECT.project().configs.set(data_model.path, val)
                data_model.value = value  # type: ignore
            elif data_model.type == "integer":
                PROJECT.project().configs.set(data_model.path, value)
                data_model.value = value  # type: ignore
            elif data_model.type == "float":
                PROJECT.project().configs.set(data_model.path, value)
                data_model.value = value  # type: ignore
            elif data_model.type == "boolean":
                PROJECT.project().configs.set(data_model.path, value)
                data_model.value = value  # type: ignore
            else:
                logger.warning(f"unknown type {data_model.type} with value {value}")
                return False
            return True
        else:
            return False

    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        flag = super().flags(index)
        column = index.column()
        row = index.row()

        if len(self.__data_models) == 0:
            return flag

        data_model = self.__data_models[row]
        if column == 0:
            if data_model.type == "boolean":
                flag &= Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsUserTristate
        elif column == 1:
            if data_model.readonly:
                flag &= ~Qt.ItemFlag.ItemIsEnabled
            else:
                flag |= Qt.ItemFlag.ItemIsEditable

        if not self.__is_pmodel_enabled(data_model):
            flag = Qt.ItemFlag.NoItemFlags

        return flag

    def headerData(
        self, section: int, orientation: Qt.Orientation, role: Qt.ItemDataRole
    ) -> object:
        return None

    # endregion

    def set_target(self, instance: str, target: str):
        self.__data_models.clear()

        if self.__ip:
            self.__disconnect_ip_signal(self.__ip)

        ip = IP.project_ips().get(instance)
        if ip is None:
            logger.error(f"the ip instance:{instance!r} is invalid.")
            self.modelReset.emit()
            return

        self.__ip = ip
        models = []
        if self.__type == WidgetBaseManagerType.MODE:
            if self.__pin_instance == instance:
                self.__work_type = WidgetBaseManagerWorkType.PIN_MODE
                function: str = PROJECT.project().configs.get(
                    f"pin/{target}/mode", ""
                ) or PROJECT.project().configs.get(f"pin/{target}/function", "")
                seqs = function.split(":")

                if len(seqs) == 2 and seqs[0] == self.__pin_instance:
                    mode = seqs[1]
                    models = self.__create_pin_mode_pmodels(target, mode)
                else:
                    if function:
                        logger.error(f"the pin mode function:{function!r} is invalid.")
            else:
                self.__work_type = WidgetBaseManagerWorkType.NORMAL_MODE
                models = self.__create_control_mode_pmodels(self.__ip.modes)
        else:
            self.__work_type = WidgetBaseManagerWorkType.CONTROL
            models = self.__create_control_mode_pmodels(self.__ip.controls)

        self.__data_models.extend(models)

        self.modelReset.emit()
        self.__connect_ip_signal(self.__ip)

    def __on_ip_parameter_item_updated(self, names: list[str]):
        if self.__ip is None:
            return

        self.__disconnect_ip_signal(self.__ip)
        for index, model in enumerate(self.__data_models, start=0):
            param = model.param
            if model.param in names:
                if self.__work_type == WidgetBaseManagerWorkType.PIN_MODE:
                    configs = self.__ip.pin_modes[model.get_property("mode")][
                        model.param
                    ]
                elif self.__work_type == WidgetBaseManagerWorkType.NORMAL_MODE:
                    configs = self.__ip.modes[model.param]
                else:
                    configs = self.__ip.controls[model.param]
                new_model = self.__create_pmodel(
                    model.path, param, self.__ip.parameters[model.param], configs
                )
                if new_model is None:
                    continue
                model.name = new_model.name
                model.value = new_model.value
                model.type = new_model.type
                model.possible_values = new_model.possible_values
                model.readonly = new_model.readonly
                model.description = new_model.description
                model.param = param
                model.parameter = new_model.parameter

                self.dataChanged.emit(
                    self.createIndex(index, 0), self.createIndex(index, 1)
                )
        self.__connect_ip_signal(self.__ip)

    def __on_ip_modes_updated(self):
        if self.__work_type != WidgetBaseManagerWorkType.NORMAL_MODE:
            return

        self.__data_models.clear()
        if self.__ip is None:
            logger.error(f"the ip is invalid.")
            self.modelReset.emit()
            return

        self.__disconnect_ip_signal(self.__ip)

        models = self.__create_control_mode_pmodels(self.__ip.modes)
        self.__data_models.extend(models)

        self.modelReset.emit()
        self.__connect_ip_signal(self.__ip)

    def __on_ip_controls_updated(self):
        if self.__work_type != WidgetBaseManagerWorkType.CONTROL:
            return

        self.__data_models.clear()
        if self.__ip is None:
            logger.error(f"the ip is invalid.")
            self.modelReset.emit()
            return

        self.__disconnect_ip_signal(self.__ip)

        models = self.__create_control_mode_pmodels(self.__ip.controls)
        self.__data_models.extend(models)

        self.modelReset.emit()
        self.__connect_ip_signal(self.__ip)

    def __on_ip_modes_item_updated(self, param: str, value: bool):
        print(param, value)

    def __on_ip_controls_item_updated(self, param: str, value: bool):
        print(param, value)

    def __create_pmodel(
        self,
        path: str,
        param: str,
        parameter: IpType.ParameterUnitType,
        config: IpType.ControlModeUnitType,
    ) -> _PModel | None:
        local = SETTINGS.get(SETTINGS.language).value.name()
        val = PROJECT.project().configs.get(path)
        if val is None:
            val = config.default
            PROJECT.project().configs.set(path, val)
        else:
            if parameter.type == "enum":
                if val not in parameter.values:
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
                        val = parameter.default
            elif parameter.type == "boolean":
                if not isinstance(val, bool):
                    logger.warning(
                        f"The value type {val!r}({type(val).__name__!r}) is invalid. Use default value {parameter.default!r}. ({parameter.type!r} is required)"
                    )
                    val = parameter.default
            else:
                logger.warning(f"unknown type {parameter.type!r}")

        if not parameter.visible:
            return None

        return _PModel(
            name=parameter.display.get(local),
            path=path,
            value=val,  # type: ignore
            possible_values=config.values,
            description=parameter.description.get(local),
            param=param,
            parameter=parameter,
        )

    def __is_pmodel_enabled(self, model: _PModel) -> bool:
        if self.__ip is not None:
            if self.__work_type == WidgetBaseManagerWorkType.NORMAL_MODE:
                if (
                    model.param in self.__ip.modes
                    and self.__ip.modes[model.param].condition
                ):
                    return True
                else:
                    return False
            elif self.__work_type == WidgetBaseManagerWorkType.CONTROL:
                if (
                    model.param in self.__ip.controls
                    and self.__ip.controls[model.param].condition
                ):
                    return True
                else:
                    return False
        return True

    def __create_pin_mode_pmodels(self, target: str, mode: str) -> list[_PModel]:
        results = [
            _PModel(
                name=self.tr("Name"),  # type: ignore
                path="",
                value=target,
                parameter=self.__pre_build_parameters["name"],
            ),
            _PModel(
                name=self.tr("Label"),  # type: ignore
                path=f"pin/{target}/label",
                value=PROJECT.project().configs.get(f"pin/{target}/label", ""),  # type: ignore
                parameter=self.__pre_build_parameters["label"],
            ),
        ]

        if self.__ip is None:
            return []

        configs = self.__ip.pin_modes.get(mode, {})

        parameters = self.__ip.parameters
        instance = self.__ip.instance()
        if parameters:
            for param, cfg in configs.items():
                parameter = parameters[param]
                path = f"{instance}/{target}/{param}"
                model = self.__create_pmodel(path, param, parameter, cfg)
                if model is not None:
                    model.set_property("mode", mode)
                    results.append(model)

        return results

    def __create_control_mode_pmodels(
        self, configs: dict[str, IpType.ControlModeUnitType]
    ) -> list[_PModel]:
        results = []

        if self.__ip is None:
            return []

        parameters = self.__ip.parameters
        instance = self.__ip.instance()
        if parameters:
            for param, cfg in configs.items():
                parameter = parameters[param]
                path = f"{instance}/{param}"
                model = self.__create_pmodel(path, param, parameter, cfg)
                if model is not None:
                    results.append(model)

        return results

    def __disconnect_ip_signal(self, ip: IpType):
        ip.parameter_item_updated.disconnect(self.__on_ip_parameter_item_updated)
        ip.modes_updated.disconnect(self.__on_ip_modes_updated)
        ip.controls_updated.disconnect(self.__on_ip_controls_updated)
        ip.modes_item_updated.disconnect(self.__on_ip_modes_item_updated)
        ip.controls_item_updated.disconnect(self.__on_ip_controls_item_updated)

    def __connect_ip_signal(self, ip: IpType):
        ip.parameter_item_updated.connect(self.__on_ip_parameter_item_updated)
        ip.modes_updated.connect(self.__on_ip_modes_updated)
        ip.controls_updated.connect(self.__on_ip_controls_updated)
        ip.modes_item_updated.connect(self.__on_ip_modes_item_updated)
        ip.controls_item_updated.connect(self.__on_ip_controls_item_updated)


class WidgetBaseManager(QWidget):

    def __init__(self, type_: WidgetBaseManagerType, parent=None):
        super().__init__(parent)

        # ----------------------------------------------------------------------
        self.v_layout = QVBoxLayout(self)
        self.v_layout.setContentsMargins(9, 9, 9, 9)
        self.table_view_property = TableView(self)
        self.table_view_property.horizontalHeader().hide()
        self.v_layout.addWidget(self.table_view_property)
        # ----------------------------------------------------------------------

        self.__type = type_
        self.__data_models: list[_PModel] = []
        self.__instance = ""
        self.__target = ""

        proxy_model = QSortFilterProxyModel(self)
        self.m_model = WidgetBaseManagerModel(self.__data_models, self.__type, self)
        proxy_model.setSourceModel(self.m_model)
        self.table_view_property.setModel(proxy_model)
        self.table_view_property.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.table_view_property.verticalHeader().setVisible(False)
        self.table_view_property.setBorderVisible(True)
        self.table_view_property.setBorderRadius(8)
        self.table_view_property.setSelectionMode(
            QAbstractItemView.SelectionMode.NoSelection
        )
        self.table_view_property.setItemDelegateForColumn(
            1,
            WidgetBaseManagerEditorDelegate(
                self.__data_models, self.table_view_property
            ),
        )

    # region getter/setter

    @property
    def instance(self) -> str:
        return self.__instance

    @property
    def target(self) -> str:
        return self.__target

    # endregion

    def set_target(self, instance: str, target: str):
        self.__instance = instance
        self.__target = target
        self.m_model.set_target(instance, target)

        ip = IP.project_ips()[instance]
        # for signal in ip.signals():
        #     print(signal, PROJECT.findAvailablePinsBySignal(signal))
