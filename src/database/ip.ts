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
  IpClockTreeElementUnitType,
  IpClockTreeType,
  IpContainersType,
  IpExpressionType,
  IpObjectConditionType,
  IpObjectType,
  IpParameterType,
  IpParameterValueUnitSignalUnitType,
  IpParameterValueUnitType,
  IpRefParameterType,
  IpType,
} from '@/electron/database'
import type { Emitter } from 'mitt'
import type { App } from 'vue'
import type { ValueHub } from '~/events'
import mitt from 'mitt'
import { inject } from 'vue'
import { evaluateExpression, evaluateExtract } from '~/utils/express'
import { I18n } from './i18n'

// #region typedef

// eslint-disable-next-line ts/consistent-type-definitions
type IpEvent = {
  activatedChanged: { name: string, oldValue: boolean, newValue: boolean }
}

export class Ip {
  private _origin: IpType
  private _parameters?: Record<string, IpParameter>
  private _parametersConditions: Record<string, IpCondition<IpParameterType>> = {}
  private _containers?: IpContainers
  private _presets?: Record<string, IpObject>
  private _pins?: Record<string, Record<string, Record<string, IpPin>>>
  private _clockTree?: IpClockTree
  private _instance: string
  private _valueHub: ValueHub
  private _emitter = mitt<IpEvent>()
  private _activated?: boolean
  private _activatedDependencies: string[] = []
  private _signals?: string[]

  constructor(instance: string, origin: IpType, valueHub: ValueHub) {
    this._instance = instance
    this._origin = origin
    this._valueHub = valueHub
  }

  get origin(): IpType {
    return this._origin
  }

  get parameters(): Record<string, IpParameter> {
    if (!this._parameters) {
      this._parameters = {}
      for (const [name, value] of Object.entries(this._origin.parameters)) {
        if (Array.isArray(value)) {
          const condition = new IpCondition<IpParameterType>(name, value, this)
          this._parametersConditions[name] = condition
          const parameters = condition.current
          if (parameters) {
            this._parameters[name] = this._createParameter(parameters, name)
          }
          condition.emitter.on('changed', (payload: { name: string, oldValue: IpParameter, newValue: IpParameter }) => {
            console.debug(`Parameter condition changed: ${payload.name}`, payload)
          })
        }
        else {
          this._parameters[name] = this._createParameter(value, name)
        }
      }
    }
    return this._parameters
  }

  get containers(): IpContainers {
    if (!this._containers) {
      this._containers = new IpContainers(this._origin.containers ?? {}, this.parameters, this)
    }
    return this._containers
  }

  get presets(): Record<string, IpObject> {
    if (!this._presets) {
      this._presets = {}
      for (const [presetName, presetValue] of Object.entries(this._origin.presets ?? {})) {
        this._presets[presetName] = new IpObject(presetValue, this.parameters, this)
      }
    }
    return this._presets
  }

  get pins(): Record<string, Record<string, Record<string, IpPin>>> | null {
    if (this._origin.pins) {
      if (!this._pins) {
        this._pins = {}
        for (const [name, value] of Object.entries(this._origin.pins)) {
          this._pins[name] = {}
          for (const [subName, subValue] of Object.entries(value)) {
            this._pins[name][subName] = {}
            for (const [pinName, pinValue] of Object.entries(subValue)) {
              this._pins[name][subName][pinName] = new IpPin(pinValue)
            }
          }
        }
      }
      return this._pins
    }
    return null
  }

  get activated(): boolean {
    if (this._activated === undefined) {
      if (this._origin.activated !== undefined) {
        const condition = this.getExpression(this._origin.activated)
        this._activated = evaluateExpression<boolean>(condition, this.valueHub().values(), false) as boolean
        const set = new Set<string>()
        evaluateExtract(condition).forEach((item) => {
          set.add(item)
        })
        this._activatedDependencies = Array.from(set)
        this.valueHub().emitter.on('valueChanged', this._onValueHubValueChanged.bind(this))
      }
      else {
        this._activated = true
      }
    }
    return this._activated
  }

  get instance(): string {
    return this._instance
  }

  get emitter(): Emitter<IpEvent> {
    return this._emitter
  }

