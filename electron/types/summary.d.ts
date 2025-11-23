/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        summary.d.ts
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

import type { I18nType } from './i18n'

export interface SummaryType {
  name: string
  clockTree: string
  core: string
  io: number
  die?: string
  frequency: number
  series: string
  line: string
  vendor: string
  vendorUrl: I18nType
  documents: SummaryDocumentType
  illustrate: I18nType
  introduction: I18nType
  modules: SummaryModuleType
  url: I18nType
  builders: { [k: string]: { [k: string]: string[] } }
  hals: [string, ...string[]]
  hasPowerPad: boolean
  package: string
  linker?: SummaryLinkerType
  pins: { [k: string]: SummaryPinType }
}

export interface SummaryDocumentType {
  datasheets?: { [k: string]: SummaryDocumentUnitType }
  errata?: { [k: string]: SummaryDocumentUnitType }
  references?: { [k: string]: SummaryDocumentUnitType }
  applications?: { [k: string]: SummaryDocumentUnitType }
  faqs?: { [k: string]: SummaryDocumentUnitType }
  [k: string]: unknown
}

export type SummaryDocumentUnitTypeType = 'pdf'

export interface SummaryDocumentUnitType {
  url: I18nType
  type: SummaryDocumentUnitTypeType
  size: string
  version: string
}

export interface SummaryModuleType {
  peripherals: { [k: string]: SummaryModuleUintType }
  middlewares: { [k: string]: SummaryModuleUintType }
}

export interface SummaryModuleUintType {
  description?: I18nType
  define?: string
  children?: { [k: string]: SummaryModuleUintType }
}

export interface SummaryLinkerType {
  defaultHeapSize?: number | string
  defaultStackSize: number | string
}

export interface SummaryPinType {
  position: number | string
  type: 'I/O' | 'power' | 'reset' | 'nc' | 'boot' | 'monoIO'
  signals?: [string, ...string[]]
  modes?: [string, ...string[]]
}
