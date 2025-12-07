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
} from '@/electron/types'
import type { Emitter } from 'mitt'
import type { App, Reactive } from 'vue'
import type { PackageIndex, PackageManager } from './packages'
import type { Summary, SummaryManager } from '~/database'
import type { UseI18nType, VueI18nType } from '~/i18n'
import mitt from 'mitt'
import semver from 'semver'
import { computed, inject, markRaw, reactive, shallowReactive, shallowRef, watchEffect } from 'vue'
import pkg from '~/../package.json'
import { Express } from './express'
import { showOpenDialog } from './io'

// #region typedef

// eslint-disable-next-line ts/consistent-type-definitions
export type ProjectEventType = {
  changed: { path: string[], newValue: any, oldValue: any }
  modulesChanged: { newValue: string[], oldValue: string[] }
}

export class Project {
  private _configs: ProjectConfigs
  private _gen: ProjectGen
  private _emitter = mitt<ProjectEventType>()
  private _dirty = false
  private _snapshot: string = '' /*! < 数据快照，使用 JSON 字符串 */
  private _checkDirtyTimer: number | null = null /*! < 防抖计时器 */
  modules: Reactive<Set<string>>

  constructor(
    private _origin: ProjectType,
    private _path: string,
  ) {
    this.modules = reactive(new Set(this._modules))

    this._configs = new ProjectConfigs(this._origin.configs ??= {})
    this._configs.emitter.on('changed', this.onConfigsChanged.bind(this))

    this._gen = new ProjectGen(this._origin.gen ??= {})
    this._gen.emitter.on('changed', this.onGenChanged.bind(this))

    watchEffect(() => {
      this._modules = [...this.modules].sort()
    })

    this._emitter.on('changed', this.onChanged.bind(this))

    /*! < pkg.version >= this.version */
    if (semver.gte(pkg.version, this.version)) {
      /*! < TODO: */
    }

    this.version = pkg.version

    /*! < 如果发生了修改，立马保存一次 */
    if (this._dirty) {
      this.save()
    }

    /*! < 创建初始快照 */
    this._updateSnapshot()
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

  private set version(value: string) {
    const oldValue = this._origin.version ?? []
    this._origin.version = value
    if (oldValue === value)
      return
    this._emitter.emit('changed', { path: ['version'], newValue: value, oldValue })
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

  private get _modules(): string[] {
    return this._origin.modules ??= []
  }

  private set _modules(value: string[]) {
    const oldValue = this._origin.modules ?? []
    this._origin.modules = value
    if (oldValue === value)
      return
    this._emitter.emit('changed', { path: ['modules'], newValue: value, oldValue })
  }

  get configs(): ProjectConfigs {
    return this._configs
  }

  get gen(): ProjectGen {
    return this._gen
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

  async save() {
    this._setDirty(false)
    await saveProject(this.origin)
    /*! < 保存后更新快照 */
    this._updateSnapshot()
  }

  path(): string {
    return this._path
  }

  /**
   * 创建当前数据的快照
   */
  private _updateSnapshot() {
    try {
      this._snapshot = JSON.stringify(this._origin)
    }
    catch (error) {
      console.error('Failed to create snapshot:', error)
    }
  }

  /**
   * 比对当前数据和快照是否相同
   * @returns true 表示数据已变化，false 表示数据未变化
   */
  private _compareWithSnapshot(): boolean {
    try {
      const current = JSON.stringify(this._origin)
      return current !== this._snapshot
    }
    catch (error) {
      console.error('Failed to compare with snapshot:', error)
      return true /*! < 出错时保守处理，认为已变化 */
    }
  }

  /**
   * 检查并更新脏状态（延迟执行）
   */
  private _checkDirtyState() {
    const hasChanged = this._compareWithSnapshot()
    this._setDirty(hasChanged)
  }

  private onChanged(_payload: { path: string[], newValue: any, oldValue: any }) {
    /*! < 清除之前的计时器 */
    if (this._checkDirtyTimer !== null) {
      clearTimeout(this._checkDirtyTimer)
    }

    /*! < 设置新的防抖计时器，500ms 后检查脏状态 */
    this._checkDirtyTimer = setTimeout(() => {
      this._checkDirtyState()
      this._checkDirtyTimer = null
    }, 500) as unknown as number
  }

  private onConfigsChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    this._emitter.emit('changed', { path: ['configs', ...payload.path], newValue: payload.newValue, oldValue: payload.oldValue })
  }

  private onGenChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    this._emitter.emit('changed', { path: ['gen', ...payload.path], newValue: payload.newValue, oldValue: payload.oldValue })
  }
}

// eslint-disable-next-line ts/consistent-type-definitions
export type ProjectConfigsEventType = {
  changed: { path: string[], newValue: any, oldValue: any }
  pinConfigChanged: { path: string[], newValue: any, oldValue: any }
  configChanged: { path: string[], newValue: any, oldValue: any }
}

export interface ProjectConfigsPinUnitType {
  label?: string
  function?: string
  mode?: string
  locked?: boolean
}

export class ProjectConfigs {
  private _emitter = mitt<ProjectConfigsEventType>()
  private _pathCache = new Map<string, string[]>()

