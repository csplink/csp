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
 *  2025-08-03     xqyjlj       initial version
-->

<script setup lang="ts">
import type { PackageDescription } from '~/utils'
import { shallowRef } from 'vue'
import { usePackageManager } from '~/utils'

const packageManager = usePackageManager()

const descriptionRef = shallowRef<PackageDescription>()

async function handPackageTreeClick(kind: string, name: string, version: string) {
  const description = await packageManager.getPackageDescription(kind, name, version)
  descriptionRef.value = description
}
</script>

<template>
  <el-splitter>
    <el-splitter-panel min="250" size="250">
      <PackageTree
        @click="handPackageTreeClick"
      />
    </el-splitter-panel>
    <el-splitter-panel min="5%">
      <PackageInfo
        v-if="descriptionRef !== undefined"
        :description="descriptionRef"
      />
    </el-splitter-panel>
  </el-splitter>
</template>

<style scoped>
.ep-splitter {
  position: static;
  display: flex;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-splitter-panel) {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}
</style>
