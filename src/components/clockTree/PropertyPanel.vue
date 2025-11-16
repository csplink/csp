<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PropertyPanel.vue
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
import type { GraphEdge, GraphNode } from '@vue-flow/core'
import { computed, ref, watch } from 'vue'

interface PropsType {
  selectedNodes: GraphNode[]
  selectedEdges: GraphEdge[]
}

const props = defineProps<PropsType>()

const hasSelection = computed(() => props.selectedNodes.length > 0 || props.selectedEdges.length > 0)
const isSingleEdge = computed(() => props.selectedEdges.length === 1)

const nodeForm = ref({
  id: '',
  type: '',
  x: undefined as number | undefined,
  y: undefined as number | undefined,
  width: undefined as number | undefined,
})

const edgeForm = ref({
  id: '',
  source: '',
  target: '',
  sourceHandle: '',
  targetHandle: '',
  label: '',
})

function calculateCommonNodeProperties() {
  if (props.selectedNodes.length === 0)
    return

  const firstNode = props.selectedNodes[0]
  let sameX = true
  let sameY = true
  let sameWidth = true

  for (let i = 1; i < props.selectedNodes.length; i++) {
    const node = props.selectedNodes[i]
    if (node.position.x !== firstNode.position.x)
      sameX = false
    if (node.position.y !== firstNode.position.y)
      sameY = false
    if (node.width !== firstNode.width)
      sameWidth = false
  }

  nodeForm.value = {
    id: props.selectedNodes.length === 1 ? props.selectedNodes[0].id : '',
    type: props.selectedNodes.length === 1 ? props.selectedNodes[0].type : '',
    x: sameX ? Number.parseFloat(firstNode.position.x.toFixed(2)) : undefined,
    y: sameY ? Number.parseFloat(firstNode.position.y.toFixed(2)) : undefined,
    width: sameWidth ? (firstNode.width as number) : undefined,
  }
}

watch([() => props.selectedNodes, () => props.selectedEdges], () => {
  if (props.selectedNodes.length !== 0) {
    calculateCommonNodeProperties()
  }
  if (props.selectedEdges.length === 1) {
    const edge = props.selectedEdges[0]
    edgeForm.value = {
      id: edge.id,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle || '',
      targetHandle: edge.targetHandle || '',
      label: edge.label as string || '',
    }
  }
}, { immediate: true, deep: true })

function updateNodePositionX(x: number) {
  for (const n of props.selectedNodes) {
    n.position.x = x
  }
}

function updateNodePositionY(y: number) {
  for (const n of props.selectedNodes) {
    n.position.y = y
  }
}

function updateNodeWidth(width: number) {
  for (const n of props.selectedNodes) {
    n.width = width
  }
}

function updateEdgeLabel(label: string) {
  for (const e of props.selectedEdges) {
    e.label = label
  }
}
</script>

<template>
  <div class="property-panel">
    <el-scrollbar class="property-panel-scrollbar">
      <div v-if="!hasSelection" class="property-panel-empty">
        <el-empty description="未选中任何元素" />
      </div>
      <div v-else class="property-panel-content">
        <el-form v-if="selectedNodes.length !== 0" label-position="left" label-width="auto" size="small">
          <el-form-item v-if="nodeForm.id" label="ID">
            <el-input v-model="nodeForm.id" disabled />
          </el-form-item>
          <el-form-item v-if="nodeForm.type" label="类型">
            <el-input v-model="nodeForm.type" disabled />
          </el-form-item>
          <el-form-item label="X 位置">
            <el-input-number
              v-model="nodeForm.x"
              :controls="false"
              :precision="2"
              :placeholder="nodeForm.x === undefined ? '混合' : ''"
              style="width: 100%"
              @change="(value:number|undefined) => updateNodePositionX(value || 0)"
            />
          </el-form-item>
          <el-form-item label="Y 位置">
            <el-input-number
              v-model="nodeForm.y"
              :controls="false"
              :precision="2"
              :placeholder="nodeForm.y === undefined ? '混合' : ''"
              style="width: 100%"
              @change="(value:number|undefined) => updateNodePositionY(value || 0)"
            />
          </el-form-item>
          <el-form-item label="宽度">
            <el-input-number
              v-model="nodeForm.width"
              :controls="false"
              :precision="2"
              :placeholder="nodeForm.width === undefined ? '混合' : ''"
              style="width: 100%"
              @change="(value:number|undefined) => updateNodeWidth(value || 0)"
            />
          </el-form-item>
        </el-form>

        <el-form v-else-if="isSingleEdge" label-position="left" label-width="auto" size="small">
          <el-form-item label="ID">
            <el-input v-model="edgeForm.id" disabled />
          </el-form-item>
          <el-form-item label="源节点">
            <el-input v-model="edgeForm.source" disabled />
          </el-form-item>
          <el-form-item label="目标节点">
            <el-input v-model="edgeForm.target" disabled />
          </el-form-item>
          <el-form-item label="源句柄">
            <el-input v-model="edgeForm.sourceHandle" disabled />
          </el-form-item>
          <el-form-item label="目标句柄">
            <el-input v-model="edgeForm.targetHandle" disabled />
          </el-form-item>
          <el-form-item label="标签">
            <el-input
              v-model="edgeForm.label"
              placeholder="请输入标签"
              @change="(value:string|undefined) => updateEdgeLabel(value || '')"
            />
          </el-form-item>
        </el-form>
      </div>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.property-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.property-panel-header {
  padding: 12px 16px;
}

.property-panel-title {
  font-weight: 600;
  color: #111827;
  font-size: 14px;
}

.property-panel-scrollbar {
  flex: 1;
  min-height: 0;
}

.property-panel-empty {
  padding: 40px 16px;
}

.property-panel-content {
  padding: 16px;
}

.property-section-title {
  padding: 0 0 12px 0;
  font-weight: 600;
  color: #374151;
  font-size: 13px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 16px;
}

:deep(.el-form-item) {
  margin-bottom: 16px;
}

:deep(.el-form-item__label) {
  font-size: 12px;
  color: #6b7280;
  font-weight: 500;
  margin-bottom: 4px;
}

:deep(.el-input__inner) {
  text-align: left;
}

:deep(.el-input-number .el-input__inner) {
  text-align: left;
}
</style>
