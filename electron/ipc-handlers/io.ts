/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        io.ts
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
 *  2025-07-13     xqyjlj       initial version
 */

import type { OpenDialogOptions, SaveDialogOptions } from 'electron'
import * as fs from 'node:fs/promises'
import path from 'node:path'
import { ipcMain } from 'electron'
import { saveFileWithDialog, showOpenDialog } from '../utils'

export function registerIoHandler() {
  ipcMain.handle('io:saveFileWithDialog', async (_event, payload: { content: string | ArrayBuffer, options?: SaveDialogOptions }) => {
    return await saveFileWithDialog(payload.content, payload.options)
  })
  ipcMain.handle('io:showOpenDialog', async (_event, payload: { options?: OpenDialogOptions }) => {
    return await showOpenDialog(payload.options)
  })
  ipcMain.handle('io:mkdir', async (_event, dirPath: string) => {
    try {
      const fullPath = path.resolve(dirPath)
      await fs.mkdir(fullPath, { recursive: true })
      return { success: true, path: fullPath }
    }
    catch (err: any) {
      return { success: false, error: err.message }
    }
  })
  ipcMain.handle('io:writeFile', async (_event, payload: { path: string, content: string }) => {
    try {
      await fs.writeFile(payload.path, payload.content, 'utf8')
      return { success: true, path: payload.path }
    }
    catch (err: any) {
      return { success: false, error: err.message }
    }
  })
}
