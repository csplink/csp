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

export interface ProjectType {
  version: string
  name: string
  vendor: string
  targetChip: string
  configs?: {
    [k: string]: unknown
  }
  modules?: string[]
  gen?: ProjectGenType
}

export interface ProjectGenType {
  copyLibrary?: boolean
  linker?: ProjectGenLinkerType
  useToolchainsPackage?: boolean
  hal: string
  halVersion?: string
  builder: string
  builderVersion?: string
  toolchains: string
  toolchainsVersion?: string
}

export interface ProjectGenLinkerType {
  defaultHeapSize?: number
  defaultStackSize?: number
}

let _projectPath = ''

export function setProjectPath(path: string) {
  _projectPath = path
}

export function getProjectPath(): string {
  return _projectPath
}
