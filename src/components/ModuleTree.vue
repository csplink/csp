<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ModuleTree.vue
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
 *  2025-05-31     xqyjlj       initial version
-->

<script setup lang="ts">
import type { MenuOptions } from '@imengyu/vue3-context-menu'
import type { ElTree, TreeNode } from 'element-plus'
import type { Project, Summary, SummaryModuleUnit } from '~/database'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useIpManager, useProjectManager, useSummaryManager } from '~/database'

interface TreeType {
  key: string
  label: string
  highlight: boolean
  description?: string
  define?: string
  children?: TreeType[]
}

const emit = defineEmits(['click', 'command'])

const defaultProps = {
  children: 'children',
  label: 'label',
}

const projectManager = useProjectManager()
const summaryManager = useSummaryManager()
const ipManager = useIpManager()
const i18n = useI18n()
const { t } = i18n

const defaultExpandedKeys = ref<string[]>([])
const treeModelRef = ref<TreeType[]>([])
const summaryRef = ref<Summary>()
const projectRef = ref<Project>()
const treeModelsMapRef = ref<Record<string, TreeType>>({})
const menuHighlightActionModels = ref<string[]>([])
const menuShowRef = ref(false)
const menuOptionsComponentRef = ref<MenuOptions>({
  x: 0,
  y: 0,
  minWidth: 230,
})

async function loadModules() {
  if (!projectRef.value || !summaryRef.value) {
    return
  }
  const project = projectRef.value
  const summary = summaryRef.value

  const peripherals = summary.modules.peripherals
  const middlewares = summary.modules.middlewares

  function convertToTree(modules: Record<string, SummaryModuleUnit>, parent: string): TreeType[] {
    return Object.entries(modules).map(([name, module]) => {
      const node_key = `${parent}.${name}`
      const highlight = project.modules.includes(name)
      defaultExpandedKeys.value.push(node_key)
      const node: TreeType = {
        key: node_key,
        label: name,
        highlight,
        description: module.description.get(i18n.locale.value),
        define: module.define,
      }
      treeModelsMapRef.value[name] = node
      if (module.children) {
        node.children = convertToTree(module.children, node_key)
      }

      return node
    })
  }

  const peripheralsTree = convertToTree(peripherals, 'peripherals')
  const middlewaresTree = convertToTree(middlewares, 'middlewares')

  treeModelRef.value = [
    {
      key: 'peripherals',
      label: t('moduleTree.peripherals'),
      highlight: false,
      children: peripheralsTree,
    },
    {
      key: 'middlewares',
      label: t('moduleTree.middlewares'),
      highlight: false,
      children: middlewaresTree,
    },
  ]

  defaultExpandedKeys.value.push('peripherals')
}

function handleNodeClick(data: TreeType) {
  emit('click', data.label)
}

function onProjectModulesChanged(payload: { oldValue: string[], newValue: string[] }) {
  const [oldValue, newValue] = [payload.oldValue, payload.newValue]
  if (oldValue.length > newValue.length) {
    const only = oldValue.filter(x => !newValue.includes(x))
    for (const module of only) {
      treeModelsMapRef.value[module].highlight = false
    }
  }
  else {
    const only = newValue.filter(x => !oldValue.includes(x))
    for (const module of only) {
      treeModelsMapRef.value[module].highlight = true
    }
  }
}

function handleContextMenu(event: MouseEvent, data: TreeType, _node: TreeNode, _component: InstanceType<typeof ElTree>) {
  event.preventDefault()

  const name = data.label
  const project = projectRef.value
  if (!project) {
    return
  }
  const ip = ipManager.getPeripheral(project.vendor, name)
  if (ip) {
    menuHighlightActionModels.value = ip.signals
  }
  else {
    menuHighlightActionModels.value = []
  }

  const position = { x: event.clientX, y: event.clientY }

  /* FIXME: 调用会发出警告
   * [Violation] Added non-passive event listener to a scroll-blocking 'wheel' event.
   * Consider marking event handler as 'passive' to make the page more responsive.
   * See https://www.chromestatus.com/feature/5745543795965952
   */
  setTimeout(() => {
    menuOptionsComponentRef.value.x = position.x
    menuOptionsComponentRef.value.y = position.y
    menuShowRef.value = true
  }, 1)
}

function handCommand(command: string) {
  emit('command', command, menuHighlightActionModels.value)
}

onMounted(async () => {
  const project = projectManager.get()
  if (project) {
    projectRef.value = project
    const summary = summaryManager.get(project.vendor, project.targetChip)
    if (summary) {
      summaryRef.value = summary
      loadModules()
    }
    project.emitter.on('modulesChanged', onProjectModulesChanged)
  }
})

onBeforeUnmount(() => {
  const project = projectManager.get()
  if (project) {
    project.emitter.off('modulesChanged', onProjectModulesChanged)
  }
})
</script>

<template>
  <div class="tree-div">
    <el-scrollbar class="module-tree-scrollbar">
      <el-tree
        class="module-tree"
        node-key="key"
        :data="treeModelRef"
        :props="defaultProps"
        :default-expanded-keys="defaultExpandedKeys"
        :highlight-current="true"
        @node-click="handleNodeClick"
        @node-contextmenu="handleContextMenu"
      >
        <template #default="{ node, data }">
          <span :class="data.highlight ? 'bg-tree-node-item' : ''">
            {{ node.label }}
          </span>
          <template v-if="data.description">
            <div class="module-tree-node">
              <el-tooltip
                :content="data.description"
                placement="right"
              />
            </div>
          </template>
        </template>
      </el-tree>
    </el-scrollbar>
    <context-menu
      v-model:show="menuShowRef"
      :options="menuOptionsComponentRef"
    >
      <context-menu-item :label="$t('moduleTree.highlight')" :disabled="menuHighlightActionModels.length === 0" @click="handCommand('highlight')" />
    </context-menu>
  </div>
</template>

<style scoped>
.tree-div {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.module-tree-scrollbar {
  flex: 1;
}

.bg-tree-node-item {
  color: var(--ep-color-primary);
}

.module-tree-node {
  display: flex;
  align-items: center;
}
</style>
