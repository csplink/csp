<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CtView.vue
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

<script lang="ts" setup>
import type { ClockTreeEdgeType } from '@/electron/types'
import type { Connection, Edge, Node } from '@vue-flow/core'
import { Background } from '@vue-flow/background'
import { useVueFlow, VueFlow } from '@vue-flow/core'
import { MiniMap } from '@vue-flow/minimap'
import { toPng } from 'html-to-image'
import { nextTick, onMounted, shallowRef, watch } from 'vue'
import { useClockTreeManager } from '~/database'
import { isDev, useProjectManager } from '~/utils'

import {
  alignBottom,
  alignHorizontalCenter,
  alignLeft,
  alignRight,
  alignTop,
  alignVerticalCenter,
  distributeHorizontally,
  distributeVertically,
  updateEdgesAnimation,
} from './clockTree/CtUtils'
import '@vue-flow/core/dist/style.css'
import '@vue-flow/core/dist/theme-default.css'

const projectManager = useProjectManager()
const clockTreeManager = useClockTreeManager()
const {
  addEdges,
  updateNode,
  getNodes,
  getEdges,
  getSelectedNodes,
  getSelectedEdges,
  fitView,
  zoomIn,
  zoomOut,
  vueFlowRef,
} = useVueFlow()

const project = projectManager.get()!
const clockTree = clockTreeManager.get(project.vendor, project.targetChip)!

const isDevMode = shallowRef(false)
const nodes = shallowRef<Node[]>([])
const edges = shallowRef<Edge[]>([])
const isLayoutLocked = shallowRef(true)

function buildNodes(): Node[] {
  const rtn: Node[] = []

  for (const [name, node] of Object.entries(clockTree.nodes)) {
    const n: Node = {
      id: name,
      type: node.type,
      data: { output: 0, node },
      position: node.position,
      width: 200,
    }
    watch(
      () => node.enabled.value,
      (v: boolean) => {
        n.selectable = v
        n.class = v ? '' : 'ct-un-focusable'
        updateNode(n.id, { selectable: v, class: v ? '' : 'ct-un-focusable' }, { replace: false })
      },
      { immediate: true },
    )
    rtn.push(n)
  }

  return rtn
}

function buildEdges(): Edge[] {
  const rtn: Edge[] = []

  for (const [name, edge] of Object.entries(clockTree.edges)) {
    rtn.push({
      id: name,
      type: edge.type,
      source: edge.source,
      target: edge.target,
      sourceHandle: edge.sourceHandle,
      targetHandle: edge.targetHandle,
      label: edge.label,
    })
  }

  return rtn
}

function handSaveCommand() {
  for (const n of getNodes.value) {
    const node = clockTree.nodes[n.id]
    node.position.x = Number.parseFloat(n.position.x.toFixed(2))
    node.position.y = Number.parseFloat(n.position.y.toFixed(2))
  }

  const es: Record<string, ClockTreeEdgeType> = {}
  for (const e of getEdges.value) {
    const id = `(${e.source}@${e.sourceHandle})->(${e.target}@${e.targetHandle})`
    const edge = clockTree.edges[id]
    es[id] = {
      source: e.source,
      target: e.target,
      sourceHandle: e.sourceHandle!,
      targetHandle: e.targetHandle!,
      label: e.label as string,
      type: edge?.type ?? 'ct-smoothstep',
    }
  }
  clockTree.updateEdges(es)

  clockTreeManager.save(project.vendor, project.targetChip)
}

async function handExportCommand() {
  fitView()
  await nextTick()
  downloadSvg()
}

function downloadSvg() {
  toPng(vueFlowRef.value!, {
    quality: 1,
    pixelRatio: 5,
    filter: (node) => {
      return !node.classList?.contains('vue-flow__background')
        && !node.classList?.contains('vue-flow__minimap')
    },
  })
    .then((dataUrl) => {
      const link = document.createElement('a')
      link.href = dataUrl
      link.download = `${project.targetChip}-clock-tree.png`
      link.click()
      link.remove()
    })
    .catch((error) => {
      console.error('oops, something went wrong!', error)
    })
}

function toggleLayoutLock() {
  isLayoutLocked.value = !isLayoutLocked.value
}

function handConnect(connection: Connection) {
  addEdges({ ...connection, type: 'smoothstep' })
}

watch(getSelectedNodes, () => {
  updateEdgesAnimation(getSelectedNodes.value, getNodes.value, getEdges.value)
}, { deep: true })

watch(getSelectedEdges, (edges) => {
  for (const edge of getEdges.value) {
    const e = edges.find(e => e.id === edge.id)
    if (e) {
      edge.zIndex = 999
    }
    else {
      edge.zIndex = 0
    }
  }
})

onMounted(async () => {
  isDevMode.value = await isDev()
  nodes.value = buildNodes()
  edges.value = buildEdges()
})

defineExpose({
  rescale: fitView,
  zoomIn,
  zoomOut,
  downloadSvg,
})
</script>

