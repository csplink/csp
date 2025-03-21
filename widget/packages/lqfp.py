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
# @file        lqfp.py
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# 2024-06-27     xqyjlj       initial version
#

from PySide6.QtCore import QPointF

from common import SummaryType, SUMMARY
from widget.graphics_item_chip_body import GraphicsItemChipBody
from widget.graphics_item_pin import GraphicsItemPin


class LQFP:
    PIN_WIDTH = 500
    PIN_HEIGHT = 50
    PIN_SPACING = 6
    PIN_LENGTH = 100

    def get_body_length(self, num: int):
        return self.PIN_SPACING + (self.PIN_HEIGHT + self.PIN_SPACING) * num

    def get_items(self, vendor: str, name: str):
        pins = SUMMARY.project_summary().pins
        _pins: list[tuple[str, SummaryType.PinType]] = sorted(
            pins.items(), key=lambda d: d[1].position, reverse=False
        )
        pins: dict[str, SummaryType.PinType] = {k: v for k, v in _pins}
        count = len(pins)
        num = count // 4
        items = []

        item = GraphicsItemChipBody(
            self.get_body_length(num),
            self.get_body_length(num),
            name,
            vendor,
            f"LQFP{count}",
        )
        item.setPos(QPointF(self.PIN_WIDTH, self.PIN_WIDTH))
        items.append(item)

        for name, pin in pins.items():
            position = pin.position - 1
            if position < num:
                index = position
                direction = GraphicsItemPin.Direction.LEFT_DIRECTION
                w = self.PIN_WIDTH
                h = self.PIN_HEIGHT
                x = 0
                y = (
                    index * (self.PIN_HEIGHT + self.PIN_SPACING)
                    + self.PIN_WIDTH
                    + self.PIN_SPACING
                )

            elif num <= position < 2 * num:
                index = position - num
                direction = GraphicsItemPin.Direction.BOTTOM_DIRECTION
                w = self.PIN_HEIGHT
                h = self.PIN_WIDTH
                x = (
                    index * (self.PIN_HEIGHT + self.PIN_SPACING)
                    + self.PIN_WIDTH
                    + self.PIN_SPACING
                )
                y = self.PIN_WIDTH + self.get_body_length(num)

            elif 2 * num <= position < 3 * num:
                index = position - 2 * num
                direction = GraphicsItemPin.Direction.RIGHT_DIRECTION
                w = self.PIN_WIDTH
                h = self.PIN_HEIGHT
                x = self.PIN_WIDTH + self.get_body_length(num)
                y = (
                    self.PIN_WIDTH
                    + self.get_body_length(num)
                    - (index + 1) * (self.PIN_HEIGHT + self.PIN_SPACING)
                )

            else:
                index = position - 3 * num
                direction = GraphicsItemPin.Direction.TOP_DIRECTION
                w = self.PIN_HEIGHT
                h = self.PIN_WIDTH
                x = (
                    self.PIN_WIDTH
                    + self.get_body_length(num)
                    - (index + 1) * (self.PIN_HEIGHT + self.PIN_SPACING)
                )
                y = 0

            item = GraphicsItemPin(
                w,
                h,
                self.PIN_LENGTH,
                direction,
                name,
                GraphicsItemPin.Type.RECTANGLE_TYPE,
                pin,
            )
            item.setPos(QPointF(x, y))
            items.append(item)

        return items
