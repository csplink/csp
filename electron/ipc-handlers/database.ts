/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        database.ts
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

import type { ClockTreeType, IpType, RepositoryType, SummaryType } from '@/electron/types'
import fs from 'node:fs'
import path from 'node:path'
import { ipcMain } from 'electron'
import yaml from 'yaml'
import {
  extractYamlHeader,
  getDefaultYamlHeader,
  getDiagramsFolder,
  getResourceFolder,
  getYamlData,
  sortObjectKeysDeep,
} from '../utils'

const pathMap = {
  DIAGRAMS_FOLDER: getDiagramsFolder(),
}

function getSummary(vendor: string, name: string): SummaryType | null {
  const data = getYamlData(path.join(getResourceFolder(), 'database', 'summary', vendor, `${name}.yml`), 'summary', null)
  return data
}

function getClockTree(vendor: string, name: string): string {
  const data = getYamlData(path.join(getResourceFolder(), 'database', 'clock', vendor, `${name}.yml`), 'clockTree', null)
  return data
}

async function saveClockTree(vendor: string, name: string, clockTree: ClockTreeType) {
  const p = path.join(getResourceFolder(), 'database', 'clock', vendor, `${name}.yml`)

  /* !< Extract or create header */
  let header = ''
  try {
    const existingContent = await fs.promises.readFile(p, 'utf8')
    header = extractYamlHeader(existingContent)
  }
  catch {
    /* !< File doesn't exist or can't be read, use default header */
  }

  if (!header) {
    header = getDefaultYamlHeader(`${name}.yml`)
  }

  const wrappedData = sortObjectKeysDeep(clockTree)
  const yamlContent = yaml.stringify(wrappedData, {
    defaultStringType: 'PLAIN',
  })

  await fs.promises.writeFile(p, header + yamlContent, 'utf8')
}

function getIp(type: string, vendor: string, name: string): IpType | null {
  const folder = path.join(getResourceFolder(), 'database', 'ip', type, vendor)
  const data = getYamlData(path.join(folder, `${name}.yml`), 'ip', null) as IpType
  if (!data?.diagrams)
    return data

  const resolveImages = (images: string[]): string[] => {
    return images.map((image) => {
      let src = image

      for (const [key, value] of Object.entries(pathMap)) {
        const pattern = new RegExp(`\\$\\{${key}\\}`, 'g')
        src = src.replace(pattern, value)
      }

      if (!path.isAbsolute(src)) {
        src = path.join(folder, src)
      }

      return `diagrams:///${src}`
    })
  }

  if (Array.isArray(data.diagrams)) {
    for (const diagram of data.diagrams) {
      diagram.content.images = resolveImages(diagram.content.images)
    }
  }
  else {
    data.diagrams.images = resolveImages(data.diagrams.images)
  }

  return data
}

function getRepository(): RepositoryType {
  const _default: RepositoryType = {
    chips: {},
    packages: {
      hal: {},
      toolchains: {},
      components: {},
    },
  }
  const data = getYamlData(path.join(getResourceFolder(), 'database', 'repository.yml'), 'repository', _default)
  return data
}

export function registerDatabaseHandler() {
  ipcMain.handle('database:getSummary', async (_event, vendor: string, name: string) => {
    return getSummary(vendor, name)
  })
  ipcMain.handle('database:getClockTree', async (_event, vendor: string, name: string) => {
    return getClockTree(vendor, name)
  })
  ipcMain.on('database:setClockTree', async (_event, vendor: string, name: string, clockTree: ClockTreeType) => {
    await saveClockTree(vendor, name, clockTree)
  })
  ipcMain.handle('database:getIp', async (_event, type: string, vendor: string, name: string) => {
    return getIp(type, vendor, name)
  })
  ipcMain.handle('database:getRepository', async (_event) => {
    return getRepository()
  })
}
