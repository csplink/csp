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

import type { ProjectType } from '@/electron/database'
import axios from 'axios'

export interface CoderDumpResponseType {
  files: {
    [k: string]: {
      content: string
      diff?: string
    }
  }
}

export async function coderDump(content: ProjectType | null, path: string, diff: boolean): Promise<CoderDumpResponseType> {
  const response = await axios.post('http://127.0.0.1:5000/api/coder/dump', {
    content,
    path,
    diff,
  })

  return response.data
}
