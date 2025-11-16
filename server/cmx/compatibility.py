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
# @file        compatibility.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2025-10-28     xqyjlj       initial version
#


from __future__ import annotations

import xml.etree.ElementTree as etree


class CmxCompatibility:

    class Rule:
        class Description:
            def __init__(self, root: etree.Element, namespace: dict[str, str]):
                self.__root = root
                self.__namespace = namespace

            def __str__(self) -> str:
                return etree.tostring(self.__root, encoding="utf-8").decode("utf-8")

            @property
            def root(self) -> etree.Element:
                return self.__root

            @property
            def mxdb_version(self) -> str:
                return self.__root.findtext("ns:MXDBVersion", "", self.__namespace)

            @property
            def rule_type(self) -> str:
                return self.__root.findtext("ns:RuleType", "", self.__namespace)

            @property
            def matcher_on_key(self) -> str:
                return self.__root.findtext("ns:MatcherOnKey", "", self.__namespace)

            @property
            def matcher_patterns(self) -> list[str]:
                return self.__root.findtext(
                    "ns:MatcherPattern", "", self.__namespace
                ).split("|")

            @property
            def match_to_pattern(self) -> str:
                return self.__root.findtext("ns:MatchToPattern", "", self.__namespace)

            @property
            def separator_on_value(self) -> str:
                return self.__root.findtext("ns:SeparatorOnValue", "", self.__namespace)

            @property
            def matcher_condition(self) -> str:
                return self.__root.findtext("ns:MatcherCondition", "", self.__namespace)

            @property
            def parser_condition(self) -> str:
                return self.__root.findtext("ns:ParserCondition", "", self.__namespace)

        def __init__(self, root: etree.Element, namespace: dict[str, str]):
            self.__root = root
            self.__namespace = namespace

            desc_node = self.__root.find("description")
            self.__description = (
                CmxCompatibility.Rule.Description(desc_node, self.__namespace)
                if desc_node is not None
                else None
            )

        def __str__(self) -> str:
            return etree.tostring(self.__root, encoding="utf-8").decode("utf-8")

        @property
        def root(self) -> etree.Element:
            return self.__root

        @property
        def name(self) -> str:
            return self.__root.attrib.get("name", "")

        @property
        def description(self) -> Description | None:
            return self.__description

    def __init__(self, path: str):
        tree = etree.parse(path)
        self.__root = tree.getroot()

        self.__namespace = {
            "ns": self.__root.tag.split("}")[0][1:] if "}" in self.__root.tag else ""
        }
        tag = self.__root.tag
        assert tag == "rules", "invalid compatibility xml file"

        self.__rules: dict[str, CmxCompatibility.Rule] = {}
        for node in self.__root.findall("ns:rule", self.__namespace):
            name = node.attrib.get("name", "")
            if name:
                self.__rules[name] = CmxCompatibility.Rule(node, self.__namespace)

    def __str__(self) -> str:
        return etree.tostring(self.__root, encoding="utf-8").decode("utf-8")

    @property
    def root(self) -> etree.Element:
        return self.__root

    @property
    def rules(self) -> dict[str, Rule]:
        return self.__rules
