<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CodeView.vue
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
-->

<script setup lang="ts">
import type { ThemeModeType } from '@/electron/types'
import Prism from 'prismjs'
import { nextTick, onMounted, shallowRef, watch } from 'vue'
import { getRealTheme, useThemeStore } from '~/utils'

interface PropsType {
  code: string
  language: string
}

const props = defineProps<PropsType>()

const htmlRef = shallowRef<string>('')
const codeRef = shallowRef<HTMLElement>()
const themeStore = useThemeStore()

const themeMap = {
  light: new URL('~/styles/prism/one-light.css', import.meta.url).href,
  dark: new URL('~/styles/prism/vsc-dark-plus.css', import.meta.url).href,
}

watch(() => themeStore.theme, async (theme) => {
  await setTheme(theme)
})

watch(
  () => [props.code],
  async () => {
    const language = props.language
    const grammar = Prism.languages[language] ?? Prism.languages.c
    htmlRef.value = Prism.highlight(props.code, grammar, language)
    await nextTick()
    Prism.highlightElement(codeRef.value!)
  },
  { immediate: true },
)

async function setPrismTheme(theme: 'light' | 'dark') {
  document.querySelectorAll('link[data-prism-theme], style[data-prism-theme]')
    .forEach(el => el.remove())

  const link = document.createElement('link')
  link.rel = 'stylesheet'
  link.href = themeMap[theme]
  link.setAttribute('data-prism-theme', theme)
  document.head.appendChild(link)

  await nextTick()
  updateScrollbarBackground()
}

function getPrismCodeBackground() {
  const codeEl = document.querySelector('code[class*=\'language-\']')
  if (!codeEl)
    return null
  return window.getComputedStyle(codeEl).backgroundColor
}

function updateScrollbarBackground() {
  const bg = getPrismCodeBackground()
  if (bg) {
    document.documentElement.style.setProperty('--code-bg-color', bg)
  }
}

async function setTheme(theme: ThemeModeType) {
  const actualTheme: 'light' | 'dark' = theme === 'auto' ? getRealTheme() : theme
  await setPrismTheme(actualTheme)
}

onMounted(async () => {
  await setTheme(themeStore.theme)
})
</script>

<template>
  <div class="main-div">
    <el-scrollbar class="code-view-scrollbar">
      <pre class="code-pre"><code ref="codeRef" :class="`language-${language} line-numbers match-braces rainbow-braces`" v-html="htmlRef" /></pre>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.main-div {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.code-view-scrollbar {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
  background: var(--ep-bg-color-page);
}

.code-pre {
  user-select: text;
  margin: 0;
  overflow: hidden;
  width: fit-content;
  background: var(--ep-bg-color-page);
}
</style>
