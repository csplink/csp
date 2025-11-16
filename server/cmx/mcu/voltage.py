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
# @file        voltage.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import xml.etree.ElementTree as etree

from .base import Base


class Voltage(Base):
    """Represents voltage characteristics of an MCU."""

    def __init__(self, root: etree.Element, namespace: dict[str, str]):
        """Initialize voltage information from XML element.

        Args:
            root: XML element containing voltage information
            namespace: XML namespace dictionary
        """
        super().__init__(root, namespace)

    @property
    def min(self) -> float:
        """Minimum operating voltage in volts."""
        return self._get_float_attr("Min")

    @property
    def max(self) -> float:
        """Maximum operating voltage in volts."""
        return self._get_float_attr("Max")
