<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CtProbeNode.vue
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
 *  2025-10-07     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { ClockTreeNode, IpParameterNumber } from '~/database'
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
const sourceData = useNodesData(() => sourceConnections.value[0]?.source)

const parameter = computed(
  (): IpParameterNumber | null => {
    const p = toValue(props.node.parameter)
    if (['integer', 'float'].includes(p.type)) {
      return p as IpParameterNumber
    }
    return null
  },
)
const input = computed((): number => {
  const data = sourceData.value
  if (data) {
    return data.data.output
  }
  else {
    return 0
  }
})
const title = computed((): string => parameter.value?.display.value || props.id)
const value = computed({
  get: (): number => parameter.value?.value.value ?? 0,
  set: (value: number) => {
    if (parameter.value) {
      parameter.value.value.value = value
    }
  },
})

watch(
  () => input.value,
  (v: number) => {
    updateNodeData(props.id, { output: v }, { replace: false })
    value.value = v
    if (parameter.value) {
      parameter.value.value.value = v
    }
  },
  { immediate: true },
)
</script>

<template>
  <div class="title">
    {{ title }}
  </div>
  <UnitInput
    v-model="value"
    class="nodrag"
    :unit="node.unit"
    :readonly="true"
    :max="parameter?.max.value ?? Number.MAX_SAFE_INTEGER"
    :min="parameter?.min.value ?? Number.MIN_SAFE_INTEGER"
  />
  <Handle
    id="target"
    type="target"
    :position="Position.Left"
    :connectable="true"
    :style="{ top: '65.75%' }"
    :is-valid-connection="isValidTargetConnection"
  />
  <Handle
    id="source"
    type="source"
    :position="Position.Right"
    :connectable="true"
    :style="{ top: '65.75%' }"
    :is-valid-connection="isValidSourceConnection"
  />
</template>

<style>
.vue-flow__node-ct-probe {
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  box-shadow: 0 0 10px var(--ep-menu-border-color);
}

.vue-flow__node-ct-probe.selected {
  box-shadow: 0 0 0 2px var(--ct-vue-flow-node-selected-color);
}

.vue-flow__node-ct-probe .vue-flow__handle {
  height: 24px;
  width: 10px;
  border-radius: 4px;
}

.vue-flow__node-ct-probe .unit-input-container {
  width: 100%;
}

.vue-flow__node-ct-probe .vue-flow__handle-source {
  background-color: var(--ct-vue-flow-handle-source-background-color);
}

.vue-flow__node-ct-probe .vue-flow__handle-target {
  background-color: var(--ct-vue-flow-handle-target-background-color);
}
</style>
