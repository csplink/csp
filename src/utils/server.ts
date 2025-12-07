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
import type { SioCoderDumpResponseFile } from '~/proto/sio_coder_dump'
import { io } from 'socket.io-client'
import { inject, markRaw } from 'vue'
import { SioCoderDumpProgress, SioCoderDumpRequest, SioCoderDumpResponse } from '~/proto/sio_coder_dump'
import { SioCoderGenerateProgress, SioCoderGenerateRequest, SioCoderGenerateResponse } from '~/proto/sio_coder_generate'
import { SioPackageDescriptionRequest, SioPackageDescriptionResponse } from '~/proto/sio_package_description'
import { SioPackageInstallProgress, SioPackageInstallRequest, SioPackageInstallResponse } from '~/proto/sio_package_install'
import { SioPackageListResponse } from '~/proto/sio_package_list'
import { SioPackageUninstallRequest, SioPackageUninstallResponse } from '~/proto/sio_package_uninstall'

// #region typedef

export interface CoderDumpResponseType {
  [k: string]: SioCoderDumpResponseFile
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
        socket.on('coder/dump.progress', (progress: ArrayBuffer) => {
          const req = SioCoderDumpProgress.decode(new Uint8Array(progress))
          onProgress(req.count, req.index, req.file)
        })
      }

      const req = SioCoderDumpRequest.fromPartial({
        content: content as any,
        path,
        diff,
      })

      const buf = SioCoderDumpRequest.encode(req).finish()
      socket.emit('sio/coder/dump', buf)

      socket.once('coder/dump.result', (response: ArrayBuffer) => {
        if (onProgress) {
          socket.off('coder/dump.progress')
        }
        const resp = SioCoderDumpResponse.decode(new Uint8Array(response))
        if (resp.success) {
          resolve(resp.files)
        }
        else {
          console.error(`Failed to coder dump: ${resp.error}`)
          reject(new Error(resp.error))
        }
      })
    })
  }

  async coderGenerate(
    path: string,
    output?: string,
    files?: string[],
    onProgress?: (count: number, index: number, file: string, write: boolean) => void,
    timeout = 2000,
  ): Promise<boolean> {
    const socket = this._socket
    return new Promise((resolve, reject) => {
      let timeoutId: ReturnType<typeof setTimeout> | null = null

      if (onProgress) {
        socket.on('coder/generate.progress', (progress: ArrayBuffer) => {
          const req = SioCoderGenerateProgress.decode(new Uint8Array(progress))
          onProgress(req.count, req.index, req.file, req.write)
        })
      }

      timeoutId = setTimeout(() => {
        if (onProgress) {
          socket.off('coder/generate.progress')
        }
        socket.off('coder/generate.result')
        reject(new Error(`coderGenerate timeout after ${timeout}ms`))
      }, timeout)

      const req = SioCoderGenerateRequest.fromPartial({
        path,
        output,
        files,
      })

      const buf = SioCoderGenerateRequest.encode(req).finish()
      socket.emit('sio/coder/generate', buf)

      socket.once('coder/generate.result', (response: ArrayBuffer) => {
        if (timeoutId) {
          clearTimeout(timeoutId)
        }
        if (onProgress) {
          socket.off('coder/generate.progress')
        }

        const resp = SioCoderGenerateResponse.decode(new Uint8Array(response))
        if (resp.success) {
          resolve(true)
        }
        else {
          console.error(`Failed to coder generate: ${resp.error}`)
          reject(new Error(resp.error))
        }
      })
    })
  }

  async packageList(): Promise<PackageIndexType> {
    return new Promise((resolve, reject) => {
      this._socket.emit('sio/package/list')

      this._socket.once('package/list.result', (response: ArrayBuffer) => {
        const resp = SioPackageListResponse.decode(new Uint8Array(response))
        if (resp.success) {
          resolve(resp.packages!)
        }
        else {
          console.error(`Failed to get package list: ${resp.error}`)
          reject(new Error(resp.error))
        }
      })
    })
  }

  async getPackageDescription(type: string, name: string, version: string): Promise<PackageDescriptionType> {
    return new Promise((resolve, reject) => {
      const req = SioPackageDescriptionRequest.fromPartial({
        type,
        name,
        version,
      })

      const buf = SioPackageDescriptionRequest.encode(req).finish()
      this._socket.emit('sio/package/description', buf)

      this._socket.once('package/description.result', (response: ArrayBuffer) => {
        const resp = SioPackageDescriptionResponse.decode(new Uint8Array(response))
        if (resp.success) {
          resolve(resp.description! as PackageDescriptionType)
        }
        else {
          console.error(`Failed to get package description: ${resp.error}`)
          reject(new Error(resp.error))
        }
      })
    })
  }

  async packageInstall(
    path: string,
    onProgress?: (count: number, index: number, file: string) => void,
  ): Promise<PackageDescriptionType> {
    return new Promise((resolve, reject) => {
      if (onProgress) {
        this._socket.on('package/install.progress', (progress: ArrayBuffer) => {
          const req = SioPackageInstallProgress.decode(new Uint8Array(progress))
          onProgress(req.count, req.index, req.file)
        })
      }

      const req = SioPackageInstallRequest.fromPartial({
        path,
      })

      const buf = SioPackageInstallRequest.encode(req).finish()
      this._socket.emit('sio/package/install', buf)

      this._socket.once('package/install.result', (response: ArrayBuffer) => {
        if (onProgress) {
          this._socket.off('package/install.progress')
        }

        const resp = SioPackageInstallResponse.decode(new Uint8Array(response))
        if (resp.success) {
          resolve(resp.description as PackageDescriptionType)
        }
        else {
          console.error(`Failed to install package: ${resp.error}`)
          reject(new Error(resp.error))
        }
      })
    })
  }

  async packageUninstall(type: string, name: string, version: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      const req = SioPackageUninstallRequest.fromPartial({
        type,
        name,
        version,
      })

      const buf = SioPackageUninstallRequest.encode(req).finish()
      this._socket.emit('sio/package/uninstall', buf)

      this._socket.once('package/uninstall.result', (response: ArrayBuffer) => {
        const resp = SioPackageUninstallResponse.decode(new Uint8Array(response))
        if (resp.success) {
          resolve(true)
        }
        else {
          console.error(`Failed to get package description: ${resp.error}`)
          reject(new Error(resp.error))
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
    this._server = markRaw(new Server(url))
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
