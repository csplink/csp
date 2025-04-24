/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        summary.ts
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

import type {
  SummaryClockTreeType,
  SummaryDocumentType,
  SummaryDocumentUnitType,
  SummaryLinkerType,
  SummaryModuleType,
  SummaryModuleUintType,
  SummaryPinType,
  SummaryType,
} from '@/electron/database'
import type { App } from 'vue'
import type { IpManager } from './ip'
import { inject } from 'vue'
import { I18n } from './i18n'

// #region typedef

export class Summary {
  private _origin: SummaryType
  private _clockTree?: SummaryClockTree
  private _vendorUrl?: I18n
  private _documents?: SummaryDocument
  private _illustrate?: I18n
  private _introduction?: I18n
  private _modules?: SummaryModule
  private _url?: I18n
  private _linker?: SummaryLinker
  private _pins?: Record<string, SummaryPin>

  private _moduleList?: Record<string, SummaryModuleUnit>
  private _pinInstance?: string

  constructor(origin: SummaryType) {
    this._origin = origin
  }

  get origin(): SummaryType {
    return this._origin
  }

  get name(): string {
    return this._origin.name
  }

  get clockTree(): SummaryClockTree {
    return this._clockTree ??= new SummaryClockTree(this._origin.clockTree)
  }

  get vendor(): string {
    return this._origin.vendor
  }

  get vendorUrl(): I18n {
    return this._vendorUrl ??= new I18n(this._origin.vendorUrl)
  }

  get documents(): SummaryDocument {
    return this._documents ??= new SummaryDocument(this._origin.documents)
  }

  get hals(): string[] {
    return this._origin.hals
  }

  get hasPowerPad(): boolean {
    return this._origin.hasPowerPad
  }

  get illustrate(): I18n {
    return this._illustrate ??= new I18n(this._origin.illustrate)
  }

  get introduction(): I18n {
    return this._introduction ??= new I18n(this._origin.introduction)
  }

  get modules(): SummaryModule {
    return this._modules ??= new SummaryModule(this._origin.modules)
  }

  get package(): string {
    return this._origin.package
  }

  get url(): I18n {
    return this._url ??= new I18n(this._origin.url)
  }

  get builder(): Record<string, Record<string, string[]>> {
    return this._origin.builder
  }

  get linker(): SummaryLinker | null {
    if (this._origin.linker) {
      return this._linker ??= new SummaryLinker(this._origin.linker)
    }
    else {
      return null
    }
  }

  get pins(): Record<string, SummaryPin> {
    if (!this._pins) {
      this._pins = {}
      const pinData = this._origin.pins
      for (const [name, value] of Object.entries(pinData)) {
        this._pins[name] = new SummaryPin(value)
      }
    }
    return this._pins
  }

  moduleList(): Record<string, SummaryModuleUnit> {
    if (!this._moduleList) {
      this._moduleList = {}
      for (const group of [this.modules.peripherals, this.modules.middlewares]) {
        for (const groupMap of Object.values(group)) {
          for (const [name, unit] of Object.entries(groupMap)) {
            this._moduleList[name] = unit
          }
        }
      }
    }
    return this._moduleList
  }

  pinInstance(): string {
    if (!this._pinInstance) {
      for (const pin of Object.values(this.pins)) {
        if (pin.modes.length > 0) {
          this._pinInstance = pin.modes[0].split(':')[0]
          break
        }
      }
    }
    return this._pinInstance ?? ''
  }
}

export class SummaryClockTree {
  private _origin: SummaryClockTreeType

  constructor(_origin: SummaryClockTreeType) {
    this._origin = _origin
  }

  get origin(): SummaryClockTreeType {
    return this._origin
  }

  get svg(): string {
    return this._origin.svg
  }

  get ip(): string {
    return this._origin.ip
  }
}

export class SummaryDocument {
  private _origin: SummaryDocumentType
  private _datasheets?: Record<string, SummaryDocumentUnit>
  private _errata?: Record<string, SummaryDocumentUnit>
  private _references?: Record<string, SummaryDocumentUnit>

  constructor(_origin: SummaryDocumentType) {
    this._origin = _origin
  }

  get origin(): SummaryDocumentType {
    return this._origin
  }

  private _getUnits(units: Record<string, SummaryDocumentUnitType>) {
    const result: Record<string, SummaryDocumentUnit> = {}
    for (const [key, value] of Object.entries(units)) {
      result[key] = new SummaryDocumentUnit(value)
    }
    return result
  }

  get datasheets() {
    return this._datasheets ??= this._getUnits(this._origin.datasheets ?? {})
  }

  get errata() {
    return this._errata ??= this._getUnits(this._origin.errata ?? {})
  }

  get references() {
    return this._references ??= this._getUnits(this._origin.references ?? {})
  }
}

