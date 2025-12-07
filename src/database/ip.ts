/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ip.ts
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
 *  2025-05-20     xqyjlj       initial version
 */

import type {
  IpContainersType,
  IpDiagramsObjectConditionType,
  IpDiagramsObjectType,
  IpObjectConditionType,
  IpObjectType,
  IpParameterType,
  IpParameterValueUnitSignalUnitType,
  IpParameterValueUnitType,
  IpRefParameterType,
  IpType,
} from '@/electron/types'
import type { App, ComputedRef, ShallowRef, WritableComputedRef } from 'vue'
import type { Summary } from './summary'
import type { VueI18nType } from '~/i18n'
import type { Project, ProjectConfigsPinUnitType } from '~/utils'
import { computed, inject, markRaw, shallowRef, watch, watchEffect } from 'vue'
import { I18n } from '~/i18n'
import { Express } from '~/utils'

// #region typedef

export class Ip {
  private _parameters: Record<string, ComputedRef<IpParameter>>
  private _containers: IpContainers
  private _presets: Record<string, IpObject>
  private _activatedDependencies: string[] = []
  private _express = new Express()
  private _diagrams: IpDiagramsObject
  private _ip_prefixed: string = ''
  private _ip_suffix: string = ''

  activated: ShallowRef<boolean>

  constructor(
    private _instance: string,
    private _origin: IpType,
    private _project: Project,
    public locale: WritableComputedRef<string>,
    public summary: Summary,
  ) {
    this.activated = shallowRef(this.buildActivated())
    this._parameters = this.buildParameters()
    this._containers = new IpContainers(this._origin.containers ?? {}, this._parameters, this)
    this._presets = this.buildPresets()
    this._diagrams = new IpDiagramsObject(this._origin.diagrams, this)

    if (_instance.startsWith(this.name)) {
      this._ip_prefixed = _instance.replace(new RegExp(`^${this.name}`), '')
    }

    if (_instance.endsWith(this.name)) {
      this._ip_suffix = _instance.replace(new RegExp(`${this.name}$`), '')
    }

    watchEffect(() => {
      if (this.activated.value) {
        this._project.modules.add(this._instance)
      }
      else {
        this._project.modules.delete(this._instance)
      }
    })
  }

  get origin(): IpType {
    return this._origin
  }

  get name(): string {
    return this._origin.name
  }

  get parameters(): Record<string, ComputedRef<IpParameter>> {
    return this._parameters
  }

  get containers(): IpContainers {
    return this._containers
  }

  get presets(): Record<string, IpObject> {
    return this._presets
  }

  //   get pins(): Record<string, Record<string, Record<string, IpPin>>> | null {
  //     if (this._origin.pins) {
  //       if (!this._pins) {
  //         this._pins = {}
  //         for (const [name, value] of Object.entries(this._origin.pins)) {
  //           this._pins[name] = {}
  //           for (const [subName, subValue] of Object.entries(value)) {
  //             this._pins[name][subName] = {}
  //             for (const [pinName, pinValue] of Object.entries(subValue)) {
  //               this._pins[name][subName][pinName] = new IpPin(pinValue)
  //             }
  //           }
  //         }
  //       }
  //       return this._pins
  //     }
  //     return null
  //   }

  get instance(): string {
    return this._instance
  }

  get prefixed(): string {
    return this._ip_prefixed
  }

  get suffix(): string {
    return this._ip_suffix
  }

  get isPinIp(): boolean {
    return this._instance === this.summary.pinInstance
  }

  get diagrams(): IpDiagramsObject {
    return this._diagrams
  }

  signals = computed((): string[] => {
    const signals = new Set<string>()
    for (const [_name, parameter] of Object.entries(this.parameters)) {
      if (parameter.value.type === 'enum') {
        const parameterEnum = parameter.value as IpParameterEnum
        for (const signal of parameterEnum.allSignals) {
          signals.add(signal)
        }
      }
    }
    const rtn = Array.from(signals)
    rtn.sort()
    return rtn
  })

