/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        window.ts
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
 *  2025-08-13     xqyjlj       initial version
 */

import type { IpcMainEvent } from 'electron'
import type { BrowserWindowArgsType, SystemBrowserWindow } from '../types'
import path from 'node:path'
import { BrowserWindow, ipcMain } from 'electron'

const windowList: BrowserWindow[] = []

export function createWindow(args: BrowserWindowArgsType) {
  const { VITE_DEV_SERVER_URL, RENDERER_DIST, MAIN_DIST } = process.env

  let routerKey = ''
  const runMode = args.runMode
  if (runMode === 'startup') {
    routerKey = 'startup'
  }
  else if (runMode === 'main') {
    routerKey = 'welcome'
  }
  else if (runMode === 'createProject') {
    routerKey = 'createProject'
  }
  else {
    return
  }

  let splash: BrowserWindow | null = null

  if (runMode === 'main') {
    splash = new BrowserWindow({
      width: 1100,
      height: 750,
      frame: false,
    })
    if (VITE_DEV_SERVER_URL) {
      splash.loadURL(`${VITE_DEV_SERVER_URL}/splash.html`)
    }
    else {
      splash.loadFile(path.join(RENDERER_DIST, 'splash.html'))
    }
  }

  const window = new BrowserWindow({
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
    show: false,
    webPreferences: {
      preload: path.join(MAIN_DIST, 'preload.mjs'),
    },
  })

  window.userData = args

  if (VITE_DEV_SERVER_URL) {
    let url = VITE_DEV_SERVER_URL
    if (routerKey) {
      url = `${VITE_DEV_SERVER_URL}/#/${routerKey}`
    }

    window.loadURL(url)
    window.webContents.openDevTools()
  }
  else {
    if (routerKey) {
      window.loadFile(path.join(RENDERER_DIST, 'index.html'), {
        hash: routerKey,
      })
    }
    else {
      window.loadFile(path.join(RENDERER_DIST, 'index.html'))
    }
  }

  windowList.push(window)
  window.on('close', () => {
    windowList.slice(windowList.indexOf(window), 1)
  })

  ipcMain.on('app:mounted', (event: IpcMainEvent) => {
    if (splash) {
      splash.close()
      splash = null
    }
    setTimeout(() => {
      const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
      if (runMode !== 'startup') {
        win.maximize()
      }
      else {
        win.show()
      }
    }, 500)
  })
}

export function closeAllWindow() {
  const copy1 = [...windowList]
  copy1.forEach(item => item.close())
}

export function closeAllSubWindow() {
  const copy1 = [...windowList]
  copy1.forEach((item: BrowserWindow) => {
    const data = item.userData!
    if (data.projectPath === undefined) {
      item.close()
    }
  })
}
