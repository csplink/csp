/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        index.ts
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

import type { I18nModeType, I18nType } from '@/electron/types'
import type { useI18n } from 'vue-i18n'
import { createI18n } from 'vue-i18n'
import en from './langs/en'
import zhCN from './langs/zh-cn'

const i18n = createI18n({
  legacy: false,
  globalInjection: true,
  locale: 'zh-cn',
  fallbackLocale: 'en',
  messages: {
    'zh-cn': zhCN,
    'en': en,
  },
})

export type VueI18nType = typeof i18n
export type UseI18nType = ReturnType<typeof useI18n<unknown, string>>
export default i18n

export function applyLocale(language: I18nModeType, vi18n: VueI18nType) {
  if (vi18n) {
    vi18n.global.locale.value = language
  }
}

export function getLocale(vi18n: VueI18nType): string {
  return vi18n.global.locale.value
}

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
    if (!this._origin[locale]) {
      if (defaultValue !== '') {
        console.warn(`Locale '${locale}' not found in`, this._origin)
      }
      return defaultValue
    }
    return this._origin[locale]
  }
}

// #endregion
