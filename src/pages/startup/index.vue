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
 *  2025-04-29     xqyjlj       initial version
-->

<script setup lang="ts">
import { useI18n } from 'vue-i18n'
import { createWindow, openProject } from '~/utils'

const i18n = useI18n()

async function handNewProject() {
  createWindow({ runMode: 'createProject', backendUrl: 'http://127.0.0.1:55432' })
}

async function handOpenProject() {
  await openProject(i18n)
}
</script>

<template>
  <div class="main-grid">
    <el-card class="grid-item" :body-style="{ display: 'flex', flex: '1' }">
      <template #header>
        {{ $t('startup.command') }}
      </template>
      <div class="btn-group mb-4 flex justify-center">
        <el-button type="primary" @click="handNewProject">
          {{ $t('startup.newChipProject') }}
        </el-button>
        <el-button type="primary" @click="handOpenProject">
          {{ $t('startup.openProject') }}
        </el-button>
      </div>
    </el-card>
    <el-card class="grid-item">
      <template #header>
        {{ $t('startup.contributors') }}
      </template>
      <ContributorsList />
    </el-card>
    <el-card class="grid-item">
      <template #header>
        {{ $t('startup.recentProjects') }}
      </template>
      <RecentProjectsCard />
    </el-card>
    <el-card class="grid-item">
      <template #header>
        {{ $t('startup.more') }}
      </template>
    </el-card>
  </div>
</template>

<style scoped>
.main-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 9px;
  padding: 9px;
  flex: 1;
}

.ep-card {
  --ep-card-padding: 12px;
}

.grid-item {
  display: flex;
  flex-direction: column;
  text-align: left;
  border-radius: 9px;
}

::v-deep(.ep-card__body) {
  min-width: 0;
  min-height: 0;
}

.btn-group {
  flex: 1;
  flex-direction: column;
  gap: 20px;
  padding: 20px;
}

.ep-button + .ep-button {
  margin-left: 0px;
}
</style>
