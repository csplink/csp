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
 *  2025-05-14     xqyjlj       initial version
 */

import path, { dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { generateContributors } from '../electron/database/contributors'

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)
const ROOT_DIR = path.join(__dirname, '..')
const OWNER = 'csplink'
const REPO = 'csp'
const TOKEN = process.env.GITHUB_CSPLINK_DEVELOPER_TOKEN || 'None'

generateContributors(ROOT_DIR, OWNER, REPO, TOKEN).catch(console.error)
