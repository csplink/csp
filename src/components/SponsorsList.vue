<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        SponsorsList.vue
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
import { onMounted, shallowRef } from 'vue'
import yaml from 'yaml'

export interface SponsorType {
  avatar: string
  amount: number
  comment: string
  name: string
}

const sponsors = shallowRef<SponsorType[]>([])

async function loadImages() {
  const resp = await fetch('./sponsors')
  const text = await resp.text()
  const parsedData = yaml.parse(text) as SponsorType[]
  sponsors.value = parsedData
}

onMounted(() => {
  loadImages()
})
</script>

<template>
  <div class="avatar-container">
    <el-tooltip
      v-for="(user, index) in sponsors"
      :key="index"
      popper-class="custom-tooltip"
    >
      <template #content>
        <div class="tooltip-content">
          <div class="sponsor-name">
            {{ user.name }}
          </div>
          <div class="sponsor-amount">
            ¥{{ user.amount }}
          </div>
          <div v-if="user.comment" class="sponsor-comment">
            {{ user.comment }}
          </div>
        </div>
      </template>
      <el-avatar
        :size="32"
        :src="user.avatar"
        class="avatar-item"
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
}

.avatar-item:hover {
  transform: scale(1.1);
  box-shadow: 0 2px 12px var(--ep-text-color-primary);
}

.custom-tooltip {
  background: #2c3e50 !important;
  border: none !important;
  border-radius: 8px !important;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2) !important;
  padding: 12px 16px !important;
  max-width: 200px !important;
}

.tooltip-content {
  text-align: center;
  line-height: 1.5;
}

.sponsor-name {
  font-weight: 600;
  font-size: 14px;
  color: #ffffff;
  margin-bottom: 4px;
}

.sponsor-amount {
  font-size: 16px;
  font-weight: bold;
  color: #4caf50;
  margin-bottom: 4px;
}

.sponsor-comment {
  font-size: 12px;
  color: #bdc3c7;
  font-style: italic;
  word-wrap: break-word;
}
</style>
