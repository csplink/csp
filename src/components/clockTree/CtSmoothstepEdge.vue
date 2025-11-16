<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CtSmoothstepEdge.vue
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
 *  2025-10-08     xqyjlj       initial version
-->

<script lang="ts" setup>
import { BaseEdge, getSmoothStepPath, Position } from '@vue-flow/core'
import { computed } from 'vue'

interface PropsType {
  id: string
  sourceX: number
  sourceY: number
  targetX: number
  targetY: number
  data: {
    text: string
  }
  style: any
  label: string
}

const props = defineProps<PropsType>()

const path = computed(() => getSmoothStepPath({ ...props, offset: 0, sourcePosition: Position.Right, targetPosition: Position.Left }))
</script>

<template>
  <BaseEdge
    :id="id"
    :style="style"
    :path="path[0]"
    :label="label"
    :label-x="path[1]"
    :label-y="path[2]"
    :label-show-bg="true"
  />
</template>

<style>
.vue-flow__edge-ct-smoothstep path {
  stroke: var(--ep-text-color-primary);
  stroke-width: 3px;
}

.vue-flow__edge-ct-smoothstep.animated path {
  stroke: var(--ct-vue-flow-node-animated-color);
  stroke-width: 5px;
}

.vue-flow__edge-ct-smoothstep.selected path {
  stroke: var(--ct-vue-flow-node-selected-color) !important;
  stroke-width: 5px;
}
</style>