  getExpression(expr: string) {
    /**
     * ${IP_INSTANCE}: 当前 IP 实例名称
     * ${IP_PREFIXED}: 当前 IP 实例前缀，例如 SIP vs QSPI = Q
     * ${IP_SUFFIXED}: 当前 IP 实例后缀，例如 SIP vs SPI1 = 1
     */
    expr = expr.replace(/\$\{IP_INSTANCE\}/g, this._instance)
    expr = expr.replace(/\$\{IP_PREFIXED\}/g, this._ip_prefixed)
    expr = expr.replace(/\$\{IP_SUFFIXED\}/g, this._ip_suffix)
    return expr
  }

  project(): Project {
    return this._project
  }

  express(): Express {
    return this._express
  }

  buildParameters(channel: string = ''): Record<string, ComputedRef<IpParameter>> {
    const rtn: Record<string, ComputedRef<IpParameter>> = {}
    for (const [name, value] of Object.entries(this._origin.parameters)) {
      if (Array.isArray(value)) {
        const condition = new IpCondition<IpParameterType>(name, value, this)
        const parameters: IpParameter[] = []

        for (const obj of value) {
          parameters.push(this._createParameter(obj.content, name, channel))
        }

        rtn[name] = computed((): IpParameter => parameters[condition.index.value])
      }
      else {
        const parameter = this._createParameter(value, name, channel)
        rtn[name] = computed((): IpParameter => parameter)
      }
    }
    return rtn
  }

  private buildActivated(): boolean {
    if (this._origin.activated !== undefined) {
      const condition = this.getExpression(this._origin.activated)
      const result = this._express.evaluateExpression<boolean>(condition, this.project().origin, false) ?? false

      const set = new Set<string>()
      this._express.evaluateExtract(condition).forEach((item) => {
        set.add(item)
      })
      this._activatedDependencies = Array.from(set)
      this.project().emitter.on('changed', this._onProjectConfigChanged.bind(this))

      return result
    }
    else {
      return true
    }
  }

  private _createParameter(parameter: IpParameterType, name: string, channel: string = ''): IpParameter {
    if (parameter.type === 'enum') {
      return new IpParameterEnum(parameter, name, channel, this)
    }
    else if (parameter.type === 'float') {
      return new IpParameterNumber(parameter, name, channel, this)
    }
    else if (parameter.type === 'integer') {
      return new IpParameterNumber(parameter, name, channel, this)
    }
    else if (parameter.type === 'boolean') {
      return new IpParameterBoolean(parameter, name, channel, this)
    }
    else {
      return new IpParameterString(parameter, name, channel, this)
    }
  }

  private buildPresets(): Record<string, IpObject> {
    const presets: Record<string, IpObject> = {}
    for (const [presetName, presetValue] of Object.entries(this._origin.presets ?? {})) {
      presets[presetName] = new IpObject(presetValue, this._parameters, this)
    }
    return presets
  }

  private _onProjectConfigChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const changedPath = payload.path.join('.')
    if (this._activatedDependencies.some(dep => changedPath.startsWith(dep))) {
      const condition = this.getExpression(this._origin.activated ?? '')
      const value = this._express.evaluateExpression<boolean>(condition, this.project().origin, false) ?? false
      if (value !== this.activated.value) {
        this.activated.value = value
      }
    }
  }
}

// #region typedef IpParameter

export type IpParameter =
  IpParameterEnum |
  IpParameterNumber |
  IpParameterBoolean |
  IpParameterString

export class IpParameterBase {
  private _display: I18n
  private _description: I18n
  private _enableDependencies: string[] = []
  protected _path

  enabled: ShallowRef<boolean>

  constructor(
    protected _origin: IpParameterType,
    protected _name: string,
    protected _channel: string = '',
    protected _parent: Ip,
  ) {
    if (_channel) {
      this._path = `${this._parent.instance}.${this._channel}.${this._name}`
    }
    else {
      this._path = `${this._parent.instance}.${this._name}`
    }

    this._display = new I18n(this._origin.display ?? { en: '' })
    this._description = new I18n(this._origin.description ?? { en: '' })

    this.enabled = shallowRef(this.buildEnable())
  }

