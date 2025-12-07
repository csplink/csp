<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PackageTree.vue
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
import type { MenuOptions } from '@imengyu/vue3-context-menu'
import type { TreeNode } from 'element-plus'
import { ElNotification, ElTree } from 'element-plus'
import { onBeforeUnmount, onMounted, ref, shallowReactive, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { usePackageManager, useServerManager } from '~/utils'

interface TreeType {
  key: string
  label: string
  installed: boolean
  type: string
  kind?: string
  name?: string
  version?: string
  children?: TreeType[]
}

const emit = defineEmits(['click'])

const defaultProps = {
  children: 'children',
  label: 'label',
}

const packageManager = usePackageManager()
const severManager = useServerManager()
const i18n = useI18n()
const { t } = i18n

const defaultExpandedKeys = ref<string[]>([])
const treeModelRef = shallowRef<TreeType[]>([])
const menuShowRef = shallowRef(false)
const menuOptionsComponentRef = shallowReactive<MenuOptions>({
  x: 0,
  y: 0,
  minWidth: 230,
})
const currentSelectedNode = shallowRef<TreeType | null>(null)

let stopConfigurationsWatchHandle: (() => void) | null = null

async function loadModules() {
  if (!packageManager.packageIndex.origin.value) {
    return
  }

  defaultExpandedKeys.value = []

  const tree: TreeType[] = []
  for (const [type, value1] of Object.entries(packageManager.packageIndex.origin.value)) {
    const typeTree: TreeType = {
      key: type,
      label: type,
      installed: true,
      type: 'type',
      children: [],
    }
    tree.push(typeTree)
    for (const [name, value2] of Object.entries(value1)) {
      const versionTree: TreeType = {
        key: `${type}.${name}`,
        label: name,
        installed: true,
        type: 'name',
        children: [],
      }
      typeTree.children?.push(versionTree)
      for (const [version, _] of Object.entries(value2)) {
        versionTree.children?.push({
          key: `${type}.${name}.${version}`,
          label: version,
          installed: true,
          type: 'version',
          kind: type,
          name,
          version,
        })
      }
      defaultExpandedKeys.value.push(`${type}.${name}`)
    }
  }

  /* !< 对最终tree进行排序 */
  tree.sort((a, b) => a.label.localeCompare(b.label))
  tree.forEach((typeTree) => {
    if (typeTree.children) {
      typeTree.children.sort((a, b) => a.label.localeCompare(b.label))
      typeTree.children.forEach((nameTree) => {
        if (nameTree.children) {
          nameTree.children.sort((a, b) => a.label.localeCompare(b.label))
        }
      })
    }
  })

  treeModelRef.value = tree
}

function handleNodeClick(data: TreeType) {
  if (data.type === 'version') {
    emit('click', data.kind, data.name, data.version)
  }
}

function handleContextMenu(event: MouseEvent, data: TreeType, _node: TreeNode, _component: InstanceType<typeof ElTree>) {
  event.preventDefault()

  /* !< 只有version类型的节点才能卸载 */
  if (data.type === 'version') {
    currentSelectedNode.value = data
    menuOptionsComponentRef.x = event.clientX
    menuOptionsComponentRef.y = event.clientY
    menuShowRef.value = true
  }
}

async function handUninstall() {
  menuShowRef.value = false

  if (!currentSelectedNode.value || !currentSelectedNode.value.kind || !currentSelectedNode.value.name || !currentSelectedNode.value.version) {
    return
  }

  try {
    await severManager.server.packageUninstall(
      currentSelectedNode.value.kind,
      currentSelectedNode.value.name,
      currentSelectedNode.value.version,
    )

    ElNotification({
      title: t('label.success'),
      message: t('message.uninstallSuccess'),
      duration: 3000,
      offset: 35,
      type: 'success',
    })

    await packageManager.reload()
  }
  catch (error) {
    console.error(t('message.uninstallFailed'), error)
    ElNotification({
      title: t('label.error'),
      message: t('message.uninstallFailed'),
      duration: 0,
      offset: 35,
      type: 'error',
    })
  }

  currentSelectedNode.value = null
}

onMounted(async () => {
  stopConfigurationsWatchHandle = watch(
    () => packageManager.packageIndex.origin.value,
    () => {
      loadModules()
    },
    { immediate: true },
  )
})

onBeforeUnmount(() => {
  if (stopConfigurationsWatchHandle) {
    stopConfigurationsWatchHandle()
    stopConfigurationsWatchHandle = null
  }
})
</script>

<template>
  <div class="tree-div">
    <el-scrollbar class="tree-scrollbar">
      <ElTree
        class="tree"
        node-key="key"
        :data="treeModelRef"
        :props="defaultProps"
        :default-expanded-keys="defaultExpandedKeys"
        :expand-on-click-node="false"
        :highlight-current="true"
        @node-click="handleNodeClick"
        @node-contextmenu="handleContextMenu"
      >
        <template #default="{ node, data }">
          <div class="tree-node-icon mr-2">
            <template v-if="data.type === 'type'">
              <MaterialFolderDist />
            </template>
            <template v-else-if="data.type === 'name'">
              <MaterialFolderBase />
            </template>
            <template v-else-if="data.type === 'version'">
              <MaterialTaskfile />
            </template>
          </div>
          <span :class="data.installed ? 'bg-tree-node-item' : ''">
            {{ node.label }}
          </span>
        </template>
      </ElTree>
    </el-scrollbar>
    <context-menu
      v-model:show="menuShowRef"
      :options="menuOptionsComponentRef"
    >
      <context-menu-item icon="ri-uninstall-line" :label="$t('command.uninstall')" @click="handUninstall()" />
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

.tree-scrollbar {
  flex: 1;
}

.tree-node-icon {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
}

.bg-tree-node-item {
  color: var(--ep-color-primary);
}

.tree-node {
  display: flex;
  align-items: center;
}
</style>
