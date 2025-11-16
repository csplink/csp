<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TitleMenuBar.vue
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
 *  2025-08-12     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { MenuBarOptions } from '@imengyu/vue3-context-menu'
import type { ComputedRef } from 'vue'
import type { CoderGenDumpDialogInstance } from './instance'
import { MenuBar } from '@imengyu/vue3-context-menu'
import { ElNotification } from 'element-plus'
import Mousetrap from 'mousetrap'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useProjectManager, useServerManager } from '~/utils'
import 'mousetrap-global-bind'

const projectManager = useProjectManager()
const severManager = useServerManager()
const { t } = useI18n()

const project = projectManager.get()!

const titleRef = ref(document.title)
const dialog = ref<CoderGenDumpDialogInstance>()
let titleObserver: MutationObserver
const menuData: ComputedRef<MenuBarOptions> = computed(() => ({
  theme: 'default',
  items: [
    {
      label: t('command.file'),
      icon: 'ri-file-line',
      children: [
        { label: t('command.new'), icon: 'ri-file-add-line', divided: true, shortcut: 'Ctrl + N' },
        { label: t('command.open'), icon: 'ri-folder-open-line', shortcut: 'Ctrl + O' },
        {
          label: t('command.openRecent'),
          icon: 'ri-history-line',
          divided: true,
          children: [
          ],
          onSubMenuOpen(_itemInstance) {
          },
        },
        { label: t('command.save'), icon: 'ri-save-line', shortcut: 'Ctrl + S', onClick: () => handSaveProjectCommand() },
        { label: t('command.saveAs'), icon: 'ri-save-3-line', divided: true, shortcut: 'Ctrl + Shift + S' },
        { label: t('command.generate'), icon: 'ri-ai-generate', divided: true, shortcut: 'Ctrl + G', onClick: () => handGenerateCommand() },
        { label: t('command.exit'), icon: 'ri-logout-box-line' },
      ],
      onSubMenuOpen(_itemInstance) {
      },
    },
    {
      label: 'Help',
      icon: 'ri-question-line',
      children: [
        { label: 'Welcome', icon: 'ri-hand-heart-line', divided: true },
        { label: 'About', icon: 'ri-information-line' },
        { label: 'License', icon: 'ri-copyleft-line' },
      ],
    },
  ],
  customClass: 'class-a',
  zIndex: 3,
  minWidth: 230,
}))

Mousetrap.bindGlobal('ctrl+s', () => handSaveProjectCommand())
Mousetrap.bindGlobal('ctrl+shift+s', () => {})
Mousetrap.bindGlobal('ctrl+g', () => handGenerateCommand())

async function handSaveProjectCommand() {
  await project?.save()
}

async function handGenerateCommand() {
  dialog.value?.show()
  dialog.value?.reset()

  await project?.save()

  try {
    await severManager.server.coderGenerate(
      project.path(),
      undefined,
      [],
      (count: number, index: number, file: string) => {
        dialog.value?.updateProgress(count, index, file)
      },
    ).then(() => {
      ElNotification({
        title: t('label.success'),
        message: t('message.generateSuccess'),
        duration: 3000,
        offset: 35,
        type: 'success',
      })
    })
  }
  catch (error) {
    console.error(t('message.generateFailed'), error)
    ElNotification({
      title: t('label.error'),
      message: t('message.generateFailed'),
      duration: 0,
      offset: 35,
      type: 'error',
    })
  }
  finally {
    dialog.value?.hide()
  }
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

defineExpose({
  generate: handGenerateCommand,
})
</script>

<template>
  <MenuBar :options="menuData" />
  <CoderGenDumpDialog ref="dialog" />
</template>

<style lang="scss" scoped>
</style>
