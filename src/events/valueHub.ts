import type { Emitter } from 'mitt'
/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        valueHub.ts
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
 *  2025-05-28     xqyjlj       initial version
 */
import type { App } from 'vue'
import mitt from 'mitt'
import { inject } from 'vue'

// eslint-disable-next-line ts/consistent-type-definitions
export type ChangeEvent = {
  changed: void
  valueChanged: { path: string[], oldValue: any, newValue: any }
}

export class ValueHub {
  private _data: Record<string, any> = {}
  private _emitter = mitt<ChangeEvent>()

  get emitter(): Emitter<ChangeEvent> {
    return this._emitter
  }

  values(): Record<string, any> {
    return this._data
  }

  assign(values: Record<string, any>): void {
    this._data = values
    this._emitter.emit('changed')
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

    this._emitter.emit('valueChanged', { path: keys, oldValue: old, newValue: value })
    this._emitter.emit('changed')
  }
}

export function createValueHubPlugin() {
  const hub = new ValueHub()

  return {
    value: hub,
    plugin: {
      install(app: App) {
        app.provide('events:valueHub', hub)
      },
    },
  }
}

export function useValueHub(): ValueHub {
  return inject('events:valueHub')!
}