  get origin(): IpParameterType {
    return this._origin
  }

  display = computed((): string => this._display.get(this._parent.locale.value))

  description = computed((): string => this._description.get(this._parent.locale.value))

  get readonly(): boolean {
    return this._origin.readonly ?? false
  }

  get type(): 'string' | 'boolean' | 'enum' | 'integer' | 'float' {
    return this._origin.type
  }

  get visible(): boolean {
    return this._origin.visible ?? true
  }

  get name(): string {
    return this._name
  }

  get path(): string {
    return this._path
  }

  private buildEnable(): boolean {
    if (this._origin.enabled === undefined) {
      return true
    }
    else if (typeof this._origin.enabled === 'boolean') {
      return this._origin.enabled
    }
    else {
      const condition = this._origin.enabled
      const result = this._parent.express().evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false

      const set = new Set<string>()
      this._parent.express().evaluateExtract(condition).forEach((item) => {
        set.add(item)
      })
      this._enableDependencies = Array.from(set)
      this._parent.project().emitter.on('changed', this._onProjectConfigChanged.bind(this))

      return result
    }
  }

  private _onProjectConfigChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const changedPath = payload.path.join('.')
    if (this._enableDependencies.some(dep => changedPath.startsWith(dep))) {
      const condition = this._origin.enabled as string
      const value = this._parent.express().evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false
      if (value !== this.enabled.value) {
        this.enabled.value = value
      }
    }
  }
}

export class IpParameterValueUnitSignalUnit {
  constructor(
    private _origin: IpParameterValueUnitSignalUnitType,
  ) {
  }

  get mode(): string {
    return this._origin.mode
  }
}

export class IpParameterValueUnit {
  private _signals: Record<string, IpParameterValueUnitSignalUnit> | null
  private _comment: I18n
  private _enableDependencies: string[] = []

  enabled: ShallowRef<boolean>

  constructor(
    private _origin: IpParameterValueUnitType,
    private _parent: Ip,
  ) {
    this._comment = new I18n(this._origin.comment ?? { en: '' })
    this._signals = this.buildSignals()

    this.enabled = shallowRef(this.buildEnable())
  }

  comment = computed((): string => this._comment.get(this._parent.locale.value))

  get signals(): Record<string, IpParameterValueUnitSignalUnit> | null {
    return this._signals
  }

  private buildSignals(): Record<string, IpParameterValueUnitSignalUnit> | null {
    if (this._origin.signals) {
      const signals: Record<string, IpParameterValueUnitSignalUnit> = {}
      for (const [name, value] of Object.entries(this._origin.signals)) {
        const key = this._parent.getExpression(name)
        signals[key] = new IpParameterValueUnitSignalUnit(value)
      }
      return signals
    }
    return null
  }

  get pins(): string[] {
    const pins = [...this._parent.summary.findPinsBySignals(Object.keys(this.signals ?? {}))]
    return pins
  }

  valid = computed((): { isEnabled: boolean, reason: string } => {
    const { available, conflicts } = this.checkAvailability()

    if (!available) {
      const reasons = []

      for (const [key, value] of Object.entries(conflicts)) {
        reasons.push(`${key} -> ${value}`)
      }

      return {
        isEnabled: false,
        reason: `引脚冲突` + `:\r\n${reasons.join('\r\n')}`,
      }
    }

    return {
      isEnabled: true,
      reason: '',
    }
  })

  private checkAvailability(): { available: boolean, conflicts: Record<string, string> } {
    const conflicts: Record<string, string> = {}
    const pins = this._parent.project().configs.get<Record<string, ProjectConfigsPinUnitType>>('pins', {})

    for (const signalName of Object.keys(this.signals ?? {})) {
      const pinNames = this._parent.summary.findPinsBySignals([signalName])
      for (const pinName of pinNames) {
        const pinConfig = pins[pinName]
        if (pinConfig && pinConfig.locked === true && pinConfig.function !== signalName) {
          conflicts[pinName] = pinConfig.function ?? ''
        }
      }
    }

    return {
      available: Object.keys(conflicts).length === 0,
      conflicts,
    }
  }

