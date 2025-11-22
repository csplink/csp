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

import type { BrowserWindowArgsType, SystemBrowserWindow } from '@/electron/types'
import type { IpcMainEvent, IpcMainInvokeEvent } from 'electron'
import { existsSync } from 'node:fs'
import { join } from 'node:path'
import { app, BrowserWindow, ipcMain, shell } from 'electron'
import { createWindow } from '../src/window'
import { getExeFolder } from '../utils'

export function registerSystemHandler() {
  ipcMain.on('system:openUrl', (_event, url: string) => {
    shell.openExternal(url)
  })
  ipcMain.handle('system:getArgs', (event: IpcMainInvokeEvent) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    return win.userData
  })
  ipcMain.handle('system:isDev', (_event) => {
    if (!app.isPackaged) {
      return true
    }

    const devFilePath = join(getExeFolder(), '.dev')

    if (existsSync(devFilePath)) {
      return true
    }

    return false
  })
  ipcMain.on('system:createWindow', (event: IpcMainEvent, args: BrowserWindowArgsType) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    const data = win.userData!
    args.backendUrl = data.backendUrl
    createWindow(args)
  })
  ipcMain.on('system:close', (event: IpcMainEvent) => {
    const win = BrowserWindow.fromWebContents(event.sender)
    win?.close()
  })
  ipcMain.on('system:openDevTools', (event: IpcMainEvent) => {
    const win = BrowserWindow.fromWebContents(event.sender)
    win?.webContents.openDevTools()
  })
}
