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

import type {
  ContributorType,
  IpType,
  ProjectType,
  SummaryType,
} from '@/electron/database'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { app, ipcMain } from 'electron'
import yaml, { Scalar } from 'yaml'
import {
  getProjectPath,
} from '../database'
import { validateDataBySchema } from '../utils'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const __root = path.join(__dirname, '..')
const __resourcePath = app.isPackaged ? process.resourcesPath : path.join(__root, 'resources')
const __specialWords = new Set(['yes', 'no', 'on', 'off'])

function getJsonData(file: string, schema: string, _default: any) {
  if (!fs.existsSync(file)) {
    console.error(`The file '${file}' is not exits.`)
    return _default
  }

  const content = fs.readFileSync(file, 'utf-8')
  const parsedData = JSON.parse(content)
  const result = validateDataBySchema(__resourcePath, parsedData, schema)
  if (!result.result) {
    console.error(`Failed to load file '${file}'`)
    console.error(result.errors)
    return _default
  }
  return parsedData
}

function getYamlData(file: string, schema: string, _default: any) {
  if (!fs.existsSync(file)) {
    console.error(`The file '${file}' is not exits.`)
    return _default
  }

  const content = fs.readFileSync(file, 'utf-8')
  const parsedData = yaml.parse(content)
  const result = validateDataBySchema(__resourcePath, parsedData, schema)
  if (!result.result) {
    console.error(`Failed to load file '${file}'`)
    console.error(result.errors)
    return _default
  }
  return parsedData
}

function getContributors(): ContributorType[] {
  const data: ContributorType[] = getJsonData(path.join(__resourcePath, 'contributors', 'contributors'), 'contributors', [])
  const contributors: ContributorType[] = []
  data.forEach((element) => {
    element.avatar = `local:///${path.join(__resourcePath, 'contributors', element.avatar)}`
    contributors.push(element)
  })
  return contributors
}

function getSummary(vendor: string, name: string): SummaryType | null {
  const data = getYamlData(path.join(__resourcePath, 'database', 'summary', vendor, `${name}.yml`), 'summary', null)
  return data
}

function getClockTree(vendor: string, name: string): string {
  const basePath = path.join(__resourcePath, 'database', 'clock', vendor)
  const svg = fs.readFileSync(path.join(basePath, `${name}.svg`), 'utf-8')

  return svg
}

function getIp(type: string, vendor: string, name: string): IpType | null {
  const data = getYamlData(path.join(__resourcePath, 'database', 'ip', type, vendor, `${name}.yml`), 'ip', null)
  return data
}

function getProject(): ProjectType | null {
  const data = getYamlData(getProjectPath(), 'project', null)
  return data
}

function sortKeysDeep(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(sortKeysDeep)
  }
  else if (obj && typeof obj === 'object') {
    return Object.keys(obj)
      .sort()
      .reduce((acc, key) => {
        acc[key] = sortKeysDeep(obj[key])
        return acc
      }, {} as any)
  }
  return obj
}

/**
 * Wrap special strings with single quote.
 *
 * In YAML, words like 'yes', 'no', 'on', 'off' are special strings that
 * cannot be used as keys directly. This function wraps these words with
 * single quotes to make them valid.
 *
 * @param obj the object to be wrapped
 * @returns the wrapped object
 */
function wrapSpecialStrings(obj: any): any {
  if (typeof obj === 'string') {
    if (__specialWords.has(obj.toLowerCase())) {
      const scalar = new Scalar(obj)
      scalar.type = 'QUOTE_SINGLE'
      return scalar
    }
    return obj
  }
  else if (Array.isArray(obj)) {
    return obj.map(wrapSpecialStrings)
  }
  else if (obj && typeof obj === 'object') {
    const result: Record<string, any> = {}
    for (const key in obj) {
      result[key] = wrapSpecialStrings(obj[key])
    }
    return result
  }
  return obj
}

function saveProject(project: ProjectType) {
  const projectPath = getProjectPath()
  if (projectPath) {
    const wrappedData = wrapSpecialStrings(sortKeysDeep(project))
    const content = yaml.stringify(wrappedData, {
      defaultStringType: 'PLAIN',
    })
    fs.writeFileSync(projectPath, content, 'utf8')
  }
}

export function registerDatabaseHandler() {
  ipcMain.handle('database:getContributors', async (_event) => {
    return getContributors()
  })
  ipcMain.handle('database:getSummary', async (_event, vendor: string, name: string) => {
    return getSummary(vendor, name)
  })
  ipcMain.handle('database:getClockTree', async (_event, vendor: string, name: string) => {
    return getClockTree(vendor, name)
  })
  ipcMain.handle('database:getIp', async (_event, type: string, vendor: string, name: string) => {
    return getIp(type, vendor, name)
  })
  ipcMain.handle('database:getProject', async (_event) => {
    return getProject()
  })
  ipcMain.handle('database:getProjectPath', async (_event) => {
    return getProjectPath()
  })
  ipcMain.on('database:saveProject', async (_event, project: ProjectType) => {
    saveProject(project)
  })
}
