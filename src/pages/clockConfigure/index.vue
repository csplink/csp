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
 *  2025-05-13     xqyjlj       initial version
-->

<script setup lang="ts">
import type { ClockViewInstance } from '~/components/instance'
import { ref } from 'vue'

const clockViewRef = ref<ClockViewInstance>()

function clockViewZoomIn() {
  clockViewRef.value?.zoomIn()
}

function clockViewRescale() {
  clockViewRef.value?.rescale()
}

function clockViewZoomOut() {
  clockViewRef.value?.zoomOut()
}
</script>

<template>
  <div class="main-div flex">
    <div class="clock-div flex">
      <ClockView ref="clockViewRef" />
    </div>
    <div class="btn-group my-4 items-center justify-center">
      <el-button circle @click="clockViewZoomIn">
        <el-icon><ZoomIn /></el-icon>
      </el-button>
      <el-button circle @click="clockViewRescale">
        <el-icon><FullScreen /></el-icon>
      </el-button>
      <el-button circle @click="clockViewZoomOut">
        <el-icon><ZoomOut /></el-icon>
      </el-button>
    </div>
  </div>
</template>

<style scoped>
.main-div {
  flex: 1;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

.clock-div {
  flex: 1;
  min-width: 0;
  min-height: 0;
}
</style>
