<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ContributorsList.vue
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

<script setup lang="ts">
import type { Contributor } from '~/utils'
import { onMounted, shallowRef } from 'vue'
import { openUrl, useContributorManager } from '~/utils'

const contributorManager = useContributorManager()

const contributors = shallowRef<Contributor[]>([])

async function loadImages() {
  contributors.value = await contributorManager.get()
}

onMounted(() => {
  loadImages()
})
</script>

<template>
  <div class="avatar-container">
    <el-tooltip
      v-for="(user, index) in contributors"
      :key="index"
      popper-class="custom-tooltip"
    >
      <template #content>
        <div class="tooltip-content">
          <div>{{ user.name }}</div>
        </div>
      </template>
      <el-avatar
        :size="32"
        :src="user.avatar"
        class="avatar-item"
        @click="openUrl(user.htmlUrl)"
      />
    </el-tooltip>
  </div>
</template>

<style scoped>
.avatar-container {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 20px;
}

.avatar-item {
  transition: transform 0.2s ease;
  cursor: pointer;
}

.avatar-item:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 12px var(--ep-text-color-primary);
}
</style>