  private buildEnable(): boolean {
    if (this._origin.enabled === undefined) {
      return true
    }
    else if (typeof this._origin.enabled === 'boolean') {
      return this._origin.enabled
    }
    else {
      const condition = this._origin.enabled
      const result = this._parent.express().evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false

      const set = new Set<string>()
      this._parent.express().evaluateExtract(condition).forEach((item) => {
        set.add(item)
      })
      this._enableDependencies = Array.from(set)
      this._parent.project().emitter.on('changed', this._onProjectConfigChanged.bind(this))

      return result
    }
  }

  private _onProjectConfigChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const changedPath = payload.path.join('.')
    if (this._enableDependencies.some(dep => changedPath.startsWith(dep))) {
      const condition = this._origin.enabled as string
      const value = this._parent.express().evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false
      if (value !== this.enabled.value) {
        this.enabled.value = value
      }
    }
  }
}

export class IpParameterEnum extends IpParameterBase {
  private _values: Record<string, IpParameterValueUnit>
  private _allSignals: string[]
  private _value: ShallowRef<string>

  constructor(origin: IpParameterType, name: string, channel: string = '', parent: Ip) {
    super(origin, name, channel, parent)
    this._values = this.buildValues()
    this._allSignals = this.buildAllSignals()
    this._value = shallowRef(this._parent.project().configs.get(this._path, this.default))
    this._parent.project().configs.emitter.on('changed', this._onProjectConfigsChanged.bind(this))
  }

  get default(): string {
    return this._origin.default as string
  }

  get values(): Record<string, IpParameterValueUnit> {
    return this._values
  }

  get allSignals(): string[] {
    return this._allSignals
  }

  private buildValues(): Record<string, IpParameterValueUnit> {
    const values: Record<string, IpParameterValueUnit> = {}
    for (const [name, value] of Object.entries(this._origin.values ?? {})) {
      values[name] = new IpParameterValueUnit(value, this._parent)
    }
    return values
  }

  private buildAllSignals(): string[] {
    const signals = new Set<string>()
    for (const [_name, value] of Object.entries(this._values)) {
      if (value.signals) {
        for (const signal of Object.keys(value.signals)) {
          signals.add(signal)
        }
      }
    }
    const allSignals = Array.from(signals)
    allSignals.sort()
    return allSignals
  }

  value = computed({
    get: (): string => this._value.value,
    set: (value: string | null) => {
      this._parent.project().configs.set(this._path, value ?? this.default)
    },
  })

  signals = computed(() => {
    return this.values[this.value.value]?.signals ?? null
  })

  private _onProjectConfigsChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const path = payload.path.join('.')
    if (path === this._path) {
      this._value.value = payload.newValue
    }
    else if (this._path.startsWith(path)) {
      this._value.value = this._parent.project().configs.get(this._path, this.default)
    }
  }
}

export class IpParameterNumber extends IpParameterBase {
  private _express
  private _dependencies: Record<string, string[]> = {}
  private _expressions: Record<string, string> = {}
  private _value: ShallowRef<number>

  max = shallowRef(Number.MAX_SAFE_INTEGER)
  min = shallowRef(Number.MIN_SAFE_INTEGER)

  constructor(origin: IpParameterType, name: string, channel: string = '', parent: Ip) {
    super(origin, name, channel, parent)

    this._express = parent.express()

    if (typeof origin.max === 'number') {
      this.max.value = origin.max
    }
    else if (typeof origin.max === 'string') {
      this.max.value = this.buildValue('max', Number.MAX_SAFE_INTEGER)
    }

    if (typeof origin.min === 'number') {
      this.min.value = origin.min
    }
    else if (typeof origin.min === 'string') {
      this.min.value = this.buildValue('min', Number.MIN_SAFE_INTEGER)
    }

    if (typeof origin.min === 'string' || typeof origin.max === 'string') {
      this._parent.project().emitter.on('changed', this._onProjectChanged.bind(this))
    }

    this._value = shallowRef(this._parent.project().configs.get(this._path, this.default))
    this._parent.project().configs.emitter.on('changed', this._onProjectConfigsChanged.bind(this))
  }