export class SummaryDocumentUnit {
  private _origin: SummaryDocumentUnitType
  private _url?: I18n

  constructor(_origin: SummaryDocumentUnitType) {
    this._origin = _origin
  }

  get origin(): SummaryDocumentUnitType {
    return this._origin
  }

  get url(): I18n {
    if (!this._url) {
      this._url = new I18n(this._origin.url)
    }
    return this._url
  }
}

export class SummaryModule {
  private _origin: SummaryModuleType
  private _peripherals?: Record<string, SummaryModuleUnit>
  private _middlewares?: Record<string, SummaryModuleUnit>

  constructor(_origin: SummaryModuleType) {
    this._origin = _origin
  }

  private _getGroup(groups: Record<string, SummaryModuleUintType>) {
    const result: Record<string, SummaryModuleUnit> = {}
    for (const [name, unit] of Object.entries(groups)) {
      result[name] = new SummaryModuleUnit(unit)
    }
    return result
  }

  get peripherals() {
    return this._peripherals ??= this._getGroup(this._origin.peripherals)
  }

  get middlewares() {
    return this._middlewares ??= this._getGroup(this._origin.middlewares)
  }
}

export class SummaryModuleUnit {
  private _origin: SummaryModuleUintType
  private _description?: I18n
  private _children?: Record<string, SummaryModuleUnit>

  constructor(_origin: SummaryModuleUintType) {
    this._origin = _origin
  }

  get origin(): SummaryModuleUintType {
    return this._origin
  }

  get description(): I18n {
    if (!this._description) {
      this._description = new I18n(this._origin.description ?? { en: '' })
    }
    return this._description
  }

  get define(): string {
    return this._origin.define ?? ''
  }

  get children(): Record<string, SummaryModuleUnit> {
    if (!this._children) {
      this._children = {}
      const childrenData = this._origin.children ?? {}
      for (const [name, value] of Object.entries(childrenData)) {
        this._children[name] = new SummaryModuleUnit(value)
      }
    }
    return this._children
  }
}

export class SummaryLinker {
  private _origin: SummaryLinkerType

  constructor(_origin: SummaryLinkerType) {
    this._origin = _origin
  }

  get origin(): SummaryLinkerType {
    return this._origin
  }

  private parseSize(size: string): number {
    return Number.parseInt(size, 16)
  }

  get defaultHeapSize(): number {
    if (typeof (this._origin.defaultHeapSize) === 'string') {
      return this.parseSize(this._origin.defaultHeapSize)
    }
    else {
      return this._origin.defaultHeapSize ?? -1
    }
  }

  get defaultStackSize(): number {
    if (typeof (this._origin.defaultStackSize) === 'string') {
      return this.parseSize(this._origin.defaultStackSize)
    }
    else {
      return this._origin.defaultStackSize ?? -1
    }
  }
}

export class SummaryPin {
  private _origin: SummaryPinType
  private _functions?: string[]

  constructor(_origin: SummaryPinType) {
    this._origin = _origin
  }

  get origin(): SummaryPinType {
    return this._origin
  }

  get position(): number {
    if (typeof (this._origin.position) === 'number') {
      return this._origin.position
    }
    else {
      return -1
    }
  }

  get type(): string {
    return this._origin.type
  }

  get signals(): string[] {
    return this._origin.signals ?? []
  }

  get modes(): string[] {
    return this._origin.modes ?? []
  }

  functions(): string[] {
    return this._functions ??= [...this.signals, ...this.modes]
  }
}

// #endregion

export class SummaryManager {
  private _ipManager: IpManager
  private _map: Record<string, Record<string, Summary>> = {}

  constructor(ipManager: IpManager) {
    this._ipManager = ipManager
  }

  async load(vendor: string, name: string) {
    const content = await window.electron.invoke('database:getSummary', vendor, name) as SummaryType
    if (content) {
      const summary = new Summary(content)

      this._loadIpPeripherals(summary.modules.peripherals, summary.vendor);

      (this._map[vendor] ??= {})[name] = summary
    }
  }

  get(vendor: string, name: string): Summary | null {
    if (this._map[vendor]?.[name]) {
      return this._map[vendor][name]
    }

    return null
  }

  private _loadIpPeripherals(modules: Record<string, SummaryModuleUnit>, vendor: string) {
    for (const [name, module] of Object.entries(modules)) {
      if (module.define) {
        this._ipManager.loadPeripheral(vendor, name, module.define)
      }
      if (module.children) {
        this._loadIpPeripherals(module.children, vendor)
      }
    }
  }
}

export function createSummaryManagerPlugin(ipManager: IpManager) {
  const manager = new SummaryManager(ipManager)

  return {
    value: manager,
    plugin: {
      install(app: App) {
        app.provide('database:summaryManager', manager)
      },
    },
  }
}

export function useSummaryManager(): SummaryManager {
  return inject('database:summaryManager')!
}
