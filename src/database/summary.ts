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
  SummaryDocumentType,
  SummaryDocumentUnitType,
  SummaryDocumentUnitTypeType,
  SummaryLinkerType,
  SummaryModuleType,
  SummaryModuleUintType,
  SummaryPinType,
  SummaryType,
} from '@/electron/types'
import type { App, WritableComputedRef } from 'vue'
import type { ClockTreeManager } from './clockTree'
import type { IpManager } from './ip'
import { computed, inject, markRaw } from 'vue'
import { I18n } from '~/i18n'

// #region typedef

export class Summary {
  private _vendorUrl: I18n
  private _documents?: SummaryDocument
  private _illustrate: I18n
  private _introduction: I18n
  private _modules?: SummaryModule
  private _url: I18n
  private _linker?: SummaryLinker
  private _pins?: Record<string, SummaryPin>

  private _moduleList?: Record<string, SummaryModuleUnit>
  private _pinInstance?: string

  constructor(
    private _origin: SummaryType,
    public locale: WritableComputedRef<string>,
  ) {
    this._vendorUrl = new I18n(this._origin.vendorUrl)
    this._illustrate = new I18n(this._origin.illustrate)
    this._introduction = new I18n(this._origin.introduction)
    this._url = new I18n(this._origin.url)
  }

  get origin(): SummaryType {
    return this._origin
  }

  get name(): string {
    return this._origin.name
  }

  get clockTree(): string {
    return this._origin.clockTree
  }

  get vendor(): string {
    return this._origin.vendor
  }

  vendorUrl = computed(() => {
    return this._vendorUrl.get(this.locale.value)
  })

  get documents(): SummaryDocument {
    return this._documents ??= new SummaryDocument(this._origin.documents, this.locale)
  }

  get hals(): string[] {
    return this._origin.hals
  }

  get hasPowerPad(): boolean {
    return this._origin.hasPowerPad
  }

  illustrate = computed(() => {
    return this._illustrate.get(this.locale.value)
  })

  introduction = computed(() => {
    return this._introduction.get(this.locale.value)
  })

  get modules(): SummaryModule {
    return this._modules ??= new SummaryModule(this._origin.modules)
  }

  get package(): string {
    return this._origin.package
  }

  url = computed(() => {
    return this._url.get(this.locale.value)
  })

  get io(): number {
    return this._origin.io
  }

  get builders(): Record<string, Record<string, string[]>> {
    return this._origin.builders
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

  get moduleList(): Record<string, SummaryModuleUnit> {
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

  get pinInstance(): string {
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

  findPinsBySignals(signals: string[]): string[] {
    const matchedPins: string[] = []
    for (const [pinName, pin] of Object.entries(this.pins)) {
      const pinSignals = pin.signals
      if (signals.some(signal => pinSignals.includes(signal))) {
        matchedPins.push(pinName)
      }
    }
    return matchedPins
  }
}

export class SummaryDocument {
  private _datasheets?: Record<string, SummaryDocumentUnit>
  private _errata?: Record<string, SummaryDocumentUnit>
  private _references?: Record<string, SummaryDocumentUnit>

  constructor(
    private _origin: SummaryDocumentType,
    public locale: WritableComputedRef<string>,
  ) {
  }

  get origin(): SummaryDocumentType {
    return this._origin
  }

  private _getUnits(units: Record<string, SummaryDocumentUnitType>) {
    const result: Record<string, SummaryDocumentUnit> = {}
    for (const [key, value] of Object.entries(units)) {
      result[key] = new SummaryDocumentUnit(value, this.locale)
    }
    return result
  }

  get datasheets(): Record<string, SummaryDocumentUnit> {
    return this._datasheets ??= this._getUnits(this._origin.datasheets ?? {})
  }

  get errata(): Record<string, SummaryDocumentUnit> {
    return this._errata ??= this._getUnits(this._origin.errata ?? {})
  }

  get references(): Record<string, SummaryDocumentUnit> {
    return this._references ??= this._getUnits(this._origin.references ?? {})
  }

  get applications(): Record<string, SummaryDocumentUnit> {
    return this._getUnits(this._origin.applications ?? {})
  }

  get faqs(): Record<string, SummaryDocumentUnit> {
    return this._getUnits(this._origin.faqs ?? {})
  }
}

export class SummaryDocumentUnit {
  private _url: I18n

  constructor(
    private _origin: SummaryDocumentUnitType,
    public locale: WritableComputedRef<string>,
  ) {
    this._url = new I18n(this._origin.url)
  }

  get origin(): SummaryDocumentUnitType {
    return this._origin
  }

  url = computed(() => {
    return this._url.get(this.locale.value)
  })

  get type(): SummaryDocumentUnitTypeType {
    return this._origin.type
  }

  get size(): string {
    return this._origin.size
  }

  get version(): string {
    return this._origin.version
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
  private _clockTreeManager?: ClockTreeManager
  private _ipManager?: IpManager
  private _map: Record<string, Record<string, Summary>> = markRaw({})

  constructor() {
  }

  setIpManager(ipManager: IpManager) {
    this._ipManager = markRaw(ipManager)
  }

  setClockTreeManager(clockTreeManager: ClockTreeManager) {
    this._clockTreeManager = markRaw(clockTreeManager)
  }

  async load(vendor: string, name: string, locale: WritableComputedRef<string>) {
    const content = await window.electron.invoke('database:getSummary', vendor, name) as SummaryType
    if (content) {
      const summary = new Summary(content, locale)

      await this._loadIpPeripherals(summary.modules.peripherals, summary)
      await this._clockTreeManager?.load(vendor, name, summary.clockTree);

      (this._map[vendor] ??= {})[name] = markRaw(summary)
    }
  }

  get(vendor: string, name: string): Summary | null {
    if (this._map[vendor]?.[name]) {
      return this._map[vendor][name]
    }

    return null
  }

  private async _loadIpPeripherals(modules: Record<string, SummaryModuleUnit>, summary: Summary) {
    for (const [name, module] of Object.entries(modules)) {
      if (module.define) {
        await this._ipManager?.loadPeripheral(summary.vendor, name, module.define, summary)
      }
      if (module.children) {
        await this._loadIpPeripherals(module.children, summary)
      }
    }
  }
}

export function createSummaryManagerPlugin() {
  const manager = new SummaryManager()

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('database@summaryManager', manager)
      },
    },
    setIpManager(ipManager: IpManager) {
      manager.setIpManager(ipManager)
    },
    setClockTreeManager(clockTreeManager: ClockTreeManager) {
      manager.setClockTreeManager(clockTreeManager)
    },
  }
}

export function useSummaryManager(): SummaryManager {
  return inject('database@summaryManager')!
}
