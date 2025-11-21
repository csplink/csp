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
import type {
  AboutDialogInstance,
  AuthorDialogInstance,
  CoderGenDumpDialogInstance,
  SaveAsProjectDialogInstance,
} from './instance'
import { MenuBar } from '@imengyu/vue3-context-menu'
import { ElNotification } from 'element-plus'
import Mousetrap from 'mousetrap'
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'
import { closeWindow, createWindow, openProject, setProjectPath, useProjectManager, useServerManager, useSettingsManager } from '~/utils'
import 'mousetrap-global-bind'

const projectManager = useProjectManager()
const severManager = useServerManager()
const router = useRouter()
const route = useRoute()
const i18n = useI18n()
const { t } = i18n
const settings = useSettingsManager()

const project = projectManager.get()!

const titleRef = ref(document.title)
const coderGenDumpDialog = ref<CoderGenDumpDialogInstance>()
const aboutDialog = ref<AboutDialogInstance>()
const authorDialog = ref<AuthorDialogInstance>()
const saveAsProjectDialog = ref<SaveAsProjectDialogInstance>()
const recentProjects = ref<string[]>([])

let titleObserver: MutationObserver
const menuData: ComputedRef<MenuBarOptions> = computed(() => ({
  theme: 'default',
  items: [
    {
      label: t('command.file'),
      icon: 'ri-file-line',
      children: [
        {
          label: t('command.new'),
          icon: 'ri-file-add-line',
          divided: true,
          shortcut: 'Ctrl + N',
          onClick: async () => {
            await handNewProject()
          },
        },
        {
          label: t('command.open'),
          icon: 'ri-folder-open-line',
          shortcut: 'Ctrl + O',
          onClick: async () => {
            await handOpenProject()
          },
        },
        {
          label: t('command.openRecent'),
          icon: 'ri-history-line',
          divided: true,
          children: recentProjects.value.map(path => ({
            label: path,
            onClick: () => {
              setProjectPath(path)
            },
          })),
        },
        {
          label: t('command.save'),
          icon: 'ri-save-line',
          shortcut: 'Ctrl + S',
          onClick: async () => {
            await handSaveProjectCommand()
          },
        },
        {
          label: t('command.saveAs'),
          icon: 'ri-save-3-line',
          divided: true,
          shortcut: 'Ctrl + Shift + S',
          onClick: async () => {
            handSaveAsProjectCommand()
          },
        },
        {
          label: t('command.generate'),
          icon: 'ri-ai-generate',
          divided: true,
          shortcut: 'Ctrl + G',
          onClick: async () => {
            await handGenerateCommand()
          },
        },
        {
          label: t('command.exit'),
          icon: 'ri-logout-box-line',
          onClick: () => {
            closeWindow()
          },
        },
      ],
    },
    {
      label: t('command.help'),
      icon: 'ri-question-line',
      children: [
        {
          label: t('command.welcome'),
          icon: 'ri-hand',
          divided: true,
          onClick: () => {
            if (!route.path.startsWith('/welcome')) {
              nextTick(() => {
                router.push('/welcome')
              })
            }
          },
        },
        { label: t('label.about'), icon: 'ri-information-line', onClick: () => { aboutDialog.value?.show() } },
        { label: t('label.author'), icon: 'ri-user-line', onClick: () => { authorDialog.value?.show() } },
      ],
    },
  ],
  zIndex: 3,
  minWidth: 230,
}))

Mousetrap.bindGlobal('ctrl+n', async () => await handNewProject())
Mousetrap.bindGlobal('ctrl+o', async () => await handOpenProject())
Mousetrap.bindGlobal('ctrl+s', async () => await handSaveProjectCommand())
Mousetrap.bindGlobal('ctrl+shift+s', () => handSaveAsProjectCommand())
Mousetrap.bindGlobal('ctrl+g', async () => await handGenerateCommand())

async function handSaveProjectCommand() {
  await project?.save()
}

function handSaveAsProjectCommand() {
  saveAsProjectDialog.value?.show()
}

async function handGenerateCommand() {
  coderGenDumpDialog.value?.show()
  coderGenDumpDialog.value?.reset()

  await project?.save()

  try {
    await severManager.server.coderGenerate(
      project.path(),
      undefined,
      [],
      (count: number, index: number, file: string) => {
        coderGenDumpDialog.value?.updateProgress(count, index, file)
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
    coderGenDumpDialog.value?.hide()
  }
}

async function handNewProject() {
  createWindow({ runMode: 'createProject', backendUrl: 'http://127.0.0.1:55432' })
}

async function handOpenProject() {
  await openProject(i18n)
}

onMounted(() => {
  titleObserver = new MutationObserver(() => {
    titleRef.value = document.title
  })

  const titleElement = document.querySelector('title')
  if (titleElement) {
    titleObserver.observe(titleElement, { childList: true })
  }

  for (const path of Object.keys(settings.settings.recentProjects)) {
    recentProjects.value.push(path)
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
  <CoderGenDumpDialog ref="coderGenDumpDialog" />
  <AboutDialog ref="aboutDialog" />
  <AuthorDialog ref="authorDialog" />
  <SaveAsProjectDialog ref="saveAsProjectDialog" />
</template>

<style>
.mx-menu-bar-item {
  height: 35px;
}
</style>
