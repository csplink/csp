<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        LogViewer.vue
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
 *  2025-10-18     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { MenuOptions } from '@imengyu/vue3-context-menu'
import type { ScrollbarInstance } from 'element-plus'
import { onMounted, onUnmounted, shallowReactive, shallowRef } from 'vue'
import { saveFileWithDialog } from '~/utils'

const logTypes = ['info', 'warn', 'error'] as const
const originalConsole: Record<string, any> = {}

const logContainer = shallowRef<HTMLDivElement>()
const scrollbarRef = shallowRef<ScrollbarInstance>()
const menuShowRef = shallowRef(false)
const menuOptionsComponentRef = shallowReactive<MenuOptions>({
  x: 0,
  y: 0,
  minWidth: 230,
})

function scrollToBottom() {
  const wrap = scrollbarRef.value?.wrapRef
  if (!wrap)
    return

  const threshold = 30
  const isAtBottom = wrap.scrollTop + wrap.clientHeight >= wrap.scrollHeight - threshold

  if (isAtBottom && !menuShowRef.value) {
    scrollbarRef.value?.setScrollTop(wrap.scrollHeight)
    scrollbarRef.value?.update()
  }
}

function handContextMenu(e: MouseEvent) {
  menuOptionsComponentRef.x = e.clientX
  menuOptionsComponentRef.y = e.clientY
  menuShowRef.value = true
}

function handSaveCommand() {
  if (logContainer.value) {
    const texts: string[] = []
    logContainer.value.childNodes.forEach((node) => {
      texts.push(node.textContent as string)
    })
    const log = texts.join('\n')
    saveFileWithDialog(log, { defaultPath: 'log.txt' })
  }
}

function handClearCommand() {
  if (logContainer.value) {
    logContainer.value.innerHTML = ''
  }
}

onMounted(() => {
  logTypes.forEach((type) => {
    originalConsole[type] = console[type] // eslint-disable-line no-console
    console[type] = (...args: any[]) => { // eslint-disable-line no-console
      originalConsole[type].apply(console, args)
      const msg = args
        .map((a) => {
          try {
            if (typeof a === 'object')
              return JSON.stringify(a, null, 2)
            return String(a)
          }
          catch {
            return String(a)
          }
        })
        .join(' ')

      const colorMap: Record<string, string> = {
        log: 'var(--ep-color-info)',
        info: 'var(--ep-color-info)',
        warn: 'var(--ep-color-warning)',
        error: 'var(--ep-color-error)',
      }

      const line = document.createElement('div')
      line.style.color = colorMap[type]
      line.style.textAlign = 'left'
      line.textContent = `[${type.toUpperCase()}] ${msg}`

      logContainer.value?.appendChild(line)
      scrollToBottom()
    }
  })
})

onUnmounted(() => {
  logTypes.forEach((type) => {
    console[type] = originalConsole[type] // eslint-disable-line no-console
  })
})
</script>

<template>
  <div class="log-div" @contextmenu="handContextMenu">
    <el-scrollbar ref="scrollbarRef" class="log-scrollbar">
      <div ref="logContainer" class="log-container" />
    </el-scrollbar>
    <context-menu
      v-model:show="menuShowRef"
      :options="menuOptionsComponentRef"
    >
      <context-menu-item icon="ri-save-line" :label="$t('command.save')" @click="handSaveCommand()" />
      <context-menu-separator />
      <context-menu-item icon="ri-eraser-line" :label="$t('command.clear')" @click="handClearCommand()" />
    </context-menu>
  </div>
</template>

<style scoped>
.log-div {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.log-scrollbar {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-scrollbar__wrap) {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-scrollbar__view) {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.log-container {
  display: flex;
  flex-direction: column;
  flex: 1;
  font-family: 'Fira Code', 'Fira Mono', Menlo, Consolas, 'DejaVu Sans Mono', monospace;
  gap: 4px;
  padding: 8px;
  border-radius: 4px;
  white-space: pre-wrap;
  user-select: text;
}
</style>
