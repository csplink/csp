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
 *  2025-07-28     xqyjlj       initial version
 */

import type { ContributorType } from '@/electron/types'
import path from 'node:path'
import { ipcMain } from 'electron'
import { getResourceFolder, getYamlData } from '../utils'

function getContributors(): ContributorType[] {
  const data: ContributorType[] = getYamlData(path.join(getResourceFolder(), 'contributors', 'contributors'), 'contributors', [])
  const contributors: ContributorType[] = []
  data.forEach((element) => {
    element.avatar = `local:///${path.join(getResourceFolder(), 'contributors', element.avatar)}`
    contributors.push(element)
  })
  return contributors
}

export function registerContributorsHandler() {
  ipcMain.handle('contributors:get', async (_event) => {
    return getContributors()
  })
}
