<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        index.vue
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
 *  2025-07-06     xqyjlj       initial version
-->
<script setup lang="ts">
import type { FileProgressDialogInstance } from '~/components/instance'
import type { CoderDumpResponseType } from '~/utils'
import { ElNotification } from 'element-plus'
import JSZip from 'jszip'
import { onMounted, ref, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute } from 'vue-router'
import { saveFileWithDialog, useProjectManager, useServerManager } from '~/utils'

const projectManager = useProjectManager()
const severManager = useServerManager()
const route = useRoute()
const { t } = useI18n()

const project = projectManager.get()!

const codeRef = shallowRef<string>('')
const languageRef = shallowRef('c')
const coderDumpResponseRef = shallowRef<CoderDumpResponseType>()
const fileTreeModelRef = ref<Record<string, boolean>>({})
const dialog = shallowRef<FileProgressDialogInstance>()

async function loadCode() {
  dialog.value?.show(t('label.dumping'))
  dialog.value?.reset()

  try {
    await severManager.server.coderDump(
      project.origin,
      project.path(),
      true,
      (count: number, index: number, file: string) => {
        dialog.value?.updateProgress(count, index, file)
      },
    ).then((response) => {
      coderDumpResponseRef.value = response
      fileTreeModelRef.value = {}
      for (const [key, value] of Object.entries(response)) {
        if (value.diff) {
          fileTreeModelRef.value[key] = true
        }
        else {
          fileTreeModelRef.value[key] = false
        }
      }
      codeRef.value = ''

      ElNotification({
        title: t('label.success'),
        message: t('message.dumpSuccess'),
        duration: 3000,
        offset: 35,
        type: 'success',
      })
    })
  }
  catch (error) {
    console.error(t('message.dumpFailed'), error)
    ElNotification({
      title: t('label.error'),
      message: t('message.dumpFailed'),
      duration: 0,
      offset: 35,
      type: 'error',
    })
  }
  finally {
    dialog.value?.hide()
  }
}

watch(() => route.fullPath, (newValue, _oldValue) => {
  if (newValue !== '/codeView')
    return
  loadCode()
})

function handleCodeFileTreeShowChoose(file: string, type: string) {
  codeRef.value = coderDumpResponseRef.value?.[file].content ?? ''
  languageRef.value = type
}

function handleCodeFileTreeShowDiff(file: string) {
  codeRef.value = coderDumpResponseRef.value?.[file].diff ?? ''
  languageRef.value = 'diff'
}

async function handleCodeFileTreeSave(files: string[], name: string) {
  if (files.length === 1) {
    saveFileWithDialog(coderDumpResponseRef.value?.[files[0]].content ?? '', { defaultPath: name })
  }
  else if (files.length > 1) {
    const zip = new JSZip()
    for (const file of files) {
      zip.file(file, coderDumpResponseRef.value?.[file].content ?? '')
    }
    const blob = await zip.generateAsync({ type: 'blob' })
    const buffer = await blob.arrayBuffer()
    saveFileWithDialog(buffer, { defaultPath: `${name}.zip` })
  }
}

async function handleCodeFileTreeGenerate(files: string[]) {
  dialog.value?.show(t('label.generating'))
  dialog.value?.reset()

  await project?.save()

  try {
    await severManager.server.coderGenerate(
      project.path(),
      undefined,
      files,
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

onMounted(async () => {
  await loadCode()
})
</script>

<template>
  <el-splitter>
    <el-splitter-panel min="250" size="250">
      <CodeFileTree
        :files="fileTreeModelRef"
        @content="handleCodeFileTreeShowChoose"
        @diff="handleCodeFileTreeShowDiff"
        @save="handleCodeFileTreeSave"
        @generate="handleCodeFileTreeGenerate"
      />
    </el-splitter-panel>
    <el-splitter-panel min="5%">
      <CodeView :code="codeRef" :language="languageRef" />
    </el-splitter-panel>
  </el-splitter>

  <FileProgressDialog ref="dialog" />
</template>

<style scoped>
.ep-splitter {
  position: static;
  display: flex;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-splitter-panel) {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.loading-content {
  display: flex;
  flex-direction: column;
}

.loading-info {
  margin-top: 20px;
  text-align: center;
}

.loading-info p {
  margin: 5px 0;
}
</style>
