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

from packaging.version import Version


class MxCellType:

    def __init__(self, element: etree.Element):
        self.__origin = element
        self.__id = element.get('id', '')
        self.__value = element.get('value', '')
        self.__parent = int(element.get('parent', '0'))
        self.__vertex = int(element.get('vertex', '0'))
        self.__edge = int(element.get('edge', '0'))

        self.__shape = []
        self.__style = {}
        styles = element.get('style', '').strip(';').split(';')
        for style in styles:
            if '=' in style:
                ss = style.split('=')
                self.__style[ss[0]] = ss[1]
            else:
                self.__shape.append(style)

    @property
    def origin(self) -> etree.Element:
        return self.__origin

    @property
    def id(self) -> str:
        return self.__id

    @property
    def value(self) -> str:
        return self.__value

    @property
    def shape(self) -> list[str]:
        return self.__shape

    @property
    def style(self) -> dict[str, str]:
        return self.__style

    @property
    def parent(self) -> int:
        return self.__parent

    @property
    def vertex(self) -> int:
        return self.__vertex

    @property
    def edge(self) -> int:
        return self.__edge


class Drawio:

    def __init__(self, path: str):
        self.__lines = {}
        self.__widgets = {}
        self.__texts = {}
        self.__graphics = {}

        with open(path, 'r', encoding='utf-8') as f:
            svg = f.read()

        self.__root = etree.fromstring(svg)
        self.__drawio = etree.fromstring(self.__root.attrib['content'])
        self.__namespace = {'ns': self.__root.tag.split('}')[0][1:] if '}' in self.__root.tag else ''}
        version = Version(self.__drawio.attrib['version'])
        objects: list[etree.Element] = self.__drawio.find('diagram').findall('mxGraphModel/root/object')
        mxCells: list[etree.Element] = self.__drawio.find('diagram').findall('mxGraphModel/root/mxCell')

        for obj in objects:
            id_ = obj.attrib['id']
            mxCell = obj.find('mxCell')
            mxCell.attrib['id'] = id_
            mxCells.append(mxCell)
        for mxCell in mxCells:
            cell = MxCellType(mxCell)
            id_ = mxCell.attrib['id']
            if self.__isWidget(cell):
                mxGeometry = mxCell.find('mxGeometry')
                x = float(mxGeometry.attrib['x']) + 1
                y = float(mxGeometry.attrib['y']) + 1
                width = float(mxGeometry.attrib['width']) + 1
                height = float(mxGeometry.attrib['height']) + 1
                self.__widgets[id_] = {'x': x, 'y': y, 'width': width, 'height': height}
            # elif self.__isLine(mxCell.attrib):
            #     self.__lines.append(id_)
            # elif self.__isText(mxCell.attrib):
            #     self.__texts.append(id_)
            # elif self.__isGraphics(mxCell.attrib):
            #     self.__graphics.append(id_)

        # TODO: 根据主题不同来变换不同的时钟树配置
        # self.__updateLine()
        # self.__updateText()
        # self.__updateGraphics()

        for id_, item in self.__widgets.items():
            element = self.__findSvgElement(id_)
            self.__updateGraphicsElement(element, id_, 'rgb(0, 255, 0)')

    @property
    def svg(self) -> bytes:
        return etree.tostring(self.__root)

    @property
    def lines(self) -> dict:
        return self.__lines

    @property
    def widgets(self) -> dict[str, dict[str, float]]:
        return self.__widgets

    def __isWidget(self, mxCell: MxCellType) -> bool:
        # widget 其背景必须为透明，edge属性为0，内部无文本（非文本图形），必须为无圆角矩形或者圆形，边框宽度等于1
        fillColor = mxCell.style.get('fillColor', 'none')
        if mxCell.value != '' or mxCell.shape == 'text':
            return False
        elif mxCell.edge == 1:
            return False
        elif fillColor == 'none' or fillColor == 'default':
            strokeWidth = int(mxCell.style.get('strokeWidth', '1'))
            if strokeWidth != 1:
                return False
            elif mxCell.style.get('rounded', '') == '0' or mxCell.shape == 'ellipse':
                return True

        return False

    def __isGraphics(self, attrib: dict[str, str]) -> bool:
        # rounded!=none && fillColor!=none
        times = 0
        styles = attrib.get('style', '').strip(';').split(';')
        for style in styles:
            if style.startswith('rounded='):
                times += 1
                continue
            elif style.startswith('fillColor=') and style != 'fillColor=none' and style != 'fillColor=default':
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
        # value!=none && shape==text && fillColor!=none/default
        times = 0
        if attrib.get('value', '') != '':
            times += 1
        styles = attrib.get('style', '').strip(';').split(';')
        for style in styles:
            if style == 'text':
                times += 1
            elif style.startswith('fillColor=') and style != 'fillColor=none' and style != 'fillColor=default':
                return False

        return times > 0

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

    def __updateGraphics(self):
        for id_ in self.__graphics:
            element = self.__findSvgElement(id_)
            self.__updateGraphicsElement(element, id_, 'rgb(0, 255, 0)')

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

    def __updateGraphicsElement(self, el: etree.Element, cellId: str, color: str):
        for e in el:
            if e.tag == '{http://www.w3.org/2000/svg}rect':
                if 'stroke' in e.attrib:
                    e.attrib['stroke'] = color
            elif e.tag == '{http://www.w3.org/2000/svg}ellipse':
                if 'stroke' in e.attrib:
                    e.attrib['stroke'] = color

            if len(e) > 0:
                self.__updateGraphicsElement(e, cellId, color)
