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
 *  2025-05-20     xqyjlj       initial version
 */

import * as fs from 'node:fs'
import path, { dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { parse } from 'yaml'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const ROOT_DIR = path.join(__dirname, '..')
const SCHEMA_DIR = path.join(ROOT_DIR, 'resources', 'database', 'schema')

function convertYamlToJson() {
  if (!fs.existsSync(SCHEMA_DIR)) {
    console.error(`Directory does not exist: ${SCHEMA_DIR}`)
    return
  }

  const files = fs.readdirSync(SCHEMA_DIR)

  files.forEach((file) => {
    if (file.endsWith('.yml')) {
      const yamlPath = path.join(SCHEMA_DIR, file)
      const jsonPath = path.join(SCHEMA_DIR, file.replace('.yml', '.json'))

      try {
        const yamlContent = fs.readFileSync(yamlPath, 'utf8')
        const jsonObj = parse(yamlContent)
        const jsonContent = JSON.stringify(jsonObj, null, 2)
        fs.writeFileSync(jsonPath, jsonContent, 'utf8')

        // eslint-disable-next-line no-console
        console.info(`Successfully converted: ${file} -> ${path.basename(jsonPath)}`)
      }
      catch (error) {
        console.error(`Error converting file ${file}:`, error)
      }
    }
  })
}

convertYamlToJson()