  get signals(): string[] {
    if (!this._signals) {
      const signals = new Set<string>()
      for (const [_name, parameter] of Object.entries(this.parameters)) {
        if (parameter.type === 'enum') {
          const parameterEnum = parameter as IpParameterEnum
          for (const signal of parameterEnum.signals) {
            signals.add(signal)
          }
        }
      }
      this._signals = Array.from(signals)
      this._signals.sort()
    }
    return this._signals
  }

  get clockTree(): IpClockTree | null {
    if (this._clockTree === undefined) {
      if (this._origin.clockTree) {
        this._clockTree = new IpClockTree(this._origin.clockTree)
      }
    }
    return this._clockTree ?? null
  }

  getExpression(expr: string) {
    expr = expr.replace(/\$\{INSTANCE\}/g, this._instance)
    return expr
  }

  valueHub(): ValueHub {
    return this._valueHub
  }

  private _createParameter(parameter: IpParameterType, name: string): IpParameter {
    if (parameter.type === 'enum') {
      return new IpParameterEnum(parameter, name, this)
    }
    else if (parameter.type === 'float') {
      return new IpParameterNumber(parameter, name, this)
    }
    else if (parameter.type === 'integer') {
      return new IpParameterNumber(parameter, name, this)
    }
    else if (parameter.type === 'boolean') {
      return new IpParameterBoolean(parameter, name, this)
    }
    else if (parameter.type === 'radio') {
      return new IpParameterRadio(parameter, name, this)
    }
    else {
      return new IpParameterString(parameter, name, this)
    }
  }

  private _onValueHubValueChanged(payload: { path: string[], oldValue: any, newValue: any }) {
    if (this._activatedDependencies.includes(payload.path.join('.'))) {
      const condition = this.getExpression(this._origin.activated ?? '')
      const value = evaluateExpression<boolean>(condition, this.valueHub().values(), false) as boolean
      if (value !== this._activated) {
        const oldValue = this._activated
        this._activated = value
        this._emitter.emit('activatedChanged', { name: this._instance, oldValue: (oldValue as boolean), newValue: value })
      }
    }
  }
}

// #region typedef IpParameter

export type IpParameter =
  IpParameterEnum |
  IpParameterNumber |
  IpParameterBoolean |
  IpParameterRadio |
  IpParameterString

export class IpParameterBase {
  protected _origin: IpParameterType
  private _display?: I18n
  private _description?: I18n
  protected _parent: Ip
  private _name: string

  constructor(origin: IpParameterType, name: string, parent: Ip) {
    this._origin = origin
    this._name = name
    this._parent = parent
  }

  get origin(): IpParameterType {
    return this._origin
  }

  get display(): I18n {
    return this._display ??= new I18n(this._origin.display ?? { en: '' })
  }

  get description(): I18n {
    return this._description ??= new I18n(this._origin.description ?? { en: '' })
  }

  get readonly(): boolean {
    return this._origin.readonly ?? false
  }

  get type(): 'string' | 'boolean' | 'enum' | 'integer' | 'float' | 'radio' {
    return this._origin.type
  }

  get visible(): boolean {
    return this._origin.visible ?? true
  }

  get expression(): IpExpression | null {
    if (this._origin.expression) {
      return new IpExpression(this._origin.expression)
    }
    return null
  }

  get name(): string {
    return this._name
  }
}

export class IpParameterValueUnitSignalUnit {
  private _origin: IpParameterValueUnitSignalUnitType

  constructor(origin: IpParameterValueUnitSignalUnitType) {
    this._origin = origin
  }

  get mode(): string {
    return this._origin.mode
  }
}

export class IpParameterValueUnit {
  private _origin: IpParameterValueUnitType
  private _signals?: Record<string, IpParameterValueUnitSignalUnit> | null
  private _comment?: I18n
  private _parent: Ip

  constructor(origin: IpParameterValueUnitType, parent: Ip) {
    this._origin = origin
    this._parent = parent
  }

  get expression(): IpExpression | null {
    if (this._origin.expression) {
      return new IpExpression(this._origin.expression)
    }
    return null
  }

  get comment(): I18n {
    return this._comment ??= new I18n(this._origin.comment ?? { en: '' })
  }

