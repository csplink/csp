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
 *  2025-08-13     xqyjlj       initial version
 */

import type { OpenDialogOptions, OpenDialogReturnValue, SaveDialogOptions } from 'electron'
import { Buffer } from 'node:buffer'
import fs from 'node:fs'
import { dialog } from 'electron'

export async function saveFileWithDialog(content: string | ArrayBuffer, options?: SaveDialogOptions) {
  let buffer: string | Buffer
  if (typeof content === 'string') {
    buffer = content
  }
  else {
    buffer = Buffer.from(content)
  }

  const { filePath, canceled } = await dialog.showSaveDialog({
    ...options,
  })

  if (canceled || !filePath) {
    return { success: false }
  }

  try {
    await fs.promises.writeFile(filePath, buffer, 'utf8')
    return { success: true, path: filePath }
  }
  catch (error) {
    if (error instanceof Error) {
      return { success: false, message: error.message }
    }
    else {
      return { success: false, message: 'Unknown error' }
    }
  }
}

export async function showOpenDialog(options?: OpenDialogOptions): Promise<OpenDialogReturnValue> {
  return await dialog.showOpenDialog({ ...options })
}