  get default(): number {
    return this._origin.default as number
  }

  value = computed({
    get: (): number => this._value.value,
    set: (value: number | null) => {
      this._parent.project().configs.set(this._path, value)
    },
  })

  private buildValue(prop: 'max' | 'min', defaultValue: number): number {
    const expression = this._parent.getExpression(this._origin[prop] as string)
    const value = this._express.evaluateExpression<number>(expression, this._parent.project().origin, defaultValue) ?? defaultValue
    const set = new Set<string>()
    this._express.evaluateExtract(expression).forEach((item) => {
      set.add(item)
    })
    this._dependencies[prop] = Array.from(set)
    this._expressions[prop] = expression
    return value
  }

  private buildValueFromHook(prop: 'max' | 'min', defaultValue: number): number {
    const expression = this._expressions[prop]
    const value = this._express.evaluateExpression<number>(expression, this._parent.project().origin, defaultValue) ?? defaultValue
    return value
  }

  private _onProjectChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const changedPath = payload.path.join('.')
    if (this._dependencies.max?.some(dep => changedPath.startsWith(dep))) {
      this.max.value = this.buildValueFromHook('max', Number.MAX_SAFE_INTEGER)
    }

    if (this._dependencies.min?.some(dep => changedPath.startsWith(dep))) {
      this.min.value = this.buildValueFromHook('min', Number.MIN_SAFE_INTEGER)
    }
  }

  getValue(value: number): number {
    if (value < this.min.value || value > this.max.value) {
      value = this.default /*! < 第一次选用默认值 */
    }

    if (value < this.min.value || value > this.max.value) {
      value = this.min.value /*! < 默认值也不满足要求，选择最小值 */
    }
    return value
  }

  private _onProjectConfigsChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const path = payload.path.join('.')
    if (path === this._path) {
      this._value.value = payload.newValue
    }
    else if (this._path.startsWith(path)) {
      this._value.value = this._parent.project().configs.get(this._path, this.default)
    }
  }
}

export class IpParameterBoolean extends IpParameterBase {
  private _value: ShallowRef<boolean>

  constructor(origin: IpParameterType, name: string, channel: string = '', parent: Ip) {
    super(origin, name, channel, parent)
    this._value = shallowRef(this._parent.project().configs.get(this._path, this.default))
    this._parent.project().configs.emitter.on('changed', this._onProjectConfigsChanged.bind(this))
  }

  get default(): boolean {
    return this._origin.default as boolean
  }

  value = computed({
    get: (): boolean => this._value.value,
    set: (value: boolean | null) => {
      this._parent.project().configs.set(this._path, value ?? this.default)
    },
  })

  private _onProjectConfigsChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const path = payload.path.join('.')
    if (path === this._path) {
      this._value.value = payload.newValue
    }
    else if (this._path.startsWith(path)) {
      this._value.value = this._parent.project().configs.get(this._path, this.default)
    }
  }
}

export class IpParameterString extends IpParameterBase {
  private _value: ShallowRef<string>

  constructor(origin: IpParameterType, name: string, channel: string = '', parent: Ip) {
    super(origin, name, channel, parent)
    this._value = shallowRef(this._parent.project().configs.get(this._path, this.default))
    this._parent.project().configs.emitter.on('changed', this._onProjectConfigsChanged.bind(this))
  }

  get default(): string {
    return this._origin.default as string
  }

  value = computed({
    get: (): string => this._value.value,
    set: (value: string | null) => {
      this._parent.project().configs.set(this._path, value ?? this.default)
    },
  })

  private _onProjectConfigsChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const path = payload.path.join('.')
    if (path === this._path) {
      this._value.value = payload.newValue
    }
    else if (this._path.startsWith(path)) {
      this._value.value = this._parent.project().configs.get(this._path, this.default)
    }
  }
}

