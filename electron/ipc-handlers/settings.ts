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
 *  2025-05-23     xqyjlj       initial version
 */

import type { AppSettingsType } from '@/electron/types'
import { ipcMain } from 'electron'
import {
  DEFAULT_SYSTEM_SETTINGS,
  loadSettingsSync,
  saveSettingsSync,
  updateSettingsSync,
} from '../utils'

export function registerSettingsHandler() {
  ipcMain.handle('settings:load', async (_event): Promise<AppSettingsType> => {
    return loadSettingsSync()
  })

  ipcMain.handle('settings:save', (_event, settings: AppSettingsType) => {
    saveSettingsSync(settings)
  })

  ipcMain.handle('settings:reset', (_event) => {
    const defaultSettings: AppSettingsType = {
      system: DEFAULT_SYSTEM_SETTINGS,
      recentProjects: loadSettingsSync().recentProjects,
    }
    saveSettingsSync(defaultSettings)
  })

  ipcMain.handle('settings:update', (_event, path: string, value: any) => {
    updateSettingsSync(path, value)
  })
}