  get signals(): Record<string, IpParameterValueUnitSignalUnit> | null {
    if (this._signals === undefined) {
      if (this._origin.signals) {
        this._signals = {}
        for (const [name, value] of Object.entries(this._origin.signals)) {
          const key = this._parent.getExpression(name)
          this._signals[key] = new IpParameterValueUnitSignalUnit(value)
        }
      }
      else {
        this._signals = null
      }
    }
    return this._signals
  }
}

export class IpParameterEnum extends IpParameterBase {
  private _values?: Record<string, IpParameterValueUnit>
  private _signals?: string[]

  get default(): string {
    return this._origin.default as string
  }

  get values(): Record<string, IpParameterValueUnit> {
    if (!this._values) {
      this._values = {}
      for (const [name, value] of Object.entries(this._origin.values ?? {})) {
        this._values[name] = new IpParameterValueUnit(value, this._parent)
      }
    }
    return this._values
  }

  get signals(): string[] {
    if (!this._signals) {
      const signals = new Set<string>()
      for (const [_name, value] of Object.entries(this.values)) {
        if (value.signals) {
          for (const signal of Object.keys(value.signals)) {
            signals.add(signal)
          }
        }
      }
      this._signals = Array.from(signals)
      this._signals.sort()
    }
    return this._signals
  }
}

export class IpParameterNumber extends IpParameterBase {
  get default(): number {
    return this._origin.default as number
  }

  get max(): number {
    return this._origin.max as number ?? Infinity
  }

  get min(): number {
    return this._origin.min as number ?? -Infinity
  }
}

export class IpParameterBoolean extends IpParameterBase {
  get default(): boolean {
    return this._origin.default as boolean
  }
}

export class IpParameterRadio extends IpParameterBase {
  get default(): boolean {
    return this._origin.default as boolean
  }

  get group(): string {
    return this._origin.group as string
  }
}

export class IpParameterString extends IpParameterBase {
  get default(): string {
    return this._origin.default as string
  }
}

// #endregion

// eslint-disable-next-line ts/consistent-type-definitions
type IpObjectEvent = {
  changed: void
}

export class IpObject {
  protected _origin: IpObjectType | IpObjectConditionType[]
  protected _parameters: Record<string, IpParameter>
  protected _refParameters?: Record<string, IpRefParameter>
  protected _refParametersConditions: IpCondition<IpObjectType>[] = []
  protected _parent: Ip
  protected _emitter = mitt<IpObjectEvent>()

  constructor(origin: IpObjectType | IpObjectConditionType[], parameters: Record<string, IpParameter>, parent: Ip) {
    this._origin = origin
    this._parameters = parameters
    this._parent = parent
  }

  get origin(): IpObjectType | IpObjectConditionType[] {
    return this._origin
  }

  get refParameters(): Record<string, IpRefParameter> {
    if (!this._refParameters) {
      this._refParameters = {}
      let refParameters: Record<string, IpRefParameterType> = {}
      if (Array.isArray(this._origin)) {
        const condition = new IpCondition<IpObjectType>('refParameters', this._origin, this._parent)
        this._refParametersConditions.push(condition)
        refParameters = condition.current?.refParameters ?? {}
        condition.emitter.on('changed', this._onConditionChanged.bind(this))
      }
      else {
        refParameters = this._origin.refParameters ?? {}
      }
      for (const [name, value] of Object.entries(refParameters)) {
        const parameter = this._parameters[name]
        this._refParameters[name] = new IpRefParameter(name, value, parameter, this._parent)
      }
    }
    return this._refParameters
  }

  get emitter(): Emitter<IpObjectEvent> {
    return this._emitter
  }

  private _onConditionChanged(payload: { name: string, oldValue: IpObjectType | null, newValue: IpObjectType | null }) {
    this._refParameters = {}
    for (const [name, value] of Object.entries(payload.newValue?.refParameters ?? {})) {
      const parameter = this._parameters[name]
      this._refParameters[name] = new IpRefParameter(name, value, parameter, this._parent)
    }
    this._emitter.emit('changed')
  }
}

// eslint-disable-next-line ts/consistent-type-definitions
type IpObjectUnitEvent = {
  conditionChanged: { name: string, oldValue: boolean, newValue: boolean }
}

export class IpRefParameter {
  private _origin: IpRefParameterType
  private _parameter: IpParameter
  private _condition?: boolean
  private _parent: Ip
  private _dependencies: string[] = []
  private _emitter = mitt<IpObjectUnitEvent>()
  private _name: string

