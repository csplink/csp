/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        clockTree.d.ts
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
 *  2025-10-05     xqyjlj       initial version
 */

import type { XYPosition } from '@vue-flow/core'

export type ClockTreeEdgeTypeType = 'ct-smoothstep' | 'ct-cliff'
export type ClockTreeNodeTypeType = 'ct-input-number' | 'ct-output' | 'ct-select' | 'ct-radio' | 'ct-probe'
export type ClockTreeNodeUnitType = 'U' | 'K' | 'M'

export interface ClockTreeEdgeType {
  type: ClockTreeEdgeTypeType
  source: string
  target: string
  sourceHandle: string | null
  targetHandle: string | null
  label: string
}

export interface ClockTreeNodeType {
  type: ClockTreeNodeTypeType
  position?: XYPosition
  unit?: ClockTreeNodeUnitType
}

export interface ClockTreeType {
  instance: string
  edges: {
    [k: string]: ClockTreeEdgeType
  }
  nodes: {
    [k: string]: ClockTreeNodeType
  }
}
