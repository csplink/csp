/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project.ts
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
 *  2025-05-21     xqyjlj       initial version
 */

import type { ProjectType } from '@/electron/types'
import fs from 'node:fs'
import { dialog } from 'electron'
import yaml from 'yaml'
import { sortObjectKeysDeep } from './convert'
import { getYamlData } from './schema'

export function checkProjectByPath(path: string): boolean {
  const data = getYamlData(path, 'project', null)
  if (!data) {
    dialog.showErrorBox('Error', 'Invalid project, please see more in log')
    return false
  }

  return true
}

export function getProject(file: string): ProjectType | null {
  const data = getYamlData(file, 'project', null)
  return data
}

export async function writeProject(file: string, project: ProjectType) {
  const wrappedData = sortObjectKeysDeep(project)
  const content = yaml.stringify(wrappedData, {
    defaultStringType: 'PLAIN',
  })
  await fs.promises.writeFile(file, content, 'utf8')
}

export async function saveProject(file: string, project: ProjectType) {
  await writeProject(file, project)
}

export async function createProject(path: string, project: ProjectType): Promise<string> {
  const name = project.name
  const folder = `${path}/${name}`
  const file = `${folder}/${name}.csp`
  await fs.promises.mkdir(folder, { recursive: true })
  await writeProject(file, project)
  return file
}