export function isEnumParameter(parameter: IpParameter): parameter is IpParameterEnum {
  return parameter.type === 'enum'
}

export function isNumberParameter(parameter: IpParameter): parameter is IpParameterNumber {
  return parameter.type === 'integer' || parameter.type === 'float'
}

export function isBooleanParameter(parameter: IpParameter): parameter is IpParameterBoolean {
  return parameter.type === 'boolean'
}

export function isStringParameter(parameter: IpParameter): parameter is IpParameterString {
  return parameter.type === 'string'
}

// #endregion

export class IpObject {
  protected _condition?: IpCondition<IpObjectType>
  protected _refParametersCache: Record<string, IpRefParameter>[] = []

  constructor(
    private _origin: IpObjectType | IpObjectConditionType[],
    private _parameters: Record<string, ComputedRef<IpParameter>>,
    private _parent: Ip,
  ) {
    this.buildRefParameters()

    if (!this._parent.isPinIp) {
      /**
当 refParameters 变化时，恢复默认值
configurations:
  - condition: configs.${IP_INSTANCE}.usart_control_mode_t == 'asynchronous'
    content:
      refParameters:
        usart_virtual_mode_t:
          values:
            - asynchronous
          default: asynchronous
  - condition: configs.${IP_INSTANCE}.usart_control_mode_t == 'synchronous'
    content:
      refParameters:
        usart_virtual_mode_t:
          values:
            - synchronous
          default: synchronous
       */
      watch(
        () => this.refParameters.value,
        (refParameters: Record<string, IpRefParameter>) => {
          for (const [_name, ref] of Object.entries(refParameters)) {
            const parameter = ref.parameter.value
            if (isEnumParameter(parameter)) {
              if (!(parameter.value.value in ref.values.value)) {
                parameter.value.value = (ref.default.value as string)
              }
            }

            /* !< 防止为空 */
            if (parameter.value.value === ref.default.value) {
              parameter.value.value = ref.default.value
            }
          }
        },
        { immediate: true },
      )
    }
  }

  get origin(): IpObjectType | IpObjectConditionType[] {
    return this._origin
  }

  refParameters = computed((): Record<string, IpRefParameter> => {
    if (this._condition) {
      const index = this._condition.index.value
      if (index === -1) {
        return {}
      }
      return this._refParametersCache[index]
    }
    else {
      return this._refParametersCache[0]
    }
  })

  private buildRefParameters() {
    if (Array.isArray(this._origin)) {
      this._condition = new IpCondition<IpObjectType>('refParameters', this._origin, this._parent)

      for (const obj of this._origin) {
        const refs: Record<string, IpRefParameter> = {}
        for (const [name, value] of Object.entries(obj.content.refParameters ?? {})) {
          const parameter = this._parameters[name]
          refs[name] = new IpRefParameter(name, value, parameter, this._parent)
        }
        this._refParametersCache.push(refs)
      }
    }
    else {
      const refs: Record<string, IpRefParameter> = {}
      for (const [name, value] of Object.entries(this._origin.refParameters ?? {})) {
        const parameter = this._parameters[name]
        refs[name] = new IpRefParameter(name, value, parameter, this._parent)
      }
      this._refParametersCache.push(refs)
    }
  }
}

export class IpRefParameter {
  private _dependencies: string[] = []
  private _express: Express
  condition: ShallowRef<boolean>

  constructor(
    private _name: string,
    private _origin: IpRefParameterType,
    private _parameter: ComputedRef<IpParameter>,
    private _parent: Ip,
  ) {
    this._express = _parent.express()
    this.condition = shallowRef(this.buildCondition())

    /**
当 condition 变化时，恢复默认值
modes:
  refParameters:
    usart_control_mode_t: {}
    usart_control_hardware_flow_control_rs232_t:
      condition: configs.${IP_INSTANCE}.usart_control_mode_t == 'asynchronous'
     */
    watch(
      () => this.condition.value,
      (value: boolean) => {
        if (!value) {
          this.parameter.value.value.value = this.default.value
        }
      },
      { immediate: true },
    )

    /**
当 condition 变化时，恢复默认值
rcm_apb1_timers_mul_t:
  - condition: configs.RCM.rcm_apb1_div_t == '/1'
    content:
      ...
  - condition: default
    content:
      ...
     */
    watch(
      () => this.parameter.value,
      (p: IpParameter) => {
        if (isEnumParameter(p)) {
          if (!(p.value.value in this.values.value)) {
            p.value.value = (this.default.value as string)
          }
        }
      },
    )
  }

