<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        SaveAsProjectDialog.vue
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
 *  2025-11-19     xqyjlj       initial version
-->

<script lang="ts" setup>
import { shallowReactive, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { saveAsProject, showOpenDialog, useProjectManager } from '~/utils'

interface FormModelType {
  projectName: string
  projectPath: string
}

const formModel = shallowReactive<FormModelType>({
  projectName: '',
  projectPath: '',
})

const visible = shallowRef(false)

const projectManager = useProjectManager()
const i18n = useI18n()

const { t } = i18n
const project = projectManager.get()!

function show() {
  visible.value = true
}

function hide() {
  visible.value = false
}

async function chooseFolder() {
  const { filePaths, canceled } = await showOpenDialog(
    {
      title: t('command.saveAs'),
      properties: ['openDirectory'],
    },
  )

  if (canceled || !filePaths) {
    return
  }

  if (filePaths.length !== 1) {
    return { success: false }
  }

  formModel.projectPath = filePaths[0]
}

async function handSaveAs() {
  await saveAsProject(formModel.projectPath, formModel.projectName, project.origin)
  visible.value = false
}

defineExpose({
  show,
  hide,
})
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="$t('command.saveAs')"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="true"
    center
    append-to-body
  >
    <el-form :model="formModel" label-position="left" label-width="auto">
      <div>
        <el-form-item label="工程名称" :required="true">
          <el-input v-model="formModel.projectName" />
        </el-form-item>
        <el-form-item label="工程路径" :required="true">
          <div style="flex: 1; display: flex; gap: 8px;">
            <el-input v-model="formModel.projectPath" :readonly="true" />
            <el-button circle @click="chooseFolder">
              <el-icon><i class="ri-more-line" /></el-icon>
            </el-button>
          </div>
        </el-form-item>
      </div>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="visible = false">
          {{ $t('command.cancel') }}
        </el-button>
        <el-button
          type="primary"
          :disabled="!formModel.projectName || !formModel.projectPath"
          @click="handSaveAs"
        >
          {{ $t('command.ok') }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>
