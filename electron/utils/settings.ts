/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        settings.ts
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
 *  2025-07-26     xqyjlj       initial version
 */

import type { AppSettingsType, SettingsRecentProjectItemType, SystemSettingsType } from '@/electron/types'
import fs from 'node:fs'
import os from 'node:os'
import path, { dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { app, nativeTheme } from 'electron'
import yaml from 'yaml'
import { getProject } from './project'

export const DEFAULT_SYSTEM_SETTINGS: SystemSettingsType = {
  theme: 'light',
  themeColor: '#409EFF',
  language: 'en',
  autoUpdate: true,
  telemetry: true,
  crashReports: true,
  autoSave: true,
}

const SETTINGS_FILE_NAME = '.csp.settings'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const __root = path.join(__dirname, '..')
const __resourceFolder = app.isPackaged ? process.resourcesPath : path.join(__root, 'resources')
let _appSettings: AppSettingsType | undefined

/**
 * Return the path of the settings file
 *
 * @returns {string} The path of the settings file
 */
function getSettingsPath(): string {
  return path.join(os.homedir(), '.csp', SETTINGS_FILE_NAME)
}

/**
 * Synchronously loads settings from a file.
 * If the settings file does not exist, or if an error occurs during loading,
 * default settings are returned.
 *
 * @returns {AppSettingsType} The loaded settings merged with default settings.
 */

function _loadSettingsSync(): AppSettingsType {
  try {
    const settingsPath = getSettingsPath()

    if (!fs.existsSync(settingsPath)) {
      return {
        system: DEFAULT_SYSTEM_SETTINGS,
        recentProjects: {},
      }
    }

    const fileContent = fs.readFileSync(settingsPath, 'utf-8')
    const parsedSettings = yaml.parse(fileContent) as AppSettingsType

    if (Array.isArray(parsedSettings.recentProjects)) {
      parsedSettings.recentProjects = {} /* !< 兼容旧版本 */
    }

    return parsedSettings
  }
  catch (error) {
    console.warn('Failed to load settings, using defaults:', error)
    return {
      system: DEFAULT_SYSTEM_SETTINGS,
      recentProjects: {},
    }
  }
}

/**
 * Synchronously loads settings from a file.
 * If the settings file does not exist, or if an error occurs during loading,
 * default settings are returned.
 *
 * @returns {AppSettingsType} The loaded settings merged with default settings.
 */

export function loadSettingsSync(): AppSettingsType {
  if (!_appSettings) {
    _appSettings = _loadSettingsSync()
  }
  return _appSettings
}

export function getSettingsSync(): AppSettingsType {
  return _appSettings!
}

export function getRealTheme(): 'light' | 'dark' {
  return nativeTheme.shouldUseDarkColors ? 'dark' : 'light'
}

/**
 * Synchronously saves settings to a file.
 * If the settings directory does not exist, it will be created.
 * If an error occurs during saving, an error will be thrown.
 *
 * @param {AppSettingsType} settings The settings to be saved.
 */
export function saveSettingsSync(settings: AppSettingsType) {
  try {
    const settingsPath = getSettingsPath()
    const yamlContent = yaml.stringify(settings, {
      indent: 2,
      lineWidth: 0,
      minContentWidth: 0,
    })

    const settingsDir = path.join(path.dirname(settingsPath))
    if (!fs.existsSync(settingsDir)) {
      fs.mkdirSync(settingsDir, { recursive: true })
    }

    fs.writeFileSync(settingsPath, yamlContent, 'utf-8')
  }
  catch (error) {
    console.error('Failed to save settings:', error)
    throw error
  }
}

function _updateSettingsSync(path: string, value: any) {
  const keys = path.split('\0')
  let item: any = _appSettings

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
}

export function updateSettingsSync(path: string, value: any) {
  if (!_appSettings) {
    _appSettings = _loadSettingsSync()
  }
  _updateSettingsSync(path, value)
  saveSettingsSync(_appSettings)
}

export function addRecentProjects(projectPath: string) {
  const appSettings = loadSettingsSync()
  appSettings.recentProjects ??= {}

  const absolutePath = path.resolve(projectPath).replace(/\\/g, '/') /* !< 强制转为绝对路径 */
  const projectInfo = getProject(absolutePath)

  if (!projectInfo) {
    return
  }

  /* !< 创建新的项目项 */
  const projectItem: SettingsRecentProjectItemType = {
    path: absolutePath,
    lastModified: new Date().toISOString(),
    projectName: projectInfo?.name,
    targetChip: projectInfo?.targetChip,
  }

  /* !< 如果已存在该项目，先删除旧的 */
  if (appSettings.recentProjects[absolutePath]) {
    delete appSettings.recentProjects[absolutePath]
  }

  /* !< 添加到最前面 */
  const newRecentProjects: Record<string, SettingsRecentProjectItemType> = {}
  newRecentProjects[absolutePath] = projectItem

  /* !< 按时间顺序添加其他项目 */
  Object.entries(appSettings.recentProjects)
    .sort(([, a], [, b]) => new Date(b.lastModified).getTime() - new Date(a.lastModified).getTime())
    .slice(0, 9)/* !< 限制最多10个项目（包括新添加的） */
    .forEach(([path, item]) => {
      newRecentProjects[path] = item
    })

  appSettings.recentProjects = newRecentProjects
  saveSettingsSync(appSettings)
}

export function getExePath(): string {
  return app.getPath('exe')
}

export function getExeFolder(): string {
  return dirname(getExePath())
}

export function getResourceFolder(): string {
  return __resourceFolder
}

export function getServerFolder(): string {
  return path.join(getResourceFolder(), 'server')
}

export function getDiagramsFolder(): string {
  return path.join(getResourceFolder(), 'images', 'diagrams')
}