  get name(): string {
    return this._name
  }

  get origin(): IpRefParameterType {
    return this._origin
  }

  values = computed((): Record<string, IpParameterValueUnit> => {
    if (!isEnumParameter(this.parameter.value)) {
      return {}
    }
    const vs: Record<string, IpParameterValueUnit> = {}
    if (this._values.length === 0) {
      for (const [name, value] of Object.entries(this.parameter.value.values ?? {})) {
        vs[name] = value
      }
    }
    else {
      for (const name of this._values) {
        vs[name] = this.parameter.value.values[name]
      }
    }
    return vs
  })

  get _values(): string[] {
    return this.origin.values ?? []
  }

  default = computed((): string | number | boolean => {
    return this._origin.default ?? this.parameter.value.default
  })

  readonly = computed((): boolean => {
    return (this._origin.readonly ?? this.parameter.value.readonly ?? false) || !this.condition.value
  })

  parameter = computed((): IpParameter => this._parameter.value)

  private buildCondition(): boolean {
    if (this._origin.condition !== undefined) {
      const condition = this._parent.getExpression(this._origin.condition)
      const result = this._express.evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false

      const set = new Set<string>()
      this._express.evaluateExtract(condition).forEach((item) => {
        set.add(item)
      })
      this._dependencies = Array.from(set)
      this._parent.project().emitter.on('changed', this._onProjectConfigChanged.bind(this))

      return result
    }
    else {
      return true
    }
  }

  private _onProjectConfigChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const changedPath = payload.path.join('.')
    if (this._dependencies.some(dep => changedPath.startsWith(dep))) {
      const condition = this._parent.getExpression(this._origin.condition ?? '')
      const value = this._express.evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false
      if (value !== this.condition.value) {
        this.condition.value = value
      }
    }
  }
}

export class IpContainerObject extends IpObject {
}

export class IpContainers {
  private _overview: IpContainerObject
  private _modes: IpContainerObject
  private _configurations: IpContainerObject
  private _clockTree: IpContainerObject

  constructor(
    private _origin: IpContainersType,
    private _parameters: Record<string, ComputedRef<IpParameter>>,
    private _parent: Ip,
  ) {
    this._overview = new IpContainerObject(this._origin.overview ?? {}, this._parameters, this._parent)
    this._modes = new IpContainerObject(this._origin.modes ?? {}, this._parameters, this._parent)
    this._configurations = new IpContainerObject(this._origin.configurations ?? {}, this._parameters, this._parent)
    this._clockTree = new IpContainerObject(this._origin.clockTree ?? {}, this._parameters, this._parent)
  }

  get origin(): IpContainersType {
    return this._origin
  }

  get overview(): IpContainerObject {
    return this._overview
  }

  get modes(): IpContainerObject {
    return this._modes
  }

  get configurations(): IpContainerObject {
    return this._configurations
  }

  get clockTree(): IpContainerObject {
    return this._clockTree
  }
}

// TODO:
export class IpPin {
  constructor(
    private _origin: {
      default: boolean
    },
  ) {
  }

  get default(): boolean {
    return this._origin.default
  }
}

export class IpCondition<T> {
  private _dependencies: string[]

  private _express: Express
  private _map: Record<string, T> = {}
  private _key: ShallowRef<string>

