/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        repository.ts
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
 *  2025-08-14     xqyjlj       initial version
 */

import type {
  $Packages$,
  Hal,
  RepositoryChipSeriesType,
  RepositoryChipsLineType,
  RepositoryChipUnitType,
  RepositoryChipVendorType,
  RepositoryType,
} from '@/electron/types'
import type { App } from 'vue'
import { inject, markRaw } from 'vue'
import { I18n } from '~/i18n'

// #region typedef

export class Repository {
  private _origin: RepositoryType
  private _chips?: Record<string, RepositoryChipVendor>
  private _packages?: RepositoryPackages

  constructor(origin: RepositoryType) {
    this._origin = origin
  }

  get origin(): RepositoryType {
    return this._origin
  }

  get chips(): Record<string, RepositoryChipVendor> {
    if (!this._chips) {
      this._chips = {}
      const chipsData = this._origin.chips
      for (const [name, value] of Object.entries(chipsData)) {
        this._chips[name] = new RepositoryChipVendor(value)
      }
    }
    return this._chips
  }

  get packages(): RepositoryPackages {
    return this._packages ??= new RepositoryPackages(this._origin.packages)
  }

  get $packages$(): $Packages$ | undefined {
    return this._origin.$packages$
  }
}

export class RepositoryChipVendor {
  private _origin: RepositoryChipVendorType
  private _content?: Record<string, RepositoryChipSeries>

  constructor(_origin: RepositoryChipVendorType) {
    this._origin = _origin
  }

  get origin(): RepositoryChipVendorType {
    return this._origin
  }

  get content(): Record<string, RepositoryChipSeries> {
    if (!this._content) {
      this._content = {}
      const contentData = this._origin.content
      for (const [name, value] of Object.entries(contentData)) {
        this._content[name] = new RepositoryChipSeries(value)
      }
    }
    return this._content
  }
}

export class RepositoryChipSeries {
  private _origin: RepositoryChipSeriesType
  private _lines?: Record<string, RepositoryChipsLine>

  constructor(_origin: RepositoryChipSeriesType) {
    this._origin = _origin
  }

  get origin(): RepositoryChipSeriesType {
    return this._origin
  }

  get lines(): Record<string, RepositoryChipsLine> {
    if (!this._lines) {
      this._lines = {}
      for (const [name, value] of Object.entries(this._origin)) {
        this._lines[name] = new RepositoryChipsLine(value)
      }
    }
    return this._lines
  }
}

export class RepositoryChipsLine {
  private _origin: RepositoryChipsLineType
  private _units?: Record<string, RepositoryChipUnit>

  constructor(_origin: RepositoryChipsLineType) {
    this._origin = _origin
  }

  get origin(): RepositoryChipsLineType {
    return this._origin
  }

  get units(): Record<string, RepositoryChipUnit> {
    if (!this._units) {
      this._units = {}
      for (const [name, value] of Object.entries(this._origin)) {
        this._units[name] = new RepositoryChipUnit(value)
      }
    }
    return this._units
  }
}

export class RepositoryChipUnit {
  private _origin: RepositoryChipUnitType

  constructor(_origin: RepositoryChipUnitType) {
    this._origin = _origin
  }

  get origin(): RepositoryChipUnitType {
    return this._origin
  }

  get core(): string {
    return this._origin.core
  }

  get current(): { lowest: number, run: number } {
    return this._origin.current
  }

  get flash(): number {
    return this._origin.flash
  }

  get frequency(): number {
    return this._origin.frequency
  }

  get io(): number {
    return this._origin.io
  }

  get package(): string {
    return this._origin.package
  }

  get peripherals(): Record<string, number> {
    return this._origin.peripherals
  }

  get ram(): number {
    return this._origin.ram
  }

  get temperature(): { max: number, min: number } {
    return this._origin.temperature
  }

  get voltage(): { max: number, min: number } {
    return this._origin.voltage
  }
}

export class RepositoryPackages {
  private _origin: {
    hal: Hal
    toolchains: Hal
    components: {
      system?: Hal
    }
  }

  private _hal?: RepositoryHal
  private _toolchains?: RepositoryHal
  private _components?: RepositoryComponents

  constructor(_origin: {
    hal: Hal
    toolchains: Hal
    components: {
      system?: Hal
    }
  }) {
    this._origin = _origin
  }

  get origin(): {
    hal: Hal
    toolchains: Hal
    components: {
      system?: Hal
    }
  } {
    return this._origin
  }

  get hal(): RepositoryHal {
    return this._hal ??= new RepositoryHal(this._origin.hal)
  }

  get toolchains(): RepositoryHal {
    return this._toolchains ??= new RepositoryHal(this._origin.toolchains)
  }

  get components(): RepositoryComponents {
    return this._components ??= new RepositoryComponents(this._origin.components)
  }
}

export class RepositoryHal {
  private _origin: Hal
  private _packages?: Record<string, RepositoryPackage>

  constructor(_origin: Hal) {
    this._origin = _origin
  }

  get origin(): Hal {
    return this._origin
  }

  get packages(): Record<string, RepositoryPackage> {
    if (!this._packages) {
      this._packages = {}
      for (const [name, value] of Object.entries(this._origin)) {
        this._packages[name] = new RepositoryPackage(value)
      }
    }
    return this._packages
  }
}

export class RepositoryComponents {
  private _origin: {
    system?: Hal
  }

  private _system?: RepositoryHal

  constructor(_origin: {
    system?: Hal
  }) {
    this._origin = _origin
  }

  get origin(): {
    system?: Hal
  } {
    return this._origin
  }

  get system(): RepositoryHal | null {
    if (this._origin.system) {
      return this._system ??= new RepositoryHal(this._origin.system)
    }
    return null
  }
}

export class RepositoryPackage {
  private _origin: $Packages$
  private _description?: I18n
  private _url?: I18n

  constructor(_origin: $Packages$) {
    this._origin = _origin
  }

  get origin(): $Packages$ {
    return this._origin
  }

  get version(): Record<string, {
    urls: string[] | { windows?: string[], linux?: string[], [k: string]: unknown }
    note: { en: string, [k: string]: unknown }
    [k: string]: unknown
  }> | undefined {
    return this._origin.version
  }

  get author(): {
    name: string
    email: string
    website: { blog?: string, github?: string, [k: string]: unknown }
    [k: string]: unknown
  } | undefined {
    return this._origin.author
  }

  get license(): string | undefined {
    return this._origin.license
  }

  get vendor(): string | undefined {
    return this._origin.vendor
  }

  //   get vendorUrl(): Url | undefined {
  //     return this._origin.vendorUrl
  //   }

  get description(): I18n | null {
    if (this._origin.description) {
      return this._description ??= new I18n(this._origin.description)
    }
    return null
  }

  get url(): I18n | null {
    if (this._origin.url) {
      return this._url ??= new I18n(this._origin.url)
    }
    return null
  }

  get support(): string | undefined {
    return this._origin.support
  }
}

// #endregion

export class RepositoryManager {
  private _repository?: Repository

  private async _get(): Promise<Repository> {
    const content = await window.electron.invoke('database:getRepository') as RepositoryType
    return new Repository(content)
  }

  async get(): Promise<Repository> {
    return this._repository ??= markRaw(await this._get())
  }
}

export function createRepositoryManagerPlugin() {
  const manager = new RepositoryManager()

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('database@repositoryManager', manager)
      },
    },
  }
}

export function useRepositoryManager(): RepositoryManager {
  return inject('database@repositoryManager')!
}
