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
import { useRoute, useRouter } from 'vue-router'

const router = useRouter()
const route = useRoute()

function handleSelect(index: string) {
  if (!route.path.startsWith(index)) {
    router.push(index)
  }
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
      <el-icon><Cpu /></el-icon>
      <template #title>
        CPU
      </template>
    </el-menu-item>
    <el-menu-item index="/clockConfigure">
      <el-icon><Clock /></el-icon>
      <template #title>
        {{ $t('mainNavigation.clock') }}
      </template>
    </el-menu-item>
    <el-menu-item index="/codeView">
      <el-icon><DataBoard /></el-icon>
      <template #title>
        {{ $t('mainNavigation.code') }}
      </template>
    </el-menu-item>
    <div class="spacer" />
    <el-menu-item index="/nav/4">
      <el-icon><Promotion /></el-icon>
      <template #title>
        {{ $t('mainNavigation.generate') }}
      </template>
    </el-menu-item>
    <el-menu-item index="/nav/4">
      <el-icon><Coffee /></el-icon>
      <template #title>
        {{ $t('mainNavigation.sponsor') }}
      </template>
    </el-menu-item>
    <el-menu-item index="/nav/4">
      <el-icon><Management /></el-icon>
      <template #title>
        {{ $t('mainNavigation.packages') }}
      </template>
    </el-menu-item>
    <el-menu-item index="/settings">
      <el-icon><Setting /></el-icon>
      <template #title>
        {{ $t('mainNavigation.settings') }}
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