<template>
  <el-splitter>
    <el-splitter-panel>
      <div v-if="isDevMode" class="clock-toolbar">
        <el-tooltip :content="$t('command.save')" placement="right">
          <el-button @click="handSaveCommand()">
            <i class="ri-save-line" />
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.export')" placement="right">
          <el-button @click="handExportCommand()">
            <i class="ri-export-line" />
          </el-button>
        </el-tooltip>
        <el-divider direction="horizontal" />
        <el-tooltip :content="isLayoutLocked ? '解锁布局' : '锁定布局'" placement="right">
          <el-button :type="isLayoutLocked ? 'primary' : ''" @click="toggleLayoutLock()">
            <i :class="isLayoutLocked ? 'ri-lock-line' : 'ri-lock-unlock-line'" />
          </el-button>
        </el-tooltip>
        <el-divider direction="horizontal" />
        <el-tooltip :content="$t('command.alignLeft')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 2" @click="alignLeft(getSelectedNodes)">
            <i class="ri-align-item-left-line" />
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.alignHorizontalCenter')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 2" @click="alignHorizontalCenter(getSelectedNodes)">
            <i class="ri-align-item-horizontal-center-line" />
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.alignRight')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 2" @click="alignRight(getSelectedNodes)">
            <i class="ri-align-item-right-line" />
          </el-button>
        </el-tooltip>
        <el-divider direction="horizontal" />
        <el-tooltip :content="$t('command.alignTop')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 2" @click="alignTop(getSelectedNodes)">
            <i class="ri-align-item-top-line" />
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.alignVerticalCenter')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 2" @click="alignVerticalCenter(getSelectedNodes)">
            <i class="ri-align-item-vertical-center-line" />
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.alignBottom')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 2" @click="alignBottom(getSelectedNodes)">
            <i class="ri-align-item-bottom-line" />
          </el-button>
        </el-tooltip>
        <el-divider direction="horizontal" />
        <el-tooltip :content="$t('command.distributeHorizontally')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 3" @click="distributeHorizontally(getSelectedNodes)">
            <i class="ri-flip-horizontal-line" />
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.distributeVertically')" placement="right">
          <el-button :disabled="getSelectedNodes.length < 3" @click="distributeVertically(getSelectedNodes)">
            <i class="ri-flip-vertical-line" />
          </el-button>
        </el-tooltip>
      </div>
      <VueFlow
        :nodes="nodes"
        :edges="edges"
        :nodes-draggable="!isLayoutLocked"
        fit-view-on-init
        elevate-edges-on-select
        :min-zoom="0.2"
        :max-zoom="4"
        @connect="handConnect"
      >
        <template #node-ct-input-number="props">
          <CtInputNumberNode :id="props.id" :data="props.data" :node="props.data.node" />
        </template>
        <template #node-ct-select="props">
          <CtSelectNode :id="props.id" :data="props.data" :node="props.data.node" />
        </template>
        <template #node-ct-radio="props">
          <CtRadioNode :id="props.id" :data="props.data" :node="props.data.node" />
        </template>
        <template #node-ct-output="props">
          <CtOutputNode :id="props.id" :node="props.data.node" />
        </template>
        <template #node-ct-probe="props">
          <CtProbeNode :id="props.id" :data="props.data" :node="props.data.node" />
        </template>
        <template #node-ct-number-label="props">
          <CNumberLabelNode :id="props.id" :node="props.data.node" />
        </template>
        <template #edge-ct-smoothstep="props">
          <CtSmoothstepEdge
            :id="props.id"
            :source-x="props.sourceX"
            :source-y="props.sourceY"
            :target-x="props.targetX"
            :target-y="props.targetY"
            :data="props.data"
            :style="props.style"
            :label="props.label as string"
          />
        </template>
        <template #edge-ct-cliff="props">
          <CtCliffEdge
            :id="props.id"
            :source-x="props.sourceX"
            :source-y="props.sourceY"
            :target-x="props.targetX"
            :target-y="props.targetY"
            :data="props.data"
            :label="props.label as string"
          />
        </template>

        <template v-if="isDevMode">
          <Background />
          <MiniMap />
        </template>
      </VueFlow>
    </el-splitter-panel>
    <el-splitter-panel v-if="isDevMode" min="250" max="20%" size="250">
      <PropertyPanel
        :selected-nodes="getSelectedNodes"
        :selected-edges="getSelectedEdges"
      />
    </el-splitter-panel>
  </el-splitter>
</template>

<style>
.vue-flow__node {
  background-color: var(--ep-bg-color-page);
}

.vue-flow__node .title {
  text-wrap: nowrap;
}

.vue-flow__node.ct-un-focusable {
  filter: grayscale(1);
  cursor: not-allowed;
  box-shadow: 0 0 10px var(--ep-color-warning-dark-2);
}
</style>

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

.clock-toolbar {
  display: flex;
  flex: 1;
  align-items: center;
  flex-direction: column;
  gap: 2px;
  padding: 0px 2px;
  border-right: solid 1px var(--ep-menu-border-color);
  background: var(--ep-bg-color-page);
}

.clock-toolbar .ep-button {
  margin-left: 0;
  height: 32px;
  padding: 0px 0px;
  width: 32px;
}

.clock-toolbar .ep-divider {
  margin: 5px 0px;
}
</style>
