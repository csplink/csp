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

import type { OpenDialogOptions, OpenDialogReturnValue, SaveDialogOptions } from 'electron'

export async function saveFileWithDialog(content: string | ArrayBuffer, options?: SaveDialogOptions) {
  const response = await window.electron.invoke('io:saveFileWithDialog', { content, options })
  if (!response.success && response.message) {
    console.warn(response.message)
  }
}

export async function showOpenDialog(options?: OpenDialogOptions): Promise<OpenDialogReturnValue> {
  return await window.electron.invoke('io:showOpenDialog', { options })
}

export async function mkdir(dirPath: string) {
  const response = await window.electron.invoke('io:mkdir', dirPath)
  if (!response.success && response.message) {
    console.warn(response.message)
  }
}

export async function writeFile(path: string, content: string) {
  const response = await window.electron.invoke('io:writeFile', { path, content })
  if (!response.success && response.message) {
    console.warn(response.message)
  }
}
