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

from PyQt5.QtCore import QRectF, QPointF, QLineF, Qt

from common.database import Database
from widget.graphics_item_pin import GraphicsItemPin
from widget.graphics_item_chip_body import GraphicsItemChipBody


class LQFP():
    pin_width = 500
    pin_height = 50
    pin_spacing = 6

    def getBodyLength(self, num: int):
        return self.pin_spacing + (self.pin_height + self.pin_spacing) * num

    def getItems(self, vendor: str, hal: str, name: str):
        pinouts = Database.getPinout(vendor, hal, name)
        pinouts = dict(sorted(pinouts.items(), key=lambda d: d[1]["Position"], reverse=False))
        count = len(pinouts)
        num = count / 4
        items = []
        for name, pinout in pinouts.items():
            position = pinout["Position"] - 1
            if (position < num):
                index = position
                direction = GraphicsItemPin.Direction.LEFT
                w = self.pin_width
                h = self.pin_height
                x = 0
                y = index * (self.pin_height + self.pin_spacing) + self.pin_width + self.pin_spacing

            elif (position >= num and position < 2 * num):
                index = position - num
                direction = GraphicsItemPin.Direction.BOTTOM
                w = self.pin_height
                h = self.pin_width
                x = index * (self.pin_height + self.pin_spacing) + self.pin_width + self.pin_spacing
                y = self.pin_width + self.getBodyLength(num)

            elif (position >= 2 * num and position < 3 * num):
                index = 3 * num - position
                direction = GraphicsItemPin.Direction.RIGHT
                w = self.pin_width
                h = self.pin_height
                x = self.pin_width + self.getBodyLength(num)
                y = self.pin_width + self.getBodyLength(num) - index * (self.pin_height + self.pin_spacing)

            else:
                index = 4 * num - position
                direction = GraphicsItemPin.Direction.TOP
                w = self.pin_height
                h = self.pin_width
                x = self.pin_width + self.getBodyLength(num) - index * (self.pin_height + self.pin_spacing)
                y = 0

            item = GraphicsItemPin(w, h, direction, name)
            item.setPos(QPointF(x, y))
            items.append(item)

        item = GraphicsItemChipBody(self.getBodyLength(num), self.getBodyLength(num), name, vendor, f"LQFP{count}")
        item.setPos(QPointF(self.pin_width, self.pin_width))
        items.append(item)
        return items
