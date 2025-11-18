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
 *  2025-05-18     xqyjlj       initial version
-->

<script setup lang="ts">
import Generate from './generate.vue'
import System from './system.vue'
</script>

<template>
  <el-tabs tab-position="left" class="demo-tabs">
    <el-tab-pane :label="$t('label.systemSetting')">
      <el-scrollbar class="setting-scrollbar">
        <System />
      </el-scrollbar>
    </el-tab-pane>
    <el-tab-pane :label="$t('label.generateSetting')">
      <el-scrollbar class="setting-scrollbar">
        <Generate />
      </el-scrollbar>
    </el-tab-pane>
  </el-tabs>
</template>

<style scoped>
.ep-tabs {
  flex: 1;
  display: flex;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-tabs__content) {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

::v-deep(.ep-tab-pane) {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.setting-scrollbar {
  flex: 1;
}
</style>

<style>
.g-settings-container {
  padding: 0px 20px;
}

.g-settings-section {
  padding: 20px;
}

.g-settings-title {
  display: flex;
  font-size: 18px;
  padding-bottom: 10px;
}

.g-settings-item {
  margin-bottom: 20px;
}
</style>
