/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        theme.ts
 *  @brief       Theme management utility for CSP application
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

import type { ThemeModeType } from '@/electron/types/theme'
import { useDark } from '@vueuse/core'
import { defineStore } from 'pinia'
import { nextTick } from 'vue'

const isDark = useDark()

export const useThemeStore = defineStore('TitleMenu', {
  state: () => {
    return {
      theme: 'auto' as ThemeModeType,
      themeColor: '#409eff',
    }
  },
})

export function applyTheme(theme: ThemeModeType) {
  const themeStore = useThemeStore()
  let actualTheme: 'light' | 'dark'
  if (theme === 'auto') {
    actualTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
  }
  else {
    actualTheme = theme
  }

  isDark.value = actualTheme === 'dark'

  const root = document.documentElement
  nextTick(() => {
    const color = getComputedStyle(root).getPropertyValue('--ep-bg-color-page').trim()
    const symbolColor = getComputedStyle(root).getPropertyValue('--ep-text-color-primary').trim()
    window.electron.send('theme:set', {
      color,
      symbolColor,
    })
    themeStore.theme = actualTheme
  })
}

export function applyThemeColor(color: string) {
  const themeStore = useThemeStore()
  const root = document.documentElement
  root.style.setProperty('--ep-color-primary', color)
  themeStore.themeColor = color
}

export function getTextColorPrimary(): string {
  const root = document.documentElement
  return getComputedStyle(root).getPropertyValue('--ep-text-color-primary').trim()
}

export function getRealTheme(): 'light' | 'dark' {
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}
