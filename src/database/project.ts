/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project.ts
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
 *  2025-05-22     xqyjlj       initial version
 */

import type {
  ProjectGenLinkerType,
  ProjectGenType,
  ProjectType,
} from '@/electron/database'
import type { Emitter } from 'mitt'
import type { App } from 'vue'
import type { ClockTreeManager } from './clockTree'
import type { IpManager } from './ip'
import type { SummaryManager } from './summary'
import type { ValueHub } from '~/events'
import mitt from 'mitt'

import { inject } from 'vue'

// #region typedef

// eslint-disable-next-line ts/consistent-type-definitions
export type ProjectEventType = {
  changed: void
  modulesChanged: { oldValue: string[], newValue: string[] }
}

export class Project {
  private _origin: ProjectType
  private _path: string
  private _configs?: ProjectConfigs
  private _gen?: ProjectGen
  private _emitter = mitt<ProjectEventType>()
  private _dirty = false
  private _valueHub: ValueHub
  private _ipManager: IpManager

  constructor(origin: ProjectType, path: string, valueHub: ValueHub, ipManager: IpManager) {
    this._origin = origin
    this._path = path
    this._valueHub = valueHub
    this._ipManager = ipManager

    this._emitter.on('changed', this.onChanged.bind(this))
  }

  get origin(): ProjectType {
    return this._origin
  }

  get emitter(): Emitter<ProjectEventType> {
    return this._emitter
  }

  get version(): string {
    return this._origin.version
  }

  get name(): string {
    return this._origin.name
  }

  get vendor(): string {
    return this._origin.vendor
  }

  get targetChip(): string {
    return this._origin.targetChip
  }

  get modules(): string[] {
    return this._origin.modules ??= []
  }

  get configs(): ProjectConfigs {
    if (this._configs) {
      return this._configs
    }
    else {
      this._configs = new ProjectConfigs(this._origin.configs ??= {}, this._valueHub)
      this._configs.emitter.on('changed', this.onConfigsChanged.bind(this))
      this._configs.emitter.on('configChanged', this.onConfigsConfigChanged.bind(this))
      return this._configs
    }
  }

  get gen(): ProjectGen | null {
    if (this._origin.gen) {
      return this._gen ??= new ProjectGen(this._origin.gen)
    }
    return null
  }

  private _setDirty(value: boolean) {
    if (this._dirty !== value) {
      this._dirty = value

      if (this._dirty) {
        document.title = `${this.name} *`
      }
      else {
        document.title = this.name
      }
    }
  }

  save() {
    this._setDirty(false)
    window.electron.send('database:saveProject', this.origin)
  }

  path(): string {
    return this._path
  }

  private onChanged() {
    this._setDirty(true)
  }

  private onConfigsChanged() {
    this._emitter.emit('changed')
  }

  private onConfigsConfigChanged(payload: { path: string[], oldValue: any, newValue: any }) {
    const [path] = [payload.path]

    if (path.length === 0) {
      return
    }
    const module = path[0]
    const ip = this._ipManager.getPeripheral(this.vendor, module)
    if (ip?.activated) {
      if (!(this.modules.includes(module))) {
        const old = this.modules// TODO
        this.modules.push(module)
        this.modules.sort()
        this._emitter.emit('modulesChanged', { oldValue: old, newValue: this.modules })
      }
    }
    else {
      const index = this.modules.indexOf(module)
      if (index !== -1) {
        const old = this.modules// TODO
        this._origin.modules = this.modules.filter(item => item !== module)
        this._emitter.emit('modulesChanged', { oldValue: old, newValue: this.modules })
      }
    }
  }
}

// eslint-disable-next-line ts/consistent-type-definitions
export type ProjectConfigsEventType = {
  changed: void
  pinConfigChanged: { path: string[], oldValue: any, newValue: any }
  configChanged: { path: string[], oldValue: any, newValue: any }
}

export interface ProjectConfigsPinUnitType {
  label?: string
  function?: string
  mode?: string
  locked?: boolean
}

export class ProjectConfigs {
  private _data: Record<string, any>
  private _emitter = mitt<ProjectConfigsEventType>()
  private _valueHub: ValueHub

  constructor(data: Record<string, any>, valueHub: ValueHub) {
    this._data = data
    this._valueHub = valueHub
    this._emitter.on('pinConfigChanged', this._onConfigChanged.bind(this))
    this._emitter.on('configChanged', this._onConfigChanged.bind(this))
  }

  get origin(): Record<string, any> {
    return this._data
  }

  set origin(value: Record<string, any>) {
    this._data = value
  }

  get emitter(): Emitter<ProjectConfigsEventType> {
    return this._emitter
  }

