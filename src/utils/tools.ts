/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        tools.ts
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
 *  2025-08-10     xqyjlj       initial version
 */

/**
 * Check if two arrays are equal.
 *
 * @param a - the first array.
 * @param b - the second array.
 * @returns true if the two arrays are equal, false otherwise.
 */
export function arrayEqual<T>(a: T[], b: T[]): boolean {
  if (a.length !== b.length)
    return false

  const setA = new Set(a)
  const setB = new Set(b)
  if (setA.size !== setB.size)
    return false

  for (const val of setA) {
    if (!setB.has(val))
      return false
  }

  return true
}