  constructor(
    private _origin: Record<string, any>,
  ) {
  }

  get origin(): Record<string, any> {
    return this._origin
  }

  get emitter(): Emitter<ProjectConfigsEventType> {
    return this._emitter
  }

  get<T = any>(path: string, defaultValue: T = null as any): T {
    const keys = this._getPathKeys(path)
    let item: any = this._origin

    for (const key of keys) {
      if (!(key in item)) {
        return defaultValue
      }
      item = item[key]
    }

    return item as T
  }

  set<T = any>(path: string, value: T): void {
    const keys = this._getPathKeys(path)
    let item: any = this._origin

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

    if (Express.isEmpty(value)) {
      delete item[lastKey]
    }

    this._emitter.emit('changed', { path: keys, newValue: value, oldValue: old })
  }

  private _getPathKeys(path: string): string[] {
    if (!this._pathCache.has(path)) {
      this._pathCache.set(path, path.split('.'))
    }
    return this._pathCache.get(path)!
  }
}

// eslint-disable-next-line ts/consistent-type-definitions
export type ProjectGenEventType = {
  changed: { path: string[], newValue: any, oldValue: any }
  copyLibraryChanged: { newValue: boolean, oldValue: boolean }
  halChanged: { newValue: string, oldValue: string }
  halVersionChanged: { newValue: string, oldValue: string }
  builderChanged: { newValue: string, oldValue: string }
  builderVersionChanged: { newValue: string, oldValue: string }
  useToolchainsPackageChanged: { newValue: boolean, oldValue: boolean }
  toolchainChanged: { newValue: string, oldValue: string }
  toolchainsVersionChanged: { newValue: string, oldValue: string }
}

export class ProjectGen {
  private _linker: ProjectGenLinker
  private _emitter = mitt<ProjectGenEventType>()
  private _state
  builders: string[] = shallowReactive([])
  builderVersions: string[] = shallowReactive([])
  toolchainsList: string[] = shallowReactive([])
  toolchainsVersions: string[] = shallowReactive([])
  toolchainsPath = shallowRef<string>()
  hals: string[] = shallowReactive([])
  halVersions: string[] = shallowReactive([])
  halPath = shallowRef<string>()

  constructor(
    private _origin: ProjectGenType,
  ) {
    this._state = reactive(this._origin)
    this._linker = new ProjectGenLinker(this._state.linker ??= {})
    this._linker.emitter.on('changed', this.onLinkerChanged.bind(this))
  }

  get origin(): ProjectGenType {
    return this._origin
  }

  get emitter(): Emitter<ProjectGenEventType> {
    return this._emitter
  }