  get<T = any>(path: string, defaultValue: T = null as any): T {
    const keys = path.split('.')
    let item: any = this._data

    for (const key of keys) {
      if (!(key in item)) {
        return defaultValue
      }
      item = item[key]
    }

    return item as T
  }

  set<T = any>(path: string, value: T): void {
    const keys = path.split('.')
    let item: any = this._data

    for (const key of keys.slice(0, -1)) {
      if (!(key in item)) {
        item[key] = {}
      }
      item = item[key]
    }

    const lastKey = keys[keys.length - 1]
    const old = item[lastKey]

    if (old === value)
      return

    item[lastKey] = value

    if (
      (value === null)
      || (typeof value === 'string' && value.length === 0)
      || (Array.isArray(value) && value.length === 0)
      || (typeof value === 'object' && Object.keys(value).length === 0)
    ) {
      delete item[lastKey]
    }

    if (keys.length >= 2) {
      if (keys[0] === 'pins') {
        this._emitter.emit('pinConfigChanged', { path: keys, oldValue: old, newValue: value })
      }
      else {
        this._emitter.emit('configChanged', { path: keys, oldValue: old, newValue: value })
      }
    }

    this._emitter.emit('changed')
  }

  private _onConfigChanged(payload: { path: string[], oldValue: any, newValue: any }) {
    const path = ['configs', ...payload.path]
    const hubKey = path.length >= 3 ? path.slice(-3).join('.') : path.slice(-2).join('.')
    this._valueHub.set(hubKey, payload.newValue)
  }
}

export class ProjectGen {
  private _origin: ProjectGenType
  private _linker?: ProjectGenLinker

  constructor(origin: ProjectGenType) {
    this._origin = origin
  }

  get origin(): ProjectGenType {
    return this._origin
  }

  get copyLibrary(): boolean {
    return this._origin.copyLibrary ?? false
  }

  get useToolchainsPackage(): boolean {
    return this._origin.useToolchainsPackage ?? false
  }

  get hal(): string {
    return this._origin.hal
  }

  get halVersion(): string {
    return this._origin.halVersion ?? 'latest'
  }

  get builder(): string {
    return this._origin.builder
  }

  get builderVersion(): string {
    return this._origin.builderVersion ?? 'latest'
  }

  get toolchains(): string {
    return this._origin.toolchains
  }

  get toolchainsVersion(): string {
    return this._origin.toolchainsVersion ?? 'latest'
  }

  get linker(): ProjectGenLinker | null {
    if (this._origin.linker) {
      return this._linker ??= new ProjectGenLinker(this._origin.linker)
    }
    return null
  }
}

export class ProjectGenLinker {
  private _origin: ProjectGenLinkerType

  constructor(origin: ProjectGenLinkerType) {
    this._origin = origin
  }

  get origin(): ProjectGenLinkerType {
    return this._origin
  }

  get defaultHeapSize(): number | null {
    return this._origin.defaultHeapSize ?? null
  }

  get defaultStackSize(): number | null {
    return this._origin.defaultStackSize ?? null
  }
}

// #endregion

export class ProjectManager {
  private _project: Project | null = null
  private _valueHub: ValueHub
  private _ipManager: IpManager

  constructor(valueHub: ValueHub, ipManager: IpManager) {
    this._valueHub = valueHub
    this._ipManager = ipManager
  }

  async init() {
    const path = await window.electron.invoke('database:getProjectPath') as string
    if (path) {
      const content = await window.electron.invoke('database:getProject') as ProjectType | null
      if (content) {
        const project = new Project(content, path, this._valueHub, this._ipManager)
        const values = structuredClone(project.origin)
        this._valueHub.assign(values)
        document.title = project.name
        this._project = project
      }
    }
  }

  get(): Project | null {
    return this._project
  }
}

export async function createProjectManagerPlugin(
  valueHub: ValueHub,
  summaryManager: SummaryManager,
  clockTreeManager: ClockTreeManager,
  ipManager: IpManager,
) {
  const manager = new ProjectManager(valueHub, ipManager)
  await manager.init()
  const project = manager.get()
  if (project) {
    await summaryManager.load(project.vendor, project.targetChip)
    const summary = summaryManager.get(project.vendor, project.targetChip)
    if (summary) {
      await clockTreeManager.load(project.vendor, summary.clockTree.svg)
    }
    else {
      console.error(`No summary found for vendor: ${project.vendor}, targetChip: ${project.targetChip}`)
    }
  }

  return {
    value: manager,
    plugin: {
      install(app: App) {
        app.provide('database:projectManager', manager)
      },
    },
  }
}

export function useProjectManager(): ProjectManager {
  return inject('database:projectManager')!
}
