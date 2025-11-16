/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        base.ts
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
 *  2025-05-24     xqyjlj       initial version
 */

import type { Pin } from '~/utils'

export interface PackageModelType {
  width: number
  height: number
  body: PackageModelBodyType
  pins: PackageModelPinType[]
}

export interface PackageModelBodyType {
  name: string
  vendor: string
  package: string
  width: number
  height: number
  x: number
  y: number
  rotation: number
}

export interface PackageModelPinType {
  name: string
  position: number
  width: number
  height: number
  x: number
  y: number
  rotation: number
  direction: string
  pin: Pin
  label: {
    width: number
    height: number
    x: number
    y: number
    align: string
  }
}

export class IPackageBase {
  constructor(
    protected _name: string,
    protected _vendor: string,
    protected _pins: Record<string, Pin>,
  ) {
  }

  async getPackageModel(): Promise<PackageModelType | null> {
    throw new Error('getPackageModel() must be implemented by subclass.')
  }
}