  constructor(
    private _name: string,
    private _origin: { condition: string, content: T }[],
    private _parent: Ip,
  ) {
    this._express = _parent.express()

    const set = new Set<string>()
    let key = 'default'

    for (const item of this._origin) {
      const condition = this._parent.getExpression(item.condition)
      item.condition = condition
      this._map[condition] = item.content

      if (condition !== 'default') {
        this._express.evaluateExtract(condition).forEach((item) => {
          set.add(item)
        })

        if ((this._express.evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false) === true) {
          key = condition
        }
      }
    }

    this._key = shallowRef(key)
    this._dependencies = Array.from(set)

    this._parent.project().emitter.on('changed', this._onProjectConfigChanged.bind(this))
  }

  get name(): string {
    return this._name
  }

  get origin(): { condition: string, content: T }[] {
    return this._origin
  }

  current = computed(() => this._map[this._key.value] ?? null)

  index = computed(() => this._origin.findIndex(item => item.condition === this._key.value))

  private _onProjectConfigChanged(payload: { path: string[], newValue: any, oldValue: any }) {
    const changedPath = payload.path.join('.')
    if (this._dependencies.some(dep => changedPath.startsWith(dep))) {
      let key = 'default'
      for (const condition of Object.keys(this._map)) {
        if (condition !== 'default') {
          if ((this._express.evaluateExpression<boolean>(condition, this._parent.project().origin, false) ?? false) === true) {
            key = condition
          }
        }
      }

      if (key !== this._key.value) {
        this._key.value = key
      }
    }
  }
}

export class IpDiagramsObject {
  protected _condition?: IpCondition<IpDiagramsObjectType>
  protected _refImagesCache: string[][] = []

  constructor(
    private _origin: IpDiagramsObjectType | IpDiagramsObjectConditionType[] | undefined,
    private _parent: Ip,
  ) {
    this.buildImages()
  }

  get origin(): IpDiagramsObjectType | IpDiagramsObjectConditionType[] | undefined {
    return this._origin
  }

  images = computed((): string[] => {
    if (this._origin === undefined) {
      return []
    }

    if (this._condition) {
      const index = this._condition.index.value
      if (index === -1) {
        return []
      }
      return this._refImagesCache[index]
    }
    else {
      return this._refImagesCache[0]
    }
  })

  private buildImages() {
    if (this._origin === undefined) {
      return
    }

    if (Array.isArray(this._origin)) {
      this._condition = new IpCondition<IpDiagramsObjectType>('images', this._origin, this._parent)

      for (const obj of this._origin) {
        this._refImagesCache.push(obj.content.images)
      }
    }
    else {
      this._refImagesCache.push(this._origin.images)
    }
  }
}

// #endregion

export class IpManager {
  private _map: Record<string, Record<string, Record<string, Ip>>> = markRaw({
    peripherals: {},
  })

  private _project: Project | null = null
  private _i18n: VueI18nType | null = null

  constructor() {
  }

  setProject(project: Project | null) {
    if (project) {
      this._project = markRaw(project)
    }
  }

  setI18n(i18n: VueI18nType) {
    this._i18n = markRaw(i18n)
  }

  getPeripheral(vendor: string, name: string): Ip | null {
    const vendorMap = this._map.peripherals[vendor]
    if (vendorMap?.[name]) {
      return vendorMap[name]
    }
    else {
      return null
    }
  }

  async loadPeripheral(vendor: string, name: string, define: string, summary: Summary) {
    if (!this._project) {
      return
    }

    const vendorMap = this._map.peripherals[vendor]
    if (vendorMap?.[name]) {
      return vendorMap[name]
    }

    const content = await window.electron.invoke('database:getIp', 'peripherals', vendor, define) as IpType
    if (content) {
      const instance: Ip = new Ip(name, content, this._project, this._i18n!.global.locale, summary);
      (this._map.peripherals[vendor] ??= {})[name] = markRaw(instance)
    }
  }
}

export function createIpManagerPlugin() {
  const manager = new IpManager()

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('database@ipManager', manager)
      },
    },
    setProject(project: Project | null) {
      manager.setProject(project)
    },
    setI18n(i18n: VueI18nType) {
      manager.setI18n(i18n)
    },
  }
}

export function useIpManager(): IpManager {
  return inject('database@ipManager')!
}
