<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CtCliffEdge.vue
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
  label: string
}

const props = defineProps<PropsType>()

const edgeConfig = {
  offsetA: { x: 30, y: 0 },
  offsetB: { x: 50, y: 30 },
}

const labelSize = computed(() => {
  const padding = 12
  const charWidth = 7
  const minWidth = 30

  const textWidth = props.label.length * charWidth
  const calculatedWidth = Math.max(textWidth + padding, minWidth)

  return {
    width: calculatedWidth,
    height: 16,
  }
})
</script>

<template>
  <g>
    <path
      fill="none"
      :d="`
        M${props.sourceX},${props.sourceY}
        L${props.sourceX + edgeConfig.offsetA.x},${props.sourceY + edgeConfig.offsetA.y}
        L${props.sourceX + edgeConfig.offsetB.x},${props.sourceY + edgeConfig.offsetB.y}
    `"
    />

    <g class="text-wrapper">
      <rect :x="props.sourceX + edgeConfig.offsetB.x - (labelSize.width / 2)" :y="props.sourceY + edgeConfig.offsetB.y - 4" :width="labelSize.width" :height="labelSize.height" rx="2" fill="#fbb612" />
      <text :x="props.sourceX + edgeConfig.offsetB.x" :y="props.sourceY + edgeConfig.offsetB.y + 6" text-anchor="middle" dominant-baseline="middle" fill="black">
        {{ label }}
      </text>
    </g>

    <path
      fill="none"
      :d="`
        M${props.targetX - edgeConfig.offsetB.x},${props.targetY - edgeConfig.offsetB.y}
        L${props.targetX - edgeConfig.offsetA.x},${props.targetY - edgeConfig.offsetA.y}
        L${props.targetX},${props.targetY}
      `"
    />

    <g class="text-wrapper">
      <rect :x="props.targetX - edgeConfig.offsetB.x - (labelSize.width / 2)" :y="props.targetY - edgeConfig.offsetB.y - 12" :width="labelSize.width" :height="labelSize.height" rx="2" fill="#fbb612" />
      <text :x="props.targetX - edgeConfig.offsetB.x" :y="props.targetY - edgeConfig.offsetB.y - 2" text-anchor="middle" dominant-baseline="middle" fill="black">
        {{ label }}
      </text>
    </g>
  </g>
</template>

<style>
.vue-flow__edge-ct-cliff path {
  stroke: var(--ep-text-color-primary);
  stroke-width: 3px;
}

.vue-flow__edge-ct-cliff.animated path {
  stroke: var(--ct-vue-flow-node-animated-color);
}

.vue-flow__edge-ct-cliff.selected path {
  stroke: var(--ct-vue-flow-node-selected-color);
  stroke-width: 5px;
}
</style>
