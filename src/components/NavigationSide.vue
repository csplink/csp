<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        NavigationSide.vue
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
import { nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const emit = defineEmits(['generate'])

const router = useRouter()
const route = useRoute()

function handleSelect(index: string) {
  if (!index)
    return
  if (!route.path.startsWith(index)) {
    nextTick(() => {
      router.push(index)
    })
  }
}

function handleGenerate() {
  emit('generate')
}
</script>

<template>
  <el-menu
    default-active="1"
    class="menu-box"
    :collapse="true"
    @select="handleSelect"
  >
    <el-menu-item index="/chipConfigure">
      <el-icon><i class="ri-cpu-line" /></el-icon>
      <template #title>
        CPU
      </template>
    </el-menu-item>
    <el-menu-item index="/clockConfigure">
      <el-icon><i class="ri-time-line" /></el-icon>
      <template #title>
        {{ $t('label.clock') }}
      </template>
    </el-menu-item>
    <el-menu-item index="/codeView">
      <el-icon><i class="ri-code-box-line" /></el-icon>
      <template #title>
        {{ $t('label.code') }}
      </template>
    </el-menu-item>
    <div class="spacer" />
    <li
      class="ep-menu-item"
      @click="handleGenerate"
    >
      <el-tooltip
        :content="$t('command.generate')"
        placement="right"
      >
        <div class="ep-menu-tooltip__trigger">
          <el-icon><i class="ri-ai-generate" /></el-icon>
        </div>
      </el-tooltip>
    </li>
    <el-menu-item index="/sponsor">
      <el-icon><i class="ri-cup-line" /></el-icon>
      <template #title>
        {{ $t('label.sponsor') }}
      </template>
    </el-menu-item>
    <el-menu-item index="/packageManager">
      <el-icon><i class="ri-book-shelf-line" /></el-icon>
      <template #title>
        {{ $t('label.packages') }}
      </template>
    </el-menu-item>
    <el-menu-item index="/settings">
      <el-icon><i class="ri-settings-line" /></el-icon>
      <template #title>
        {{ $t('label.settings') }}
      </template>
    </el-menu-item>
  </el-menu>
</template>

<style scoped>
.menu-box {
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
}

.spacer {
  flex-grow: 1;
}
</style>
