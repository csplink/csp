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
# @file        base.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-11-05     xqyjlj       initial version
#

from __future__ import annotations

import xml.etree.ElementTree as etree


class Base:
    """Base class for CMX XML element wrappers.

    Provides common functionality for accessing XML element attributes
    and standard string representation.
    """

    def __init__(self, root: etree.Element, namespace: dict[str, str]):
        """Initialize the element wrapper.

        Args:
            root: The XML element to wrap
            namespace: XML namespace dictionary for XPath queries
        """
        self._root = root
        self._namespace = namespace

    def __str__(self) -> str:
        """Return the XML string representation of the element."""
        return etree.tostring(self._root, encoding="utf-8").decode("utf-8")

    @property
    def root(self) -> etree.Element:
        """Get the underlying XML element."""
        return self._root

    def _get_str_attr(self, name: str, default: str = "") -> str:
        """Get a string attribute value.

        Args:
            name: Attribute name
            default: Default value if attribute doesn't exist

        Returns:
            The attribute value or default
        """
        return self._root.attrib.get(name, default)

    def _get_float_attr(self, name: str, default: float = 0.0) -> float:
        """Get a float attribute value.

        Args:
            name: Attribute name
            default: Default value if attribute doesn't exist or is invalid

        Returns:
            The attribute value as float or default
        """
        value = self._root.attrib.get(name, "")
        try:
            return float(value) if value else default
        except ValueError:
            return default

    def _get_bool_attr(self, name: str, default: bool = False) -> bool:
        """Get a boolean attribute value.

        Args:
            name: Attribute name
            default: Default value if attribute doesn't exist

        Returns:
            True if attribute is "true", False if "false" or default
        """
        return self._root.attrib.get(name, "false" if not default else "true") == "true"
