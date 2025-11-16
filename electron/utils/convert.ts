/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        convert.ts
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
 *  2025-07-26     xqyjlj       initial version
 */

/**
 * Sort object keys recursively.
 *
 * @param obj the object to be sorted
 * @returns the sorted object
 */

export function sortObjectKeysDeep(obj: any): any {
  if (Array.isArray(obj)) {
    return obj.map(sortObjectKeysDeep)
  }
  else if (obj && typeof obj === 'object') {
    return Object.keys(obj)
      .sort()
      .reduce((acc, key) => {
        acc[key] = sortObjectKeysDeep(obj[key])
        return acc
      }, {} as any)
  }
  return obj
}

/**
 * Extract header comments from content.
 *
 * Extracts all leading comment lines (starting with #) from the content.
 *
 * @param content the file content
 * @returns the header comments or empty string
 */
export function extractYamlHeader(content: string): string {
  const lines = content.split('\n')
  const headerLines: string[] = []

  for (const line of lines) {
    const trimmed = line.trim()
    if (trimmed.startsWith('#') || trimmed === '') {
      headerLines.push(line)
    }
    else {
      break
    }
  }

  /* !< Remove trailing empty lines from header */
  while (headerLines.length > 0 && headerLines[headerLines.length - 1].trim() === '') {
    headerLines.pop()
  }

  return headerLines.length > 0 ? `${headerLines.join('\n')}\n\n` : ''
}

/**
 * Get default YAML file header.
 *
 * Returns a default Apache License header for YAML files.
 *
 * @param filename the file name
 * @returns the default header
 */
export function getDefaultYamlHeader(filename: string): string {
  const date = new Date().toISOString().split('T')[0]
  return `# Licensed under the Apache License v. 2 (the "License")
# You may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0.html
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Copyright (C) 2025-2025 xqyjlj<xqyjlj@126.com>
#
# @author      xqyjlj
# @file        ${filename}
#
# Change Logs:
# Date           Author       Notes
# ------------   ----------   -----------------------------------------------
# ${date}     xqyjlj       initial version
#

`
}
