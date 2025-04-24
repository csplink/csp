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

import path from 'node:path'
import { fileURLToPath } from 'node:url'

import { app, BrowserWindow } from 'electron'
import * as handlers from './ipc-handlers'
import { args } from './src/cli'

const __dirname = path.dirname(fileURLToPath(import.meta.url))

process.env.APP_ROOT = path.join(__dirname, '..')

export const VITE_DEV_SERVER_URL = process.env.VITE_DEV_SERVER_URL
export const MAIN_DIST = path.join(process.env.APP_ROOT, 'dist-electron')
export const RENDERER_DIST = path.join(process.env.APP_ROOT, 'dist')

process.env.VITE_PUBLIC = VITE_DEV_SERVER_URL ? path.join(process.env.APP_ROOT, 'public') : RENDERER_DIST

let win: BrowserWindow | null

function createWindow() {
  let routerKey = ''
  if (args.runMode === 'startup') {
    routerKey = 'startup'
  }
  else if (args.runMode === 'main') {
    routerKey = 'chipConfigure'
  }
  else {
    return
  }

  win = new BrowserWindow({
    icon: path.join(process.env.VITE_PUBLIC, 'images', 'logo.ico'),
    frame: false,
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#ffffff',
      symbolColor: '#303133',
      height: 35,
    },
    width: 1100,
    height: 750,
    webPreferences: {
      preload: path.join(__dirname, 'preload.mjs'),
    },
  })

  if (VITE_DEV_SERVER_URL) {
    let url = VITE_DEV_SERVER_URL
    if (routerKey) {
      url = `${VITE_DEV_SERVER_URL}/#/${routerKey}`
    }

    win.loadURL(url)
    win.webContents.openDevTools()
  }
  else {
    if (routerKey) {
      win.loadFile(path.join(RENDERER_DIST, 'index.html'))
    }
    else {
      win.loadFile(path.join(RENDERER_DIST, 'index.html'), {
        hash: routerKey,
      })
    }
  }

//   win.maximize()
}

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
    win = null
  }
})

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow()
  }
})

app.whenReady().then(() => {
  createWindow()
})

app.whenReady().then(() => {
  const handlersTyped = handlers as Record<string, () => void>
  for (const handler in handlersTyped) {
    handlersTyped[handler]()
  }
})
