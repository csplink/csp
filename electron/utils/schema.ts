/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        schema.ts
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
 *  2025-05-06     xqyjlj       initial version
 */

import type { ErrorObject } from 'ajv'
import fs from 'node:fs'
import path from 'node:path'
import Ajv from 'ajv'
import yaml from 'yaml'
import { getResourceFolder } from './settings'

export function validateDataBySchema(folder: string, data: any, schema: string): { result: boolean, errors?: ErrorObject[] | null } {
  const content = fs.readFileSync(path.join(folder, 'database', 'schema', `${schema}.yml`), 'utf-8')
  const parsedData = yaml.parse(content)
  const ajv = new Ajv()
  const validate = ajv.compile(parsedData)
  const result = validate(data)
  const errors = validate.errors
  return { result, errors }
}

export function getJsonData(file: string, schema: string, _default: any) {
  if (!fs.existsSync(file)) {
    console.error(`The file '${file}' is not exits.`)
    return _default
  }

  const content = fs.readFileSync(file, 'utf-8')
  const parsedData = JSON.parse(content)
  const result = validateDataBySchema(getResourceFolder(), parsedData, schema)
  if (!result.result) {
    console.error(`Failed to load file '${file}'`)
    console.error(result.errors)
    return _default
  }
  return parsedData
}

export function getYamlData(file: string, schema: string, _default: any) {
  if (!fs.existsSync(file)) {
    console.error(`The file '${file}' is not exits.`)
    return _default
  }

  const content = fs.readFileSync(file, 'utf-8')
  const parsedData = yaml.parse(content)
  const result = validateDataBySchema(getResourceFolder(), parsedData, schema)
  if (!result.result) {
    console.error(`Failed to load file '${file}'`)
    console.error(result.errors)
    return _default
  }
  return parsedData
}
