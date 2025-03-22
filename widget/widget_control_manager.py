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
# @file        widget_control_manager.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-07-02     xqyjlj       initial version
#

from loguru import logger
from common import PROJECT, IP, VALUE_HUB, SUMMARY, SIGNAL_BUS
from utils import Express
from .widget_base_manager import WidgetBaseManager, WidgetBaseManagerType


class WidgetControlManager(WidgetBaseManager):

    def __init__(self, parent=None):
        super().__init__(WidgetBaseManagerType.CONTROL, parent)

        PROJECT.project().configs.configs_changed.connect(
            self.__on_project_configsChanged
        )

    def __on_project_configsChanged(self, keys: list[str], old: str, new: str):
        if len(keys) != 2:
            return

        instance = keys[0]
        ips = IP.project_ips()

        if instance not in ips:
            logger.error(f"the ip instance:{instance!r} is invalid.")
            return

        ip = ips[instance]
        param = keys[1]

        if param not in ip.parameters:
            return

        old_value = ip.parameters[param].values.get(old, None)
        new_value = ip.parameters[param].values.get(new, None)

        if old_value is not None:
            for name, cfg in old_value.signals.items():
                signal = name.replace("${INSTANCE}", instance)
                pins = SUMMARY.find_pins_by_signal(signal)
                if len(pins) > 0:
                    pin = pins[0]
                    function_key = f"pin/{pin}/function"
                    locked_key = f"pin/{pin}/locked"
                    mode_key = f"pin/{pin}/mode"

                    PROJECT.project().configs.set(function_key, "")
                    PROJECT.project().configs.set(locked_key, False)
                    PROJECT.project().configs.set(mode_key, "")

                    SIGNAL_BUS.update_pin_triggered.emit(pin)

        if new_value is not None:
            for name, cfg in new_value.signals.items():
                signal = name.replace("${INSTANCE}", instance)
                pins = SUMMARY.find_pins_by_signal(signal)
                if len(pins) > 0:
                    pin = pins[0]
                    function_key = f"pin/{pin}/function"
                    locked_key = f"pin/{pin}/locked"
                    mode_key = f"pin/{pin}/mode"

                    PROJECT.project().configs.set(function_key, signal)
                    PROJECT.project().configs.set(locked_key, True)
                    PROJECT.project().configs.set(mode_key, cfg.mode)

                    SIGNAL_BUS.update_pin_triggered.emit(pin)

                for pin in pins:
                    print(pin, PROJECT.pin_instance().find_pin_groups(pin, signal))
