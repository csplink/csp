/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        settings.ts
 *  @brief       Settings persistence utility for CSP application (Electron IPC)
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
 *  2025-07-26     xqyjlj       initial version
 */

import type { AppSettingsType, I18nModeType, SettingsRecentProjectItemType, SystemSettingsType, ThemeModeType } from '@/electron/types'
import type { Emitter } from 'mitt'
import type { App } from 'vue'
import type { VueI18nType } from '~/i18n'
import mitt from 'mitt'
import { computed, inject, markRaw, reactive, watchEffect } from 'vue'
import { applyLocale } from '~/i18n'
import { applyTheme, applyThemeColor } from './theme'

/**
 * Save settings to the YAML file via IPC
 */
export async function saveSettings(settings: AppSettingsType): Promise<void> {
  try {
    await window.electron.invoke('settings:save', settings)
  }
  catch (error) {
    console.error('Failed to save settings via IPC:', error)
    throw error
  }
}

/**
 * Reset settings to defaults and save via IPC
 */
export async function resetSettings(): Promise<AppSettingsType> {
  try {
    return await window.electron.invoke('settings:reset')
  }
  catch (error) {
    console.error('Failed to reset settings via IPC:', error)
    throw error
  }
}

// #region typedef

// eslint-disable-next-line ts/consistent-type-definitions
export type AppSettingsEventType = {
  changed: { path: string, newValue: any, oldValue: any }
}

export class AppSettings {
  private _origin: AppSettingsType
  private _emitter = mitt<AppSettingsEventType>()
  private _system?: SystemSettings

  constructor(origin: AppSettingsType) {
    this._origin = origin
  }

  get origin(): AppSettingsType {
    return this._origin
  }

  get emitter(): Emitter<AppSettingsEventType> {
    return this._emitter
  }

  get system(): SystemSettings {
    if (this._system === undefined) {
      this._system = new SystemSettings(this._origin.system)
      this._system.emitter.on('changed', (payload: { path: string, newValue: any, oldValue: any }) => {
        this._emitter.emit('changed', { path: `system\0${payload.path}`, newValue: payload.newValue, oldValue: payload.oldValue })
      })
    }
    return this._system
  }

  get recentProjects(): Record<string, SettingsRecentProjectItemType> {
    return this._origin.recentProjects ?? {}
  }

  /**
   * 删除指定路径的最近项目
   */
  removeRecentProject(projectPath: string): void {
    if (this._origin.recentProjects?.[projectPath]) {
      const old = { ...this._origin.recentProjects[projectPath] }
      delete this._origin.recentProjects[projectPath]
      this._emitter.emit('changed', { path: `recentProjects\0${projectPath}`, newValue: null, oldValue: old })
    }
  }
}

// eslint-disable-next-line ts/consistent-type-definitions
export type SystemSettingsEventType = {
  changed: { path: string, newValue: any, oldValue: any }
}

export class SystemSettings {
  private _emitter = mitt<SystemSettingsEventType>()
  private _state
  constructor(
    private _origin: SystemSettingsType,
  ) {
    this._state = reactive(this._origin)
  }

  get origin(): SystemSettingsType {
    return this._origin
  }

  get emitter(): Emitter<SystemSettingsEventType> {
    return this._emitter
  }

  theme = computed({
    get: (): ThemeModeType => this._state.theme,
    set: (value: ThemeModeType) => {
      const old = this._state.theme
      this._state.theme = value
      this._emitter.emit('changed', { path: 'theme', newValue: value, oldValue: old })
    },
  })

  themeColor = computed({
    get: (): string => this._state.themeColor,
    set: (value: string) => {
      const old = this._state.themeColor
      this._state.themeColor = value
      this._emitter.emit('changed', { path: 'themeColor', newValue: value, oldValue: old })
    },
  })

  language = computed({
    get: (): I18nModeType => this._state.language,
    set: (value: I18nModeType) => {
      const old = this._state.language
      this._state.language = value
      this._emitter.emit('changed', { path: 'language', newValue: value, oldValue: old })
    },
  })

  autoUpdate = computed({
    get: (): boolean => this._state.autoUpdate,
    set: (value: boolean) => {
      const old = this._state.autoUpdate
      this._state.autoUpdate = value
      this._emitter.emit('changed', { path: 'autoUpdate', newValue: value, oldValue: old })
    },
  })

  telemetry = computed({
    get: (): boolean => this._state.telemetry,
    set: (value: boolean) => {
      const old = this._state.telemetry
      this._state.telemetry = value
      this._emitter.emit('changed', { path: 'telemetry', newValue: value, oldValue: old })
    },
  })

  crashReports = computed({
    get: (): boolean => this._state.crashReports,
    set: (value: boolean) => {
      const old = this._state.crashReports
      this._state.crashReports = value
      this._emitter.emit('changed', { path: 'crashReports', newValue: value, oldValue: old })
    },
  })

  autoSave = computed({
    get: (): boolean => this._state.autoSave,
    set: (value: boolean) => {
      const old = this._state.autoSave
      this._state.autoSave = value
      this._emitter.emit('changed', { path: 'autoSave', newValue: value, oldValue: old })
    },
  })
}

// #endregion

export class SettingsManager {
  private _settings: AppSettings | null = null

  async init(i18n: VueI18nType) {
    this._settings = markRaw(new AppSettings(await window.electron.invoke('settings:load')))

    this._settings.emitter.on('changed', (payload: { path: string, newValue: any, oldValue: any }) => {
      window.electron.invoke('settings:update', payload.path, payload.newValue)
    })

    watchEffect(() => {
      applyTheme(this._settings!.system.theme.value)
    })

    watchEffect(() => {
      applyThemeColor(this._settings!.system.themeColor.value)
    })

    watchEffect(() => {
      applyLocale(this._settings!.system.language.value, i18n)
    })
  }

  get settings(): AppSettings {
    return this._settings!
  }
}

export function createSettingsManagerPlugin() {
  const manager = new SettingsManager()

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('utils@settingsManager', manager)
      },
    },
    async init(i18n: VueI18nType) {
      await manager.init(i18n)
    },
  }
}

export function useSettingsManager(): SettingsManager {
  return inject('utils@settingsManager')!
}
