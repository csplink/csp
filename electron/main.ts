/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        main.ts
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
 *  2025-04-26     xqyjlj       initial version
 */

import type { ProcessArgsType } from './types'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { app, BrowserWindow } from 'electron'
import * as handlers from './ipc-handlers'
import { createWindow } from './src/window'
import { clientOffline, createServer, processArgs } from './utils'
import './src/cli'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

process.env.APP_ROOT = path.join(__dirname, '..')

export const VITE_DEV_SERVER_URL = process.env.VITE_DEV_SERVER_URL
export const MAIN_DIST = path.join(process.env.APP_ROOT, 'dist-electron')
export const RENDERER_DIST = path.join(process.env.APP_ROOT, 'dist')

process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL ? path.join(process.env.APP_ROOT, 'public') : RENDERER_DIST
process.env.MAIN_DIST = MAIN_DIST
process.env.RENDERER_DIST = RENDERER_DIST

const gotTheLock = app.requestSingleInstanceLock(processArgs)
if (!gotTheLock) {
  app.quit()
}

app.on('second-instance', (_event: Electron.Event, _argv: string[], _workingDirectory: string, additionalData: unknown) => {
  const data = additionalData as ProcessArgsType
  createWindow(data)
})

app.on('window-all-closed', () => {
  clientOffline(processArgs.backendUrl)
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', async () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    processArgs.backendUrl = await createServer()
    createWindow(processArgs)
  }
})

app.whenReady().then(async () => {
  processArgs.backendUrl = await createServer()
  createWindow(processArgs)
})

app.whenReady().then(() => {
  const handlersTyped = handlers as Record<string, () => void>
  for (const handler in handlersTyped) {
    handlersTyped[handler]()
  }
})
