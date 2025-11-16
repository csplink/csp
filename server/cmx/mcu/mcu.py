#!/usr/bin/env python3
# -*- coding:utf-8 -*-

# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        mcu.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import xml.etree.ElementTree as etree
from typing import Any

from .base import Base
from .current import Current
from .ip import Ip
from .pin import Pin
from .temperature import Temperature
from .voltage import Voltage


class Mcu(Base):
    """Represents an MCU configuration from CMX XML file."""

    def __init__(self, path: str):
        """Initialize MCU from XML file path.

        Args:
            path: Path to the MCU XML file

        Raises:
            AssertionError: If the XML file is not a valid MCU file
        """
        tree = etree.parse(path)
        root = tree.getroot()

        namespace = {"ns": root.tag.split("}")[0][1:] if "}" in root.tag else ""}
        tag = root.tag.split("}")[-1]

        assert tag == "Mcu", "invalid mcu xml file"

        super().__init__(root, namespace)

        self.__ram_sizes: list[float] = []
        for ram in self._root.findall("ns:Ram", self._namespace):
            if ram.text:
                self.__ram_sizes.append(float(ram.text))
        self.__flash_sizes: list[float] = []
        for flash in self._root.findall("ns:Flash", self._namespace):
            if flash.text:
                self.__flash_sizes.append(float(flash.text))

        # Parse electrical characteristics
        voltage_node = self._root.find("ns:Voltage", self._namespace)
        self.__voltage = (
            Voltage(voltage_node, self._namespace) if voltage_node is not None else None
        )

        current_node = self._root.find("ns:Current", self._namespace)
        self.__current = (
            Current(current_node, self._namespace) if current_node is not None else None
        )

        temp_node = self._root.find("ns:Temperature", self._namespace)
        self.__temperature = (
            Temperature(temp_node, self._namespace) if temp_node is not None else None
        )

        self.__ips: dict[str, Ip] = {}
        for node in self._root.findall("ns:IP", self._namespace):
            name = node.attrib.get("InstanceName", "")
            self.__ips[name] = Ip(node, self._namespace)

        self.__pins: dict[str, Pin] = {}
        for node in self._root.findall("ns:Pin", self._namespace):
            name = node.attrib.get("Name", "")
            self.__pins[name] = Pin(node, self._namespace)

        self.__context = self.build_context()

        signals = set()
        for name, pin in self.pins.items():
            signals.update(pin.signals.keys())
        self.__signals = sorted(list(signals))

    @property
    def ref_name(self) -> str:
        """Reference name of the MCU."""
        return self._get_str_attr("RefName")

    @property
    def family(self) -> str:
        """MCU family name."""
        return self._get_str_attr("Family")

    @property
    def line(self) -> str:
        """MCU line name."""
        return self._get_str_attr("Line")

    @property
    def package(self) -> str:
        """Package type."""
        return self._get_str_attr("Package")

    @property
    def clock_tree(self) -> str:
        """Clock tree configuration."""
        return self._get_str_attr("ClockTree")

    @property
    def io_type(self) -> str:
        """IO type configuration."""
        return self._get_str_attr("IOType")

    @property
    def has_power_pad(self) -> bool:
        """Whether the MCU has a power pad."""
        return self._get_bool_attr("HasPowerPad")

    @property
    def db_version(self) -> str:
        """Database version."""
        return self._get_str_attr("DBVersion")

    @property
    def core(self) -> str:
        """CPU core type."""
        return self._root.findtext("ns:Core", "", self._namespace)

    @property
    def frequency(self) -> float:
        """Maximum frequency in Hz."""
        freq_text = self._root.findtext("ns:Frequency", "", self._namespace)
        try:
            return float(freq_text) if freq_text else 0.0
        except ValueError:
            return 0.0

    @property
    def ram_sizes(self) -> list[float]:
        """Available RAM sizes in KB."""
        return self.__ram_sizes

    @property
    def flash_sizes(self) -> list[float]:
        """Available Flash sizes in KB."""
        return self.__flash_sizes

    @property
    def io_count(self) -> int:
        """Number of IO pins."""
        io_text = self._root.findtext("ns:IONb", "", self._namespace)
        try:
            return int(io_text) if io_text else 0
        except ValueError:
            return 0

    @property
    def die(self) -> str:
        """Die name."""
        return self._root.findtext("ns:Die", "", self._namespace)

    @property
    def voltage(self) -> Voltage | None:
        """Voltage characteristics."""
        return self.__voltage

    @property
    def current(self) -> Current | None:
        """Current consumption characteristics."""
        return self.__current

    @property
    def temperature(self) -> Temperature | None:
        """Temperature range characteristics."""
        return self.__temperature

    @property
    def ips(self) -> dict[str, Ip]:
        """Available IP modules."""
        return self.__ips

    @property
    def pins(self) -> dict[str, Pin]:
        """Available pins."""
        return self.__pins

    @property
    def description(self) -> str:
        """MCU description."""
        return self._root.findtext("ns:Description", "", self._namespace)

    @property
    def context(self) -> dict[str, Any]:
        """Context dictionary for expression evaluation."""
        return self.__context

    @property
    def signals(self) -> list[str]:
        """Available signal names."""
        return self.__signals

    def build_context(self) -> dict[str, Any]:
        """Build context dictionary for expression evaluation.

        Returns:
            Dictionary containing context information about the MCU
            including IP existence flags and MCU characteristics.
        """
        result = {}

        for key in self.ips.keys():
            result[f"{key}_Exist"] = True

        result[self.family] = True
        result[self.line] = True
        result[self.package] = True
        result[self.die] = True

        return result
