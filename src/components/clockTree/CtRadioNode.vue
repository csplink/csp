<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CtRadioNode.vue
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
 *  2025-09-29     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { ClockTreeNode, IpParameterEnum } from '~/database'
import { Handle, Position, useNodeConnections, useNodesData, useVueFlow } from '@vue-flow/core'
import { computed, toValue, watch } from 'vue'
import { isValidSourceConnection, isValidTargetConnection } from './CtUtils'

interface PropsType {
  id: string
  data: {
    output: number
  }
  node: ClockTreeNode
}

const props = defineProps<PropsType>()

const { updateNodeData } = useVueFlow()
const sourceConnections = useNodeConnections({
  handleType: 'target',
})
const sourceData = useNodesData(() => sourceConnections.value.map(connection => connection.source))

const layoutParams = {
  containerPadding: 8, /* !< padding: 8px 16px */
  radioGap: 8, /* !< gap: 8px */
  radioHeight: 32, /* !< radio高度 */
  idDivHeight: 16, /* !< ID div高度 */
}

const parameter = computed(
  (): IpParameterEnum | null => {
    const p = toValue(props.node.parameter)
    if (p.type === 'enum') {
      return p as IpParameterEnum
    }
    return null
  },
)
const options = computed(
  (): Record<string, { label: string, target: string, enabled: boolean }> => {
    if (parameter.value) {
      const rtn: Record<string, { label: string, target: string, enabled: boolean }> = {}
      for (const [k, v] of Object.entries(parameter.value.values)) {
        rtn[k] = { label: toValue(v.comment), target: `target-${k}`, enabled: v.enabled.value }
      }
      return rtn
    }
    return { '?': { label: '?', target: '?', enabled: false } }
  },
)
const title = computed((): string => parameter.value?.display.value || props.id)
const value = computed({
  get: (): string => parameter.value?.value.value ?? '?',
  set: (value: string) => {
    if (parameter.value) {
      parameter.value.value.value = value
    }
  },
})

const input = computed((): number => {
  const target = options.value[value.value]?.target
  if (!target)
    return 0

  const connection = sourceConnections.value.find(conn => conn.targetHandle === target)
  if (!connection)
    return 0

  const nodeData = sourceData.value.find(node => node.id === connection.source)
  return nodeData?.data?.output ?? 0
})

watch(
  () => input.value,
  (v: number) => {
    updateNodeData(props.id, { output: v }, { replace: false })
  },
  { immediate: true },
)

watch(
  () => value.value,
  (v: string) => {
    const option = options.value[v]!
    if (!option.enabled) {
      console.error(`option ${v} is disabled`)
    }
    updateNodeData(props.id, { selectedValue: v }, { replace: false })
  },
  { immediate: true },
)

function calculateLayoutInfo() {
  const radioCount = Object.keys(options.value).length
  if (radioCount === 0)
    return null

  const { containerPadding, radioGap, radioHeight, idDivHeight } = layoutParams

  const radioGroupStartPosition = containerPadding + idDivHeight + radioGap
  const radioGroupHeight = radioCount * radioHeight + (radioCount - 1) * radioGap
  const totalHeight = containerPadding * 2 + idDivHeight + radioGap + radioGroupHeight

  return {
    radioGroupStartPosition,
    radioGroupHeight,
    totalHeight,
    radioCount,
    radioHeight,
    radioGap,
  }
}

function calculateHandlePosition(index: number): string {
  const layout = calculateLayoutInfo()
  if (!layout)
    return '50%'

  const { radioGroupStartPosition, totalHeight, radioHeight, radioGap } = layout

  /* !< 计算当前radio的中心位置 */
  const radioTopPosition = radioGroupStartPosition + index * (radioHeight + radioGap)
  const radioCenterPosition = radioTopPosition + radioHeight / 2

  /* !< 转换为百分比 */
  const relativeTop = (radioCenterPosition / totalHeight) * 100

  return `${relativeTop}%`
}

function calculateRadioGroupCenter(): string {
  const layout = calculateLayoutInfo()
  if (!layout)
    return '50%'

  const { radioGroupStartPosition, radioGroupHeight, totalHeight } = layout

  /* !< radio组的中心位置 */
  const radioGroupCenterPosition = radioGroupStartPosition + radioGroupHeight / 2

  /* !< 转换为百分比 */
  const relativeTop = (radioGroupCenterPosition / totalHeight) * 100

  return `${relativeTop}%`
}
</script>

<template>
  <div class="title">
    {{ title }}
  </div>
  <el-radio-group v-model="value" class="nodrag">
    <el-radio
      v-for="([k, v], index) of Object.entries(options)"
      :key="index"
      :value="k"
      :disabled="!v.enabled"
      :class="{ 'radio-error': !v.enabled && value === k }"
    >
      <el-tooltip content="该选项已被禁用" :disabled="!(!v.enabled && value === k)">
        {{ v.label }}
      </el-tooltip>
    </el-radio>
  </el-radio-group>
  <Handle
    id="source"
    type="source"
    :position="Position.Right"
    :connectable="true"
    :style="{ top: calculateRadioGroupCenter() }"
    :is-valid-connection="isValidSourceConnection"
  />
  <Handle
    v-for="([k], index) of Object.entries(options)"
    :id="`target-${k}`"
    :key="`${k}`"
    type="target"
    :position="Position.Left"
    :connectable="true"
    :style="{ top: calculateHandlePosition(index) }"
    :is-valid-connection="isValidTargetConnection"
  />
</template>

<style>
.vue-flow__node-ct-radio {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  box-shadow: 0 0 10px var(--ep-menu-border-color);
}

.vue-flow__node-ct-radio.selected {
  box-shadow: 0 0 0 2px var(--ct-vue-flow-node-selected-color);
}

.vue-flow__node-ct-radio .title {
  text-align: center;
  width: 100%;
}

.vue-flow__node-ct-radio .ep-radio-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  align-items: flex-start;
}

.vue-flow__node-ct-radio .ep-radio {
  margin-right: 30px;
}

.vue-flow__node-ct-radio .vue-flow__handle {
  height: 10px;
  width: 10px;
  border-radius: 4px;
}

.vue-flow__node-ct-radio .vue-flow__handle-source {
  background-color: var(--ct-vue-flow-handle-source-background-color);
}

.vue-flow__node-ct-radio [class*='vue-flow__handle-target'] {
  background-color: var(--ct-vue-flow-handle-target-background-color);
}

.vue-flow__node-ct-radio .radio-error .ep-radio__inner {
  background-color: var(--ep-color-error) !important;
}

.vue-flow__node-ct-radio .radio-error .ep-radio__label {
  color: var(--ep-color-error) !important;
}
</style>
