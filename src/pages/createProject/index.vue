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
 *  2025-08-14     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { Summary } from '~/database'
import { shallowReactive, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import pkg from '~/../package.json'
import { useSummaryManager } from '~/database'
import { createProject, showOpenDialog } from '~/utils'

interface FormModelType {
  projectName: string
  projectPath: string
  builder: string
  builderVersion: string
  toolchains: string
  hal: string
}

const formModel = shallowReactive<FormModelType>({
  projectName: '',
  projectPath: '',
  builder: '',
  builderVersion: '',
  toolchains: '',
  hal: '',
})

const summaryManager = useSummaryManager()
const i18n = useI18n()
const { t } = i18n

const builderOptions = shallowRef<string[]>([])
const builderVersionOptions = shallowRef<string[]>([])
const toolchainsOptions = shallowRef<string[]>([])
const halOptions = shallowRef<string[]>([])

const filterResult = shallowRef<string[]>([])
const chip = shallowRef<string>('')
const dialogVisible = shallowRef(false)

let summary: Summary | null = null

watch(() => formModel.builder, (_newValue: string) => {
  if (summary) {
    builderVersionOptions.value = Object.keys(summary.builders[formModel.builder])
    formModel.builderVersion = builderVersionOptions.value[0]
  }
})

watch(() => formModel.builderVersion, (_newValue: string) => {
  if (summary) {
    toolchainsOptions.value = summary.builders[formModel.builder][formModel.builderVersion]
    formModel.toolchains = toolchainsOptions.value[0]
  }
})

function create(chip: string) {
  const parts = chip.split('@')
  if (parts.length <= 1) {
    console.error('chip name error', chip)
    return
  }

  const vendor = parts[0]
  const chipName = parts[1]

  summary = summaryManager.get(vendor, chipName)
  if (!summary) {
    console.error('chip not found', chip)
    return
  }

  builderOptions.value = Object.keys(summary.builders)
  formModel.builder = builderOptions.value[0]

  halOptions.value = summary.hals
  formModel.hal = halOptions.value[0]

  dialogVisible.value = true
}

async function chooseFolder() {
  const { filePaths, canceled } = await showOpenDialog(
    {
      title: t('message.openCspProject'),
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

function handCreate() {
  if (!summary) {
    return
  }
  createProject(formModel.projectPath, {
    name: formModel.projectName,
    vendor: summary.vendor,
    targetChip: summary.name,
    version: pkg.version,
    gen: {
      builder: formModel.builder,
      builderVersion: formModel.builderVersion,
      toolchains: formModel.toolchains,
      hal: formModel.hal,
    },
  })
  dialogVisible.value = false
}
</script>

<template>
  <el-splitter>
    <el-splitter-panel min="250" max="50%" size="250">
      <ChipFilter v-model="filterResult" />
    </el-splitter-panel>
    <el-splitter-panel min="50%">
      <el-splitter layout="vertical">
        <el-splitter-panel min="10%" size="70%">
          <ChipInfo :chip="chip" />
        </el-splitter-panel>
        <el-splitter-panel min="10%">
          <ChipTable
            v-model="chip"
            :filter-result="filterResult"
          />
        </el-splitter-panel>
      </el-splitter>
      <div class="tools-div my-4 pr-4">
        <el-button type="primary" :disabled="!chip" @click="create(chip)">
          {{ $t('command.createProject') }}
        </el-button>
      </div>
    </el-splitter-panel>
  </el-splitter>
  <el-dialog
    v-model="dialogVisible"
    :close-on-click-modal="false"
    :modal="false"
    :title="$t('command.createProject')"
    draggable
  >
    <el-form :model="formModel" label-position="left" label-width="auto">
      <div>
        <el-form-item :label="$t('label.projectName')" :required="true">
          <el-input v-model="formModel.projectName" />
        </el-form-item>
        <el-form-item :label="$t('label.projectPath')" :required="true">
          <div style="flex: 1; display: flex; gap: 8px;">
            <el-input v-model="formModel.projectPath" :readonly="true" />
            <el-button circle @click="chooseFolder">
              <el-icon><i class="ri-more-line" /></el-icon>
            </el-button>
          </div>
        </el-form-item>
        <el-form-item :label="$t('label.builderTool')" :required="true">
          <el-select v-model="formModel.builder">
            <el-option
              v-for="option in builderOptions"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('label.builderVersion')" :required="true">
          <el-select v-model="formModel.builderVersion">
            <el-option
              v-for="option in builderVersionOptions"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('label.toolchains')" :required="true">
          <el-select v-model="formModel.toolchains">
            <el-option
              v-for="option in toolchainsOptions"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item :label="$t('label.hal')" :required="true">
          <el-select v-model="formModel.hal">
            <el-option
              v-for="option in halOptions"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
      </div>
    </el-form>
    <template #footer>
      <div class="dialog-footer">
        <el-button @click="dialogVisible = false">
          {{ $t('command.cancel') }}
        </el-button>
        <el-button type="primary" @click="handCreate">
          {{ $t('command.ok') }}
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.ep-splitter {
  position: static;
  display: flex;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-splitter-panel) {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

.tools-div {
  display: flex;
  justify-content: end;
}
</style>