  copyLibrary = computed({
    get: () => this._state.copyLibrary ?? false,
    set: (value: boolean) => {
      const oldValue = this._state.copyLibrary ?? false
      this._state.copyLibrary = value
      if (oldValue === value)
        return
      this._emitter.emit('copyLibraryChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['copyLibrary'], newValue: value, oldValue })
    },
  })

  useToolchainsPackage = computed({
    get: () => this._state.useToolchainsPackage ?? false,
    set: (value: boolean) => {
      const oldValue = this._state.useToolchainsPackage ?? false
      this._state.useToolchainsPackage = value
      if (oldValue === value)
        return
      this._emitter.emit('useToolchainsPackageChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['useToolchainsPackage'], newValue: value, oldValue })
    },
  })

  hal = computed({
    get: () => this._state.hal ?? '',
    set: (value: string) => {
      const oldValue = this._state.hal ?? ''
      this._state.hal = value
      if (oldValue === value)
        return
      this._emitter.emit('halChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['hal'], newValue: value, oldValue })
    },
  })

  halVersion = computed({
    get: () => this._state.halVersion ?? 'latest',
    set: (value: string) => {
      const oldValue = this._state.halVersion ?? 'latest'
      this._state.halVersion = value
      if (oldValue === value)
        return
      this._emitter.emit('halVersionChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['halVersion'], newValue: value, oldValue })
    },
  })

  builder = computed({
    get: () => this._state.builder ?? '',
    set: (value: string) => {
      const oldValue = this._state.builder ?? ''
      this._state.builder = value
      if (oldValue === value)
        return
      this._emitter.emit('builderChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['builder'], newValue: value, oldValue })
    },
  })

  builderVersion = computed({
    get: () => this._state.builderVersion ?? 'latest',
    set: (value: string) => {
      const oldValue = this._state.builderVersion ?? 'latest'
      this._state.builderVersion = value
      if (oldValue === value)
        return
      this._emitter.emit('builderVersionChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['builderVersion'], newValue: value, oldValue })
    },
  })

  toolchains = computed({
    get: () => this._state.toolchains ?? '',
    set: (value: string) => {
      const oldValue = this._state.toolchains ?? ''
      this._state.toolchains = value
      if (oldValue === value)
        return
      this._emitter.emit('toolchainChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['toolchains'], newValue: value, oldValue })
    },
  })

  toolchainsVersion = computed({
    get: () => this._state.toolchainsVersion ?? 'latest',
    set: (value: string) => {
      const oldValue = this._state.toolchainsVersion ?? 'latest'
      this._state.toolchainsVersion = value
      if (oldValue === value)
        return
      this._emitter.emit('toolchainsVersionChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['toolchainsVersion'], newValue: value, oldValue })
    },
  })

  get linker(): ProjectGenLinker {
    return this._linker
  }

  private onLinkerChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    this._emitter.emit('changed', { path: ['linker', ...payload.path], newValue: payload.newValue, oldValue: payload.oldValue })
  }
}

// eslint-disable-next-line ts/consistent-type-definitions
export type ProjectGenLinkerEventType = {
  changed: { path: string[], newValue: any, oldValue: any }
  heapSizeChanged: { newValue: number, oldValue: number }
  stackSizeChanged: { newValue: number, oldValue: number }
}

export class ProjectGenLinker {
  private _emitter = mitt<ProjectGenLinkerEventType>()
  private _state

  constructor(
    private _origin: ProjectGenLinkerType,
  ) {
    this._state = reactive(this._origin)
  }

  get origin(): ProjectGenLinkerType {
    return this._origin
  }

  get emitter(): Emitter<ProjectGenLinkerEventType> {
    return this._emitter
  }

  heapSize = computed({
    get: () => this._state.heapSize ?? -1,
    set: (value: number) => {
      const oldValue = this._state.heapSize ?? -1
      this._state.heapSize = value
      if (oldValue === value)
        return
      this._emitter.emit('heapSizeChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['heapSize'], newValue: value, oldValue })
    },
  })

  stackSize = computed({
    get: () => this._state.stackSize ?? -1,
    set: (value: number) => {
      const oldValue = this._state.stackSize ?? -1
      this._state.stackSize = value
      if (oldValue === value)
        return
      this._emitter.emit('stackSizeChanged', { newValue: value, oldValue })
      this._emitter.emit('changed', { path: ['stackSize'], newValue: value, oldValue })
    },
  })
}

// #endregion

export class ProjectManager {
  private _project: Project | null = null

  constructor() {
  }

  async init() {
    const path = await getProjectPath()
    if (path) {
      const content = await getProject()
      if (content) {
        const project = new Project(content, path)
        document.title = project.name
        this._project = markRaw(project)
      }
    }
  }

  get(): Project | null {
    return this._project
  }

  binding(summary: Summary, packageIndex: PackageIndex): void {
    if (this._project === null) {
      return
    }

    this.updateLinkerHeapSize(this._project!, summary)
    this.updateLinkerStackSize(this._project!, summary)
    this.updateBuilder(this._project!, summary)
    this.updateHal(this._project!, summary)

    watchEffect(() => {
      this.updateBuilderVersion(this._project!, summary)
    })

    watchEffect(() => {
      this.updateToolchains(this._project!, summary)
    })

    watchEffect(() => {
      this.updateToolchainsVersion(this._project!, packageIndex)
    })

    watchEffect(() => {
      this.updateToolchainsPath(this._project!, packageIndex)
    })

    watchEffect(() => {
      this.updateHalVersion(this._project!, packageIndex)
    })

    watchEffect(() => {
      this.updateHalPath(this._project!, packageIndex)
    })
  }

  private updateLinkerHeapSize(project: Project, summary: Summary) {
    if (summary.linker) {
      let heapSize = -1

      if (project.gen.linker.heapSize.value > 0) {
        heapSize = project.gen.linker.heapSize.value
      }
      else if (summary.linker.defaultHeapSize > 0) {
        heapSize = summary.linker.defaultHeapSize
      }

      project.gen.linker.heapSize.value = heapSize
    }
  }

  private updateLinkerStackSize(project: Project, summary: Summary) {
    if (summary.linker) {
      let stackSize = -1
      if (project.gen.linker.stackSize.value > 0) {
        stackSize = project.gen.linker.stackSize.value
      }
      else if (summary.linker.defaultStackSize > 0) {
        stackSize = summary.linker.defaultStackSize
      }

      project.gen.linker.stackSize.value = stackSize
    }
  }

  private updateBuilder(project: Project, summary: Summary) {
    const options = []

    for (const [builder, _] of Object.entries(summary.builders)) {
      options.push(builder)
    }

    project.gen.builders.length = 0
    project.gen.builders.push(...options)

    let builder = ''
    if (project.gen.builder) {
      builder = project.gen.builder.value

      if (!options.includes(builder)) {
        console.warn(`构建工具 ${builder} 未找到，使用默认构建工具 ${options[0]}`)
        builder = options[0]
      }
    }
    else {
      builder = options[0]
    }

    project.gen.builder.value = builder
  }

  private updateBuilderVersion(project: Project, summary: Summary) {
    const options = []

    for (const version in summary.builders[project.gen.builder.value]) {
      options.push(version)
    }

    project.gen.builderVersions.length = 0
    project.gen.builderVersions.push(...options)

    let version = ''
    if (project.gen.builderVersion.value) {
      version = project.gen.builderVersion.value

      if (!options.includes(version)) {
        version = options[0]
      }
    }
    else {
      version = options[0]
    }

    project.gen.builderVersion.value = version
  }

  private updateToolchains(project: Project, summary: Summary) {
    const options = []

    for (const toolchains of summary.builders[project.gen.builder.value][project.gen.builderVersion.value]) {
      options.push(toolchains)
    }

    project.gen.toolchainsList.length = 0
    project.gen.toolchainsList.push(...options)

    let toolchains = ''
    if (project.gen.toolchains) {
      toolchains = project.gen.toolchains.value

      if (!options.includes(toolchains)) {
        toolchains = options[0]
      }
    }
    else {
      toolchains = options[0]
    }

    project.gen.toolchains.value = toolchains
  }

  private updateToolchainsVersion(project: Project, packageIndex: PackageIndex) {
    const options = []

    const toolchainsPackages = packageIndex.origin.value.toolchains?.[project.gen.toolchains.value] ?? {}

    if (!project.gen.useToolchainsPackage.value) {
      project.gen.toolchainsVersion.value = ''
      return
    }

    for (const version in toolchainsPackages) {
      options.push(version)
    }

    project.gen.toolchainsVersions.length = 0
    project.gen.toolchainsVersions.push(...options)

    let version = ''
    if (project.gen.toolchainsVersion.value) {
      version = project.gen.toolchainsVersion.value

      if (!options.includes(version)) {
        version = options[0]
      }
    }
    else {
      version = options[0]
    }

    project.gen.toolchainsVersion.value = version
  }

  private updateToolchainsPath(project: Project, packageIndex: PackageIndex) {
    project.gen.toolchainsPath.value = packageIndex.path('toolchains', project.gen.toolchains.value, project.gen.toolchainsVersion.value)
  }

  private updateHal(project: Project, summary: Summary) {
    const options = [...summary.hals]

    project.gen.hals.length = 0
    project.gen.hals.push(...options)

    let hal = ''
    if (project.gen.hal) {
      hal = project.gen.hal.value

      if (!options.includes(hal)) {
        hal = options[0]
      }
    }
    else {
      hal = options[0]
    }

    project.gen.hal.value = hal
  }

  private updateHalVersion(project: Project, packageIndex: PackageIndex) {
    const options = []
    const halPackages = packageIndex.origin.value.hal?.[project.gen.hal.value] ?? {}
    for (const version in halPackages) {
      options.push(version)
    }

    project.gen.halVersions.length = 0
    project.gen.halVersions.push(...options)

    let version = ''
    if (project.gen.halVersion) {
      version = project.gen.halVersion.value

      if (!options.includes(version)) {
        version = options[0]
      }
    }
    else {
      version = options[0]
    }

    project.gen.halVersion.value = version
  }

  private updateHalPath(project: Project, packageIndex: PackageIndex) {
    project.gen.halPath.value = packageIndex.path('hal', project.gen.hal.value, project.gen.halVersion.value)
  }
}

export function createProjectManagerPlugin(i18n: VueI18nType) {
  const manager = new ProjectManager()

  async function init(summaryManager: SummaryManager, packageManager: PackageManager) {
    const project = manager.get()
    if (project) {
      await summaryManager.load(project.vendor, project.targetChip, i18n.global.locale)
      const summary = summaryManager.get(project.vendor, project.targetChip)
      if (summary) {
        manager.binding(summary, packageManager.packageIndex)
      }
      else {
        console.error(`No summary found for vendor: ${project.vendor}, targetChip: ${project.targetChip}`)
      }
    }
  }

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('utils@projectManager', manager)
      },
    },
    async load() {
      await manager.init()
    },
    init,
    project(): Project | null {
      return manager.get()
    },
  }
}

export function useProjectManager(): ProjectManager {
  return inject('utils@projectManager')!
}

async function saveProject(project: ProjectType) {
  await window.electron.invoke('project:save', project)
}

async function getProject(): Promise<ProjectType | null> {
  return await window.electron.invoke('project:get')
}

async function getProjectPath(): Promise<string> {
  return await window.electron.invoke('project:getPath')
}

export function setProjectPath(path: string) {
  window.electron.send('project:setPath', path)
}

export async function openProject(i18n: UseI18nType) {
  const { t } = i18n
  const { filePaths, canceled } = await showOpenDialog(
    {
      title: t('message.openCspProject'),
      filters: [
        { name: t('fileType.csp'), extensions: ['csp'] },
      ],
    },
  )

  if (canceled || !filePaths) {
    return { success: false }
  }

  if (filePaths.length !== 1) {
    return { success: false }
  }

  const projectPath = filePaths[0]
  setProjectPath(projectPath)
}

export function createProject(path: string, project: ProjectType) {
  window.electron.send('project:create', path, project)
}

export async function saveAsProject(path: string, name: string, project: ProjectType) {
  const copy = { ...project }
  copy.name = name
  await window.electron.invoke('project:saveAs', path, copy)
}
