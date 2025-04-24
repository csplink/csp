/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        i18n.ts
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
 *  2025-05-07     xqyjlj       initial version
 */

import type { I18nType } from '@/electron/database'

// #region typedef

export class I18n {
  private _origin: I18nType

  constructor(origin: I18nType) {
    this._origin = origin
  }

  get origin(): I18nType {
    return this._origin
  }

  get(locale: string) {
    const defaultValue = this._origin.en
    if (locale === 'en') {
      return defaultValue
    }
    return this._origin[locale] ?? defaultValue
  }
}

// #endregion
