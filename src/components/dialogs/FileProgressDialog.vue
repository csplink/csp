<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        FileProgressDialog.vue
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
 *  2025-10-20     xqyjlj       initial version
-->

<script lang="ts" setup>
import { shallowReactive, shallowRef } from 'vue'

const visible = shallowRef(false)
const titleRef = shallowRef('')
const state = shallowReactive({
  progress: 0,
  currentFile: '',
  total: 0,
  current: 0,
})

function updateProgress(total: number, index: number, file: string) {
  state.total = total
  state.current = index
  state.currentFile = file
  state.progress = Math.floor((index / total) * 100)
}

function show(title: string) {
  visible.value = true
  titleRef.value = title
}

function hide() {
  visible.value = false
}

function reset() {
  state.progress = 0
  state.currentFile = '...'
  state.total = 0
  state.current = 0
}

defineExpose({
  show,
  hide,
  reset,
  updateProgress,
})
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="titleRef"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="false"
    center
    append-to-body
  >
    <div class="loading-content">
      <el-progress :percentage="state.progress" />
      <div class="loading-info">
        <p v-if="state.total > 0">
          {{ $t('label.progress') }}: {{ state.current }}/{{ state.total }}
        </p>
        <p>{{ $t('label.currentFile') }}: {{ state.currentFile }}</p>
      </div>
    </div>
  </el-dialog>
</template>