  constructor(name: string, origin: IpRefParameterType, parameter: IpParameter, parent: Ip) {
    this._name = name
    this._origin = origin
    this._parameter = parameter
    this._parent = parent
  }

  get name(): string {
    return this._name
  }

  get origin(): IpRefParameterType {
    return this._origin
  }

  get values(): string[] {
    return this._origin.values ?? Object.keys(this._parameter.origin.values ?? {})
  }

  get default(): string | number | boolean {
    return this._origin.default ?? this._parameter.default
  }

  get readonly(): boolean {
    return this._origin.readonly ?? this._parameter.readonly ?? false
  }

  get condition(): boolean {
    if (this._condition === undefined) {
      if (this._origin.condition !== undefined) {
        const condition = this._parent.getExpression(this._origin.condition)
        this._condition = evaluateExpression<boolean>(condition, this._parent.valueHub().values(), false) as boolean
        const set = new Set<string>()
        evaluateExtract(condition).forEach((item) => {
          set.add(item)
        })
        this._dependencies = Array.from(set)
        this._parent.valueHub().emitter.on('valueChanged', this._onValueHubValueChanged.bind(this))
      }
      else {
        this._condition = true
      }
    }
    return this._condition
  }

  get parameter(): IpParameter {
    return this._parameter
  }

  get emitter(): Emitter<IpObjectUnitEvent> {
    return this._emitter
  }

  private _onValueHubValueChanged(payload: { path: string[], oldValue: any, newValue: any }) {
    if (this._dependencies.includes(payload.path.join('.'))) {
      const condition = this._parent.getExpression(this._origin.condition ?? '')
      const value = evaluateExpression<boolean>(condition, this._parent.valueHub().values(), false) as boolean
      if (value !== this._condition) {
        const oldValue = this._condition
        this._condition = value
        this._emitter.emit('conditionChanged', { name: this._name, oldValue: (oldValue as boolean), newValue: value })
      }
    }
  }
}

export class IpContainerObject extends IpObject {
}

export class IpContainers {
  private _origin: IpContainersType
  private _parameters: Record<string, IpParameter>
  private _overview?: IpContainerObject
  private _modes?: IpContainerObject
  private _configurations?: IpContainerObject
  private _parent: Ip

  constructor(origin: IpContainersType, parameters: Record<string, IpParameter>, parent: Ip) {
    this._origin = origin
    this._parameters = parameters
    this._parent = parent
  }

  get origin(): IpContainersType {
    return this._origin
  }

  get overview(): IpContainerObject {
    if (!this._overview) {
      this._overview = new IpContainerObject(this._origin.overview ?? {}, this._parameters, this._parent)
    }
    return this._overview
  }

  get modes(): IpContainerObject {
    if (!this._modes) {
      this._modes = new IpContainerObject(this._origin.modes ?? {}, this._parameters, this._parent)
    }
    return this._modes
  }

  get configurations(): IpContainerObject {
    if (!this._configurations) {
      this._configurations = new IpContainerObject(this._origin.configurations ?? {}, this._parameters, this._parent)
    }
    return this._configurations
  }
}

export class IpPin {
  private _origin: {
    default: boolean
  }

  constructor(origin: {
    default: boolean
  }) {
    this._origin = origin
  }

  get default(): boolean {
    return this._origin.default
  }
}

export class IpExpression {
  private _origin: IpExpressionType

  constructor(origin: IpExpressionType) {
    this._origin = origin
  }

  get display(): string {
    return this._origin.display
  }

  get real(): number {
    return 0
  }
}

// eslint-disable-next-line ts/consistent-type-definitions
type IpConditionEvent = {
  changed: { name: string, oldValue: any, newValue: any }
}

export class IpCondition<T> {
  private _name: string
  private _origin: { condition: string, content: T }[]
  private _current: T | null = null
  private _parent: Ip
  private _dependencies: string[]
  private _emitter = mitt<IpConditionEvent>()

