/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        packages.ts
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
 *  2025-07-31     xqyjlj       initial version
 */

import type { I18nType } from '@/electron/types'
import type { App, ShallowRef } from 'vue'
import type { Server, ServerManager } from './server'
import { inject, markRaw, shallowRef } from 'vue'
import { I18n } from '~/i18n'

// #region typedef

// #region PackageDescription

export interface PackageDescriptionWebsiteType {
  blog: string
  github: string
}

export interface PackageDescriptionAuthorType {
  name: string
  email: string
  website: PackageDescriptionWebsiteType
}

export interface PackageDescriptionType {
  name: string
  version: string
  license: string
  type: string
  vendor: string
  vendorUrl: I18nType
  description: I18nType
  url: I18nType
  support: string
  author: PackageDescriptionAuthorType
}

export class PackageDescriptionWebsite {
  private _data: PackageDescriptionWebsiteType

  constructor(data: PackageDescriptionWebsiteType) {
    this._data = data
  }

  get blog(): string {
    return this._data.blog
  }

  get github(): string {
    return this._data.github
  }
}

export class PackageDescriptionAuthor {
  private _data: PackageDescriptionAuthorType
  private _website?: PackageDescriptionWebsite

  constructor(data: PackageDescriptionAuthorType) {
    this._data = data
  }

  get name(): string {
    return this._data.name
  }

  get email(): string {
    return this._data.email
  }

  get website(): PackageDescriptionWebsite {
    return this._website ??= new PackageDescriptionWebsite(this._data.website)
  }
}

export class PackageDescription {
  private _data: PackageDescriptionType
  private _author?: PackageDescriptionAuthor
  private _vendorUrl?: I18n
  private _description?: I18n
  private _url?: I18n

  constructor(data: PackageDescriptionType) {
    this._data = data
  }

  get origin(): PackageDescriptionType {
    return this._data
  }

  get author(): PackageDescriptionAuthor {
    return this._author ??= new PackageDescriptionAuthor(this._data.author)
  }

  get name(): string {
    return this._data.name
  }

  get version(): string {
    return this._data.version
  }

  get license(): string {
    return this._data.license
  }

  get type(): string {
    return this._data.type
  }

  get vendor(): string {
    return this._data.vendor
  }

  get vendorUrl(): I18n {
    return this._vendorUrl ??= new I18n(this._data.vendorUrl)
  }

  get description(): I18n {
    return this._description ??= new I18n(this._data.description)
  }

  get url(): I18n {
    return this._url ??= new I18n(this._data.url)
  }

  get support(): string {
    return this._data.support
  }
}

// #endregion

// #region PackageIndex

export interface PackageIndexType {
  [kind: string]: {
    [name: string]: {
      [version: string]: string
    }
  }
}

export class PackageIndex {
  private _data: PackageIndexType
  private _ref: ShallowRef<PackageIndexType>

  constructor(data: PackageIndexType) {
    this._data = data
    this._ref = shallowRef(this._data)
  }

  get origin(): ShallowRef<PackageIndexType> {
    return this._ref
  }

  update(data: PackageIndexType) {
    this._data = data
    this._ref.value = this._data
  }

  types(): string[] {
    return Object.keys(this.origin.value)
  }

  items(kind: string): string[] {
    return Object.keys(this.origin.value[kind] || {})
  }

  versions(kind: string, name: string): string[] {
    return Object.keys((this.origin.value[kind] || {})[name] || {})
  }

  path(kind: string, name: string, version: string): string {
    return ((this.origin.value[kind] || {})[name] || {})[version] || ''
  }
}

// #endregion

// #endregion

export class PackageManager {
  private _packageIndex: PackageIndex | null = null
  private _server: Server
  private _descriptionCache: Record<string, PackageDescription> = markRaw({})

  constructor(server: Server) {
    this._server = markRaw(server)
  }

  async init() {
    this._packageIndex = markRaw(new PackageIndex(await this._server.packageList().catch(() => {
      return {}
    })))
  }

  get packageIndex(): PackageIndex {
    return this._packageIndex!
  }

  async getPackageDescription(kind: string, name: string, version: string): Promise<PackageDescription | undefined> {
    if (this._descriptionCache[`${kind}/${name}/${version}`]) {
      return this._descriptionCache[`${kind}/${name}/${version}`]
    }

    const description = await this._server.getPackageDescription(kind, name, version).catch(() => undefined)
    if (description) {
      this._descriptionCache[`${kind}/${name}/${version}`] = markRaw(new PackageDescription(description))
    }
    return this._descriptionCache[`${kind}/${name}/${version}`]
  }

  async reload() {
    this._packageIndex?.update(markRaw(await this._server.packageList().catch(() => {
      return {}
    })))
  }
}

export function createPackageManagerPlugin(serverManager: ServerManager) {
  const manager = new PackageManager(serverManager.server)

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('utils@packageManager', manager)
      },
    },
    async init() {
      await manager.init()
    },
  }
}

export function usePackageManager(): PackageManager {
  return inject('utils@packageManager')!
}
