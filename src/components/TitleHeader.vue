<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TitleHeader.vue
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
 *  2025-04-25     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { MenuBarOptions } from '@imengyu/vue3-context-menu'
import { MenuBar } from '@imengyu/vue3-context-menu'
import Mousetrap from 'mousetrap'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProjectManager } from '~/database'
import { useTitleMenuStore } from '~/store/titleMenu'
import 'mousetrap-global-bind'

const titleMenu = useTitleMenuStore()
const projectManager = useProjectManager()
const { t } = useI18n()

const showRef = ref<boolean>(titleMenu.show)
const titleRef = ref(document.title)
let titleObserver: MutationObserver
const menuData: MenuBarOptions = {
  theme: 'default',
  items: [
    {
      label: t('titleHeader.file'),
      children: [
        { label: t('titleHeader.fileNew'), divided: true, shortcut: 'Ctrl + N' },
        { label: t('titleHeader.fileOpen'), shortcut: 'Ctrl + O' },
        {
          label: t('titleHeader.fileOpenRecent'),
          divided: true,
          children: [
          ],
          onSubMenuOpen(_itemInstance) {
          },
        },
        { label: t('titleHeader.fileSave'), shortcut: 'Ctrl + S', onClick: () => saveProject() },
        { label: t('titleHeader.fileSaveAs'), divided: true, shortcut: 'Ctrl + Shift + S' },
        { label: t('titleHeader.fileGenerate'), divided: true, shortcut: 'Ctrl + G' },
        { label: t('titleHeader.fileExit') },
      ],
      onSubMenuOpen(_itemInstance) {
      },
    },
    {
      label: 'Edit',
      children: [
        { label: 'Undo' },
        { label: 'Redo' },
        { label: 'Cut', divided: true },
        { label: 'Copy' },
        { label: 'Find', divided: true },
        { label: 'Replace' },
      ],
    },
    {
      label: 'View',
      children: [
        { label: 'Zoom in' },
        { label: 'Zoom out' },
        { label: 'Reset zoom' },
        { label: 'Full screent', divided: true },
        { label: 'Find', divided: true },
        { label: 'Replace' },
      ],
    },
    {
      label: 'Help',
      children: [
        { label: 'About' },
      ],
    },
  ],
  iconFontClass: 'iconfont',
  customClass: 'class-a',
  zIndex: 3,
  minWidth: 230,
}

Mousetrap.bindGlobal('ctrl+s', () => saveProject())

Mousetrap.bindGlobal('ctrl+shift+s', () => {
})

function saveProject() {
  const project = projectManager.get()
  project?.save()
}

onMounted(() => {
  titleObserver = new MutationObserver(() => {
    titleRef.value = document.title
  })

  const titleElement = document.querySelector('title')
  if (titleElement) {
    titleObserver.observe(titleElement, { childList: true })
  }
})

onBeforeUnmount(() => {
  if (titleObserver) {
    titleObserver.disconnect()
  }
})
</script>

<template>
  <div class="window-titlebar window-title-drag">
    <div class="window-title-drag window-title-left flex items-center justify-center">
      <el-image class="window-title-drag window-app-icon" style="width: 18px; height: 18px" src="/images/logo.svg" />
      <template v-if="showRef">
        <div class="window-title-no-drag">
          <MenuBar :options="menuData" />
        </div>
      </template>
    </div>
    <div class="window-title-drag window-title-center">
      {{ titleRef }}
    </div>
    <div class="window-title-drag draggable-area" />
    <div class="window-title-no-drag window-controls-container" />
  </div>
</template>

<style lang="scss" scoped>
.window-titlebar {
  height: 35px;
  background: var(--ep-menu-bg-color);
  display: flex;
  align-items: center;
  flex-shrink: 0;
  border-bottom: 1px solid var(--ep-menu-border-color);
}

.window-title-drag {
  -webkit-app-region: drag;
}

.window-title-no-drag {
  -webkit-app-region: no-drag;
}

.window-title-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  min-width: max-content;
}

.window-app-icon {
  padding: 0px 9px;
}

.window-title-center {
  flex: 1;
  text-align: center;
  color: var(--ep-text-color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.draggable-area {
  flex: 0;
}

.window-controls-container {
  width: 150px;
  flex-shrink: 0;
}

::v-deep(.mx-menu-bar-content) {
  align-items: center;
  display: flex;
}

::v-deep(.mx-menu-bar-item) {
  display: flex;
  align-items: center;
  padding-top: 5px;
}
</style>
