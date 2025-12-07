<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        AboutDialog.vue
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
 *  2025-11-18     xqyjlj       initial version
-->
<script lang="ts" setup>
import { shallowRef } from 'vue'
import pkg from '../../../package.json'

const visible = shallowRef(false)

function show() {
  visible.value = true
}

function hide() {
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
    :title="$t('label.about')"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="true"
    center
    append-to-body
  >
    <div class="about-content">
      <el-descriptions
        :column="1"
        :border="true"
      >
        <el-descriptions-item :label="$t('label.version')">
          {{ pkg.version }}
        </el-descriptions-item>
        <el-descriptions-item :label="$t('label.license')">
          Apache License 2.0
        </el-descriptions-item>
        <el-descriptions-item label="electron">
          {{ pkg.devDependencies.electron }}
        </el-descriptions-item>
        <el-descriptions-item label="vite">
          {{ pkg.devDependencies.vite }}
        </el-descriptions-item>
        <el-descriptions-item label="element-plus">
          {{ pkg.dependencies['element-plus'] }}
        </el-descriptions-item>
        <el-descriptions-item label="vue">
          {{ pkg.dependencies.vue }}
        </el-descriptions-item>
        <el-descriptions-item label="prismjs">
          {{ pkg.dependencies.prismjs }}
        </el-descriptions-item>
        <el-descriptions-item label="konva">
          {{ pkg.dependencies.konva }}
        </el-descriptions-item>
        <el-descriptions-item label="markdown-it">
          {{ pkg.dependencies['markdown-it'] }}
        </el-descriptions-item>
        <el-descriptions-item label="pinia">
          {{ pkg.dependencies.pinia }}
        </el-descriptions-item>
        <el-descriptions-item label="socket.io-client">
          {{ pkg.dependencies['socket.io-client'] }}
        </el-descriptions-item>
      </el-descriptions>
    </div>
  </el-dialog>
</template>

<style lang="scss" scoped>
.about-content {
  user-select: text;
}
</style>
