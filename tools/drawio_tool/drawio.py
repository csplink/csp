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
        self.__texts = []

        with open(path, 'r', encoding='utf-8') as f:
            svg = f.read()

        self.__root = etree.fromstring(svg)
        self.__drawio = etree.fromstring(self.__root.attrib['content'])
        self.__namespace = {'ns': self.__root.tag.split('}')[0][1:] if '}' in self.__root.tag else ''}
        version = Version(self.__drawio.attrib['version'])

        mxCells: list[etree.Element] = self.__drawio.find('diagram').findall('mxGraphModel/root/mxCell')
        for mxCell in mxCells:
            id_ = mxCell.attrib['id']
            if self.__isLine(mxCell.attrib):
                self.__lines.append(id_)
            elif self.__isWidget(mxCell.attrib):
                self.__widgets.append(id_)
            elif self.__isText(mxCell.attrib):
                self.__texts.append(id_)

        self.__updateLine()
        self.__updateText()

    @property
    def svg(self) -> bytes:
        return etree.tostring(self.__root)

    @property
    def lineIds(self) -> list[str]:
        return self.__lines

    @property
    def widgetIds(self) -> list[str]:
        return self.__widgets

    def __isWidget(self, attrib: dict[str, str]) -> bool:
        # value==none && shape!=text && rounded!=none && fillColor==none
        times = 0
        if attrib.get('value', '') != '':
            return False
        styles = attrib.get('style', '').strip(';').split(';')
        for style in styles:
            if style == 'text':
                return False
            if style.startswith('rounded='):
                times += 1
                continue
            elif style == 'fillColor=none':
                times += 1
                continue

            if times == 2:
                return True
        return False

    def __isLine(self, attrib: dict[str, str]) -> bool:
        # shape==line; edge==1 && strokeColor!=none/default
        styles = attrib.get('style', '').strip(';').split(';')
        for style in styles:
            if style.startswith('strokeColor=') and style != 'strokeColor=none' and style != 'strokeColor=default':
                return False
            if style == 'line':
                return True

        if attrib.get('edge', '0') == '0':
            return False

        return True

    def __isText(self, attrib: dict[str, str]) -> bool:
        # value!=none; shape==text
        if attrib.get('value', '') != '':
            return True
        styles = attrib.get('style', '').strip(';').split(';')
        for style in styles:
            if style == 'text':
                return True

        return False

    def __findSvgElement(self, id_: str) -> etree.Element:
        rtn = None

        gs = self.__root.findall('ns:g/ns:g/ns:g/ns:g', self.__namespace)
        for g in gs:
            if g.attrib['data-cell-id'] == id_:
                rtn = g
                break

        return rtn

    def __updateLine(self):
        for id_ in self.__lines:
            element = self.__findSvgElement(id_)
            self.__updateLineElement(element, id_, 'rgb(255, 0, 0)')

    def __updateText(self):
        for id_ in self.__texts:
            element = self.__findSvgElement(id_)
            self.__updateTextElement(element, id_, 'rgb(0, 255, 255)')

    def __updateLineElement(self, el: etree.Element, cellId: str, color: str):
        for e in el:
            if e.tag == '{http://www.w3.org/2000/svg}path':
                e.attrib['stroke'] = color
                if e.get('fill', 'none') != 'none':
                    e.attrib['fill'] = color
            elif e.tag == '{http://www.w3.org/2000/svg}ellipse':
                e.attrib['fill'] = color
                e.attrib['stroke'] = color

            if len(e) > 0:
                self.__updateLineElement(e, cellId, color)

    def __updateTextElement(self, el: etree.Element, cellId: str, color: str):
        for e in el:
            if e.tag == '{http://www.w3.org/2000/svg}g':
                if 'fill' in e.attrib:
                    e.attrib['fill'] = color

            if len(e) > 0:
                self.__updateTextElement(e, cellId, color)
