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
# @file        drawio.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-10-21     xqyjlj       initial version
#

import xml.etree.ElementTree as etree
from pathlib import Path

from packaging.version import Version


class Drawio:

    def __init__(self, path: Path):
        self.__lines = []
        self.__widgets = []
        self.__vertex = []

        with open(path, 'r', encoding='utf-8') as f:
            svg = f.read()

        self.__root = etree.fromstring(svg)
        self.__drawio = etree.fromstring(self.__root.attrib['content'])
        version = self.__drawio.attrib['version']
        print(f'version: {version}')
        print(Version(f'V{version}'))

        mxCells: list[etree.Element] = self.__drawio.find('diagram').findall('mxGraphModel/root/mxCell')
        for mxCell in mxCells:
            id_ = mxCell.attrib['id']
            styles = mxCell.attrib.get('style', '').strip(';').split(';')
            if len(styles) > 0:
                if self.__isLineByStyles(styles):
                    self.__lines.append(id_)
                elif self.__isWidgetByStyles(styles):
                    self.__widgets.append(id_)
                elif mxCell.attrib.get('vertex', '0') == '1':
                    self.__vertex.append(id_)

        self.__findSvgElementById('11')

    @property
    def svg(self) -> bytes:
        return etree.tostring(self.__root)

    @property
    def lineIds(self) -> list[str]:
        return self.__lines

    @property
    def widgetIds(self) -> list[str]:
        return self.__widgets

    @property
    def vertexIds(self) -> list[str]:
        return self.__vertex

    def __isLineByStyles(self, styles: list[str]) -> bool:
        for style in styles:
            if style == 'line' or style.startswith('endArrow='):
                return True
        return False

    def __isWidgetByStyles(self, styles: list[str]) -> bool:
        roundedFound = False
        for style in styles:
            if not roundedFound and style.startswith('rounded='):
                roundedFound = True
                continue
            elif roundedFound and style == 'fillColor=none':
                return True
        return False

    def __findSvgElementById(self, id_: str) -> etree.Element | None:
        rtn = None

        namespace = {'ns': self.__root.tag.split('}')[0][1:] if '}' in self.__root.tag else ''}
        gs = self.__root.findall('ns:g/ns:g/ns:g/ns:g', namespace)
        for g in gs:
            if g.attrib['data-cell-id'] == id_:
                rtn = g
                break

        return rtn
