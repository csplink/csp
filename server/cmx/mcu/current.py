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
# @file        current.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import xml.etree.ElementTree as etree

from .base import Base


class Current(Base):
    """Represents current consumption characteristics of an MCU."""

    def __init__(self, root: etree.Element, namespace: dict[str, str]):
        """Initialize current information from XML element.

        Args:
            root: XML element containing current information
            namespace: XML namespace dictionary
        """
        super().__init__(root, namespace)

    @property
    def run(self) -> float:
        """Running current consumption in mA."""
        return self._get_float_attr("Run")

    @property
    def lowest(self) -> float:
        """Lowest sleep mode current consumption in mA."""
        return self._get_float_attr("Lowest")
