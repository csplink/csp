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
import type { CoderDumpResponseType } from '~/composables'
import type { Project } from '~/database'
import JSZip from 'jszip'
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { coderDump } from '~/composables'
import { saveFileWithDialog } from '~/composables/io'
import { useProjectManager } from '~/database'

const projectManager = useProjectManager()
const route = useRoute()
const codeRef = ref<string>('')
const languageRef = ref('c')
const projectRef = ref<Project>()
const coderDumpResponseRef = ref<CoderDumpResponseType>()
const fileTreeModelRef = ref<Record<string, boolean>>({})

async function loadCode() {
  await coderDump(projectRef.value?.origin ?? null, projectRef.value?.path() ?? '', true).then((response) => {
    coderDumpResponseRef.value = response
    fileTreeModelRef.value = {}
    for (const [key, value] of Object.entries(response.files)) {
      if (value.diff) {
        fileTreeModelRef.value[key] = true
      }
      else {
        fileTreeModelRef.value[key] = false
      }
    }
    codeRef.value = ''
  })
}

watch(() => route.fullPath, (newValue, _oldValue) => {
  if (newValue !== '/codeView')
    return
  loadCode()
})

function handleCodeFileTreeShowChoose(file: string, type: string) {
  codeRef.value = coderDumpResponseRef.value?.files[file].content ?? ''
  languageRef.value = type
}

function handleCodeFileTreeShowDiff(file: string) {
  codeRef.value = coderDumpResponseRef.value?.files[file].diff ?? ''
  languageRef.value = 'diff'
}

async function handleCodeFileTreeSave(files: string[], name: string) {
  if (files.length === 1) {
    saveFileWithDialog(coderDumpResponseRef.value?.files[files[0]].content ?? '', { defaultPath: name })
  }
  else if (files.length > 1) {
    const zip = new JSZip()
    for (const file of files) {
      zip.file(file, coderDumpResponseRef.value?.files[file].content ?? '')
    }
    const blob = await zip.generateAsync({ type: 'blob' })
    const buffer = await blob.arrayBuffer()
    saveFileWithDialog(buffer, { defaultPath: `${name}.zip` })
  }
}

function handleCodeFileTreeGenerate(files: string[]) {
  console.log(files)
}

onMounted(async () => {
  const project = projectManager.get()
  if (project) {
    projectRef.value = project
    await loadCode()
  }
})
</script>

<template>
  <el-splitter>
    <el-splitter-panel min="5%">
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
</style>
