/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        server.ts
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
 *  2025-10-20     xqyjlj       initial version
 */

import type { Buffer } from 'node:buffer'
import { spawn } from 'node:child_process'
import axios from 'axios'
import { app } from 'electron'
import { processArgs } from './args'
import { getServerFolder } from './settings'

export function clientOnline(url: string) {
  if (!app.isPackaged) {
    return
  }

  axios.get(`${url}/api/client/online`, { params: { id: process.pid } })
    .then(() => {
    })
    .catch((error) => {
      console.error('clientOnline Error:', error.message)
    })
}

export function clientOffline(url: string) {
  if (!app.isPackaged) {
    return
  }

  axios.get(`${url}/api/client/offline`, { params: { id: process.pid } })
    .then(() => {
    })
    .catch((error) => {
      if (axios.isAxiosError(error)) {
        if (error.code === 'ECONNRESET') {
          /* !< 服务端已经断开 */
          return
        }
      }
      console.error('clientOffline Error:', error.message)
    })
}

export function createServer(): Promise<string> {
  return new Promise((resolve, reject) => {
    if (!app.isPackaged) {
      resolve(processArgs.backendUrl)
      return
    }

    try {
      const process = spawn('csp-server.exe', ['serve', '-p', '55432'], {
        cwd: getServerFolder(),
      })

      let resolved = false

      const timeout = setTimeout(() => {
        if (!resolved) {
          resolved = true
          reject(new Error('Server startup timeout after 5s'))
          process.kill()
        }
      }, 5000)

      process.stderr!.once('data', async (data: Buffer) => {
        const text = data.toString()
        const match = text.match(/http:\/\/127\.0\.0\.1:(\d+)/)
        if (match) {
          const url = match[0]
          resolved = true
          clearTimeout(timeout)
          /* !< 延时 1s 等待服务端真正启动 */
          await new Promise(r => setTimeout(r, 1000))
          clientOnline(url)
          resolve(url)
        }
      })

      process.once('error', (err) => {
        if (!resolved) {
          resolved = true
          clearTimeout(timeout)
          reject(err)
        }
      })

      process.once('exit', (code) => {
        if (!resolved) {
          resolved = true
          clearTimeout(timeout)
          reject(new Error(`Server exited with code ${code}`))
        }
      })
    }
    catch (error) {
      reject(error)
    }
  })
}
