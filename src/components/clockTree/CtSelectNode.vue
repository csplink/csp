<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CtSelectNode.vue
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
import { computed, toValue, watchEffect } from 'vue'
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
  (): IpParameterEnum | null => {
    const p = toValue(props.node.parameter)
    if (p.type === 'enum') {
      return p as IpParameterEnum
    }
    return null
  },
)

const mathFunctions = {
  '+': (a: number, b: number) => a + b,
  '-': (a: number, b: number) => a - b,
  '*': (a: number, b: number) => a * b,
  '/': (a: number, b: number) => a / b,
}

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
  get: (): string => parameter.value?.value.value ?? '',
  set: (value: string) => {
    if (parameter.value) {
      parameter.value.value.value = value
    }
  },
})

watchEffect(() => {
  let output = input.value

  if (value.value) {
    const operator = value.value.charAt(0) as keyof typeof mathFunctions /* !< 解析运算符，例如 "*2" -> "*" */
    const operand = Number.parseFloat(value.value.slice(1)) /* !< 解析操作数，例如 "*2" -> 2 */

    if (mathFunctions[operator] && !Number.isNaN(operand)) { /* !< 输入验证和处理 */
      output = mathFunctions[operator](input.value, operand)
    }
  }

  updateNodeData(props.id, { output }, { replace: false })
})
</script>

<template>
  <div class="title">
    {{ title }}
  </div>
  <el-select v-model="value" class="nodrag">
    <el-option
      v-for="[k, v] in Object.entries(parameter?.values ?? {})"
      :key="k"
      :value="k"
      :label="v.comment.value"
    />
  </el-select>
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
.vue-flow__node-ct-select {
  display: flex;
  align-items: center;
  flex-direction: column;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 8px;
  box-shadow: 0 0 10px var(--ep-menu-border-color);
}

.vue-flow__node-ct-select.selected {
  box-shadow: 0 0 0 2px var(--ct-vue-flow-node-selected-color);
}

.vue-flow__node-ct-select .vue-flow__handle {
  height: 24px;
  width: 10px;
  border-radius: 4px;
}

.vue-flow__node-ct-select .ep-select {
  width: 100%;
}

.vue-flow__node-ct-select .vue-flow__handle-source {
  background-color: var(--ct-vue-flow-handle-source-background-color);
}

.vue-flow__node-ct-select .vue-flow__handle-target {
  background-color: var(--ct-vue-flow-handle-target-background-color);
}
</style>
