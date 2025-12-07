/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        contributors.ts
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
 *  2025-04-27     xqyjlj       initial version
 */

import type { ContributorType } from '@/electron/types'
import type { App } from 'vue'
import { inject, markRaw } from 'vue'

// #region typedef

export class Contributor {
  private _origin: ContributorType

  constructor(origin: ContributorType) {
    this._origin = origin
  }

  get origin(): ContributorType {
    return this._origin
  }

  get avatar(): string {
    return this._origin.avatar
  }

  get contributions(): number {
    return this._origin.contributions
  }

  get htmlUrl(): string {
    return this._origin.htmlUrl
  }

  get name(): string {
    return this._origin.name
  }
}

// #endregion

export class ContributorManager {
  private _contributors?: Contributor[]

  private async _get(): Promise<Contributor[]> {
    const content = await window.electron.invoke('contributors:get') as ContributorType[]
    const contributors: Contributor[] = []
    content.forEach((element) => {
      contributors.push(new Contributor (element))
    })

    return contributors
  }

  async get(): Promise<Contributor[]> {
    return this._contributors ??= markRaw(await this._get())
  }
}

export function createContributorManagerPlugin() {
  const manager = new ContributorManager()

  return {
    manager,
    plugin: {
      install(app: App) {
        app.provide('utils@contributorManager', manager)
      },
    },
  }
}

export function useContributorManager(): ContributorManager {
  return inject('utils@contributorManager')!
}