  constructor(name: string, origin: { condition: string, content: T }[], parent: Ip) {
    this._name = name
    this._origin = origin
    this._parent = parent

    const set = new Set<string>()
    let defaultValue = null
    for (const item of this._origin) {
      const condition = this._parent.getExpression(item.condition)

      if (condition === 'default') {
        defaultValue = item.content
      }
      else {
        evaluateExtract(condition).forEach((item) => {
          set.add(item)
        })

        if (evaluateExpression<boolean>(condition, this._parent.valueHub().values(), false) === true) {
          this._current = item.content
        }
      }
    }
    if (this._current === null) {
      this._current = defaultValue
    }

    this._dependencies = Array.from(set)

    this._parent.valueHub().emitter.on('valueChanged', this._onValueHubValueChanged.bind(this))
  }

  get name(): string {
    return this._name
  }

  get origin(): { condition: string, content: T }[] {
    return this._origin
  }

  get current(): T | null {
    return this._current
  }

  get emitter(): Emitter<IpConditionEvent> {
    return this._emitter
  }

  private _onValueHubValueChanged(payload: { path: string[], oldValue: any, newValue: any }) {
    if (this._dependencies.includes(payload.path.join('.'))) {
      let defaultValue
      let value = null
      for (const item of this._origin) {
        const condition = this._parent.getExpression(item.condition)
        if (condition === 'default') {
          defaultValue = item.content
        }
        else {
          if (evaluateExpression<boolean>(condition, this._parent.valueHub().values(), false) === true) {
            value = item.content
          }
        }
      }
      if (value === undefined && defaultValue !== undefined) {
        value = defaultValue
      }

      if (value !== this._current) {
        const oldValue = this._current
        this._current = value
        this._emitter.emit('changed', { name: this.name, oldValue, newValue: value })
      }
    }
  }
}

export class IpClockTree {
  private _origin: IpClockTreeType
  private _elements?: Record<string, IpClockTreeElementUnit>
  private _i18n?: Record<string, I18n>

  constructor(origin: IpClockTreeType) {
    this._origin = origin
  }

  get origin(): IpClockTreeType {
    return this._origin
  }

  get elements(): Record<string, IpClockTreeElementUnit> {
    if (!this._elements) {
      this._elements = {}
      const rawElements = this._origin.elements ?? {}
      for (const [name, element] of Object.entries(rawElements)) {
        this._elements[name] = new IpClockTreeElementUnit(element)
      }
    }
    return this._elements
  }

  get i18n(): Record<string, I18n> {
    if (!this._i18n) {
      this._i18n = {}
      const rawI18n = this._origin.i18n ?? {}
      for (const [name, entry] of Object.entries(rawI18n)) {
        this._i18n[name] = new I18n(entry)
      }
    }
    return this._i18n
  }
}

export class IpClockTreeElementUnit {
  private _origin: IpClockTreeElementUnitType

  constructor(origin: IpClockTreeElementUnitType) {
    this._origin = origin
  }

  get origin(): IpClockTreeElementUnitType {
    return this._origin
  }

  get refParameter(): string {
    return this._origin.refParameter ?? ''
  }

  get type(): string {
    return this._origin.type ?? ''
  }

  get enable(): string | boolean | null {
    return this._origin.enable ?? null
  }

  get output(): string[] {
    return this._origin.output ?? []
  }

  get input(): string[] {
    return this._origin.input ?? []
  }
}

// #endregion

export class IpManager {
  private _map: Record<string, Record<string, Record<string, Ip>>> = {
    peripherals: {},
  }

  private _valueHub: ValueHub

  constructor(valueHub: ValueHub) {
    this._valueHub = valueHub
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

  async loadPeripheral(vendor: string, name: string, define: string) {
    const vendorMap = this._map.peripherals[vendor]
    if (vendorMap?.[name]) {
      return vendorMap[name]
    }

    const content = await window.electron.invoke('database:getIp', 'peripherals', vendor, define) as IpType
    if (content) {
      const instance: Ip = new Ip(name, content, this._valueHub);
      (this._map.peripherals[vendor] ??= {})[name] = instance
    }
  }
}

export function createIpManagerPlugin(valueHub: ValueHub) {
  const manager = new IpManager(valueHub)

  return {
    value: manager,
    plugin: {
      install(app: App) {
        app.provide('database:ipManager', manager)
      },
    },
  }
}

export function useIpManager(): IpManager {
  return inject('database:ipManager')!
}
