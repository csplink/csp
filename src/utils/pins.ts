/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        pins.ts
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
 *  2025-09-11     xqyjlj       initial version
 */

import type { App, ComputedRef, ShallowReactive } from 'vue'
import type { Project, ProjectConfigsPinUnitType, ProjectManager } from './project'
import type { Ip, IpManager, IpParameter, IpRefParameter, SummaryManager, SummaryPin } from '~/database'
import { computed, inject, markRaw, shallowReactive } from 'vue'
import { IpObject } from '~/database'

export class Pin {
  private _parameters: Record<string, ComputedRef<IpParameter>>
  private _project: Project
  private _presets?: Record<string, IpObject>
  private _path: string
  private _ipPath: string
  private _functionPath: string
  private _modePath: string
  private _labelPath: string
  private _lockedPath: string
  private _item: ShallowReactive<ProjectConfigsPinUnitType>

  constructor(
    private _name: string,
    private _summaryPin: SummaryPin,
    private _ip: Ip,
  ) {
    this._project = _ip.project()

    this._path = `pins.${this._name}`
    this._ipPath = `${this._ip.instance}.${this._name}`
    this._functionPath = `${this._path}.function`
    this._modePath = `${this._path}.mode`
    this._labelPath = `${this._path}.label`
    this._lockedPath = `${this._path}.locked`

    this._parameters = _ip.buildParameters(this._name)

    this._item = shallowReactive<ProjectConfigsPinUnitType>({
      function: this._project.configs.get(this._functionPath, ''),
      mode: this._project.configs.get(this._modePath, ''),
      label: this._project.configs.get(this._labelPath, ''),
      locked: this._project.configs.get(this._lockedPath, false),
    })

    this._project.configs.emitter.on('changed', this._onProjectConfigsChanged.bind(this))
  }

  get name(): string {
    return this._name
  }

  function = computed((): string => this._item.function!)

  mode = computed((): string => this._item.mode!)

  label = computed({
    get: (): string => this._item.label!,
    set: (value: string | null) => {
      this._project.configs.set(this._labelPath, value)
    },
  })

  locked = computed({
    get: (): boolean => this._item.locked!,
    set: (value: boolean) => {
      this._project.configs.set(this._lockedPath, value)
    },
  })

  state = computed((): string => {
    const key = this.mode.value || this.function.value
    if (key && key.includes(':')) {
      return key.split(':')[1]
    }
    return 'unknown'
  })

  get parameters(): Record<string, ComputedRef<IpParameter>> {
    return this._parameters
  }

  get presets(): Record<string, IpObject> {
    if (!this._presets) {
      this._presets = {}
      for (const [presetName, presetValue] of Object.entries(this._ip.origin.presets ?? {})) {
        this._presets[presetName] = new IpObject(presetValue, this._parameters, this._ip)
      }
    }
    return this._presets
  }

  refParameters = computed((): Record<string, IpRefParameter> => {
    return this.presets[this.state.value]?.refParameters.value ?? {}
  })

  get position(): number {
    return this._summaryPin.position
  }

  get type(): string {
    return this._summaryPin.type
  }

  get signals(): string[] {
    return this._summaryPin.signals
  }

  get modes(): string[] {
    return this._summaryPin.modes
  }

  get functions(): string[] {
    return this._summaryPin.functions()
  }

  reset() {
    this._project.configs.set<Record<string, any>>(this._ipPath, {})
    this._project.configs.set<ProjectConfigsPinUnitType>(this._path, {})
  }

  setFunction(func: string, mode: string = '') {
    const seqs = func.split(':')
    const instance = seqs[0]
    const state = seqs[1]
    let locked = false
    if (instance === this._ip.instance && this.modes.includes(func)) {
      locked = true
      const presets = this.presets[state] ?? {}
      const models: Record<string, any> = {}
      for (const [key, refParameter] of Object.entries(presets.refParameters.value)) {
        models[key] = refParameter.default.value
      }
      this._project.configs.set<Record<string, any>>(this._ipPath, models)
    }

    this._project.configs.set<ProjectConfigsPinUnitType>(this._path, {
      locked,
      function: func,
      mode,
      label: this.label.value,
    })
  }

  unsetFunction() {
    this._project.configs.set<Record<string, any>>(this._ipPath, {})
    this._project.configs.set<ProjectConfigsPinUnitType>(this._path, {
      locked: false,
      function: '',
      mode: '',
      label: this.label.value,
    })
  }

  private _onProjectConfigsChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const path = payload.path.join('.')

    if (path === this._functionPath) {
      this._item.function = payload.newValue
    }
    else if (path === this._modePath) {
      this._item.mode = payload.newValue
    }
    else if (path === this._labelPath) {
      this._item.label = payload.newValue
    }
    else if (path === this._lockedPath) {
      this._item.locked = payload.newValue
    }
    else if (path === this._path) {
      const value: ProjectConfigsPinUnitType = payload.newValue ?? {}
      this._item.function = value.function ?? ''
      this._item.mode = value.mode ?? ''
      this._item.label = value.label ?? ''
      this._item.locked = value.locked ?? false
    }
  }
}

export class PinsManager {
  private _pins: Record<string, Pin> = markRaw({})

  constructor() {
  }

  get pins(): Record<string, Pin> {
    return this._pins
  }
}

export function createPinsManagerPlugin() {
  const manager = new PinsManager()

  function init(projectManager: ProjectManager, summaryManager: SummaryManager, ipManager: IpManager) {
    const project = projectManager.get()
    if (project) {
      const summary = summaryManager.get(project.vendor, project.targetChip)
      if (summary) {
        const ip = ipManager.getPeripheral(project.vendor, summary.pinInstance)
        if (ip) {
          for (const [name, summaryPin] of Object.entries(summary.pins)) {
            manager.pins[name] = markRaw(new Pin(name, summaryPin, ip))
          }
        }
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
        app.provide('utils@pinsManager', manager)
      },
    },
    init,
  }
}

export function usePinsManager(): PinsManager {
  return inject('utils@pinsManager')!
}
