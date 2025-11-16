/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        lqfp.ts
 *  @brief
 *
 * ****************************************************************************
 *  @attention
 *  Licensed under the Apache License v. 2 (the "License");
 *  You may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      https://www.apache.org/licenses/LICENSE-2.0.html
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 *
 *  Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
 *
 * ****************************************************************************
 *  Change Logs:
 *  Date           Author       Notes
 *  ------------   ----------   -----------------------------------------------
 *  2025-05-07     xqyjlj       initial version
 */

import type { PackageModelPinType, PackageModelType } from './base'
import { IPackageBase } from './base'

export class LQFP extends IPackageBase {
  private PIN_WIDTH = 500
  private PIN_HEIGHT = 25
  private PIN_SPACING = 6
  private PIN_LENGTH = 60

  private _get_body_length(num: number) {
    return this.PIN_SPACING + (this.PIN_HEIGHT + this.PIN_SPACING) * num
  }

  async getPackageModel(): Promise<PackageModelType | null> {
    const count = Object.keys(this._pins).length
    const num = count / 4

    const body = {
      name: this._name,
      vendor: this._vendor,
      package: `LQFP${count}`,
      x: this.PIN_WIDTH,
      y: this.PIN_WIDTH,
      width: this._get_body_length(num),
      height: this._get_body_length(num),
      rotation: 0,
    }

    const pins: PackageModelPinType[] = []
    for (const [name, pin] of Object.entries(this._pins)) {
      const position = pin.position - 1
      const width = this.PIN_LENGTH
      const height = this.PIN_HEIGHT
      let x = 0
      let y = 0
      let labelX = 0
      let labelY = 0
      let labelAlign = 'right'
      let rotation = 0
      let direction = 'left'

      if (position < num) {
        const index = position
        x = this.PIN_WIDTH - this.PIN_LENGTH
        y = index * (this.PIN_HEIGHT + this.PIN_SPACING) + this.PIN_WIDTH + this.PIN_SPACING
        labelX = 0
        labelY = y
        labelAlign = 'right'
        rotation = 0
        direction = 'left'
      }
      else if (num <= position && position < 2 * num) {
        const index = position - num
        x = index * (this.PIN_HEIGHT + this.PIN_SPACING) + this.PIN_WIDTH + this.PIN_SPACING
        y = this.PIN_WIDTH + this._get_body_length(num) + this.PIN_LENGTH
        labelX = x
        labelY = y + (this.PIN_WIDTH - this.PIN_LENGTH)
        labelAlign = 'right'
        rotation = -90
        direction = 'bottom'
      }
      else if (2 * num <= position && position < 3 * num) {
        const index = position - 2 * num
        x = this.PIN_WIDTH + this._get_body_length(num)
        y = this.PIN_WIDTH + this._get_body_length(num) - (index + 1) * (this.PIN_HEIGHT + this.PIN_SPACING)
        labelX = x + this.PIN_LENGTH
        labelY = y
        labelAlign = 'left'
        rotation = 0
        direction = 'right'
      }
      else {
        const index = position - 3 * num
        x = this.PIN_WIDTH + this._get_body_length(num) - (index + 1) * (this.PIN_HEIGHT + this.PIN_SPACING)
        y = this.PIN_WIDTH
        labelX = x
        labelY = y - this.PIN_LENGTH
        labelAlign = 'left'
        rotation = -90
        direction = 'top'
      }

      pins.push({
        name,
        position,
        width,
        height,
        x,
        y,
        rotation,
        direction,
        pin,
        label: {
          width: this.PIN_WIDTH - this.PIN_LENGTH,
          height,
          x: labelX,
          y: labelY,
          align: labelAlign,
        },
      })
    }

    return {
      width: this._get_body_length(num) + 2 * this.PIN_WIDTH,
      height: this._get_body_length(num) + 2 * this.PIN_WIDTH,
      body,
      pins,
    }
  }
}
