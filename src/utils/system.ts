/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        system.ts
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
 *  2025-08-04     xqyjlj       initial version
 */

import type { BrowserWindowArgsType } from '@/electron/types'
import { defineStore } from 'pinia'

export function openUrl(url: string) {
  if (!url)
    return
  window.electron.send('system:openUrl', url)
}

export async function getSystemArgs(): Promise<BrowserWindowArgsType> {
  return await window.electron.invoke('system:getArgs')
}

export async function isDev(): Promise<boolean> {
  return await window.electron.invoke('system:isDev')
}

export function createWindow(args: BrowserWindowArgsType) {
  window.electron.send('system:createWindow', args)
}

export function closeWindow() {
  window.electron.send('system:close')
}

export function openDevTools() {
  window.electron.send('system:openDevTools')
}

export const useSystemStore = defineStore('SystemStore', {
  state: () => {
    return {
      args: {
        runMode: 'startup',
      } as BrowserWindowArgsType,
    }
  },
})
