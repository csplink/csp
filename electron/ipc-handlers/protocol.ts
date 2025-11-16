/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        protocol.ts
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
 *  2025-04-29     xqyjlj       initial version
 */

import { readFile } from 'node:fs/promises'
import { pathToFileURL } from 'node:url'
import { net, protocol } from 'electron'
import { getRealTheme } from '../utils'

export function registerProtocolHandler() {
  protocol.handle('local', (request) => {
    const filePath = request.url.slice('local:///'.length)
    return net.fetch(pathToFileURL(filePath).toString())
  })

  protocol.handle('diagrams', async (request) => {
    const urlWithoutProtocol = decodeURIComponent(request.url.slice('diagrams:///'.length))
    const [filePath, queryString] = urlWithoutProtocol.split('?')
    const params: Record<string, string> = {}
    if (queryString) {
      queryString.split('&').forEach((pair) => {
        const [key, value] = pair.split('=')
        if (key)
          params[key] = value ?? ''
      })
    }
    const theme = params.theme ?? 'auto'

    let data = await readFile(filePath, 'utf-8')

    if (filePath.endsWith('.svg')) {
      const actualTheme = theme === 'auto' ? getRealTheme() : theme
      const color = actualTheme === 'dark' ? '#e5eaf3' : '#303133'

      data = data.replace(/rgb\s*\(\s*0\s*,\s*0\s*,\s*0\s*\)/gi, color)

      return new Response(data, {
        headers: { 'Content-Type': 'image/svg+xml' },
      })
    }

    return net.fetch(pathToFileURL(filePath).toString())
  })
}
