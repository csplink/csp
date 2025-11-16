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
 *  2025-07-10     xqyjlj       initial version
 */

import type { ProjectType } from '@/electron/types'
import type { Socket } from 'socket.io-client'
import type { App } from 'vue'
import type { PackageDescriptionType, PackageIndexType } from './packages'
import { io } from 'socket.io-client'
import { inject } from 'vue'

// #region typedef

export interface CoderDumpResponseType {
  files: {
    [k: string]: {
      content: string
      diff?: string
    }
  }
}

export interface PackageIndexResponseType {
  [kind: string]: {
    [name: string]: {
      [version: string]: string
    }
  }
}

export class Server {
  private _url: string
  private _socket: Socket

  constructor(url: string) {
    this._url = url
    this._socket = io(url)
  }

  get url(): string {
    return this._url
  }

  get socket(): Socket {
    return this._socket
  }

  async coderDump(
    content: ProjectType | null,
    path: string,
    diff: boolean,
    onProgress?: (count: number, index: number, file: string) => void,
  ): Promise<CoderDumpResponseType> {
    return new Promise((resolve, reject) => {
      const socket = this._socket
      if (onProgress) {
        socket.on('coder/dump.progress', (data: { count: number, index: number, file: string }) => {
          onProgress(data.count, data.index, data.file)
        })
      }

      socket.emit('sio/coder/dump', {
        content,
        path,
        diff,
      })

      socket.once('coder/dump.result', (response: { success: boolean, error?: string, result?: CoderDumpResponseType }) => {
        if (onProgress) {
          socket.off('coder/dump.progress')
        }

        if (response.success) {
          resolve(response.result!)
        }
        else {
          console.error(`Failed to coder dump: ${response.error}`)
          reject(new Error(response.error))
        }
      })
    })
  }

  async coderGenerate(
    path: string,
    output?: string,
    files?: string[],
    onProgress?: (count: number, index: number, file: string) => void,
    timeout = 2000,
  ): Promise<boolean> {
    const socket = this._socket
    return new Promise((resolve, reject) => {
      let timeoutId: ReturnType<typeof setTimeout> | null = null

      if (onProgress) {
        socket.on('coder/generate.progress', (data: { count: number, index: number, file: string }) => {
          onProgress(data.count, data.index, data.file)
        })
      }

      timeoutId = setTimeout(() => {
        if (onProgress) {
          socket.off('coder/generate.progress')
        }
        socket.off('coder/generate.result')
        reject(new Error(`coderGenerate timeout after ${timeout}ms`))
      }, timeout)

      socket.emit('sio/coder/generate', {
        path,
        output,
        files,
      })

      socket.once('coder/generate.result', (response: { success: boolean, error?: string }) => {
        if (timeoutId) {
          clearTimeout(timeoutId)
        }
        if (onProgress) {
          socket.off('coder/generate.progress')
        }

        if (response.success) {
          resolve(true)
        }
        else {
          console.error(`Failed to coder generate: ${response.error}`)
          reject(new Error(response.error))
        }
      })
    })
  }

  async packageList(): Promise<PackageIndexType> {
    return new Promise((resolve, reject) => {
      this._socket.emit('sio/package/list')

      this._socket.once('package/list.result', (response: { success: boolean, error?: string, result?: PackageIndexType }) => {
        if (response.success) {
          resolve(response.result!)
        }
        else {
          console.error(`Failed to get package list: ${response.error}`)
          reject(new Error(response.error))
        }
      })
    })
  }

  async getPackageDescription(type: string, name: string, version: string): Promise<PackageDescriptionType> {
    return new Promise((resolve, reject) => {
      this._socket.emit('sio/package/description', { kind: type, name, version })

      this._socket.once('package/description.result', (response: {
        success: boolean
        error?: string
        result?: PackageDescriptionType
      }) => {
        if (response.success) {
          resolve(response.result!)
        }
        else {
          console.error(`Failed to get package description: ${response.error}`)
          reject(new Error(response.error))
        }
      })
    })
  }
}

// #endregion

export class ServerManager {
  private _server: Server | null = null

  async init() {
    const url = await window.electron.invoke('server:getUrl')
    this._server = new Server(url)
  }

  get server(): Server {
    return this._server!
  }
}

export function createServerManagerPlugin() {
  const manager = new ServerManager()

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('utils@serverManager', manager)
      },
    },
    async init() {
      await manager.init()
    },
  }
}

export function useServerManager(): ServerManager {
  return inject('utils@serverManager')!
}
