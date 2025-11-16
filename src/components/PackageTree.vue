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
import type { PackageIndex } from '~/utils'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { usePackageManager } from '~/utils'

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

const packageIndexRef = ref<PackageIndex>()
const defaultExpandedKeys = ref<string[]>([])
const treeModelRef = ref<TreeType[]>([])

async function loadModules() {
  if (!packageIndexRef.value) {
    return
  }

  defaultExpandedKeys.value = []

  const tree: TreeType[] = []
  for (const [type, value1] of Object.entries(packageIndexRef.value.origin)) {
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

  treeModelRef.value = tree
}

function handleNodeClick(data: TreeType) {
  if (data.type === 'version') {
    emit('click', data.kind, data.name, data.version)
  }
}

onMounted(async () => {
  packageIndexRef.value = packageManager.packageIndex
  loadModules()
})

onBeforeUnmount(() => {
})
</script>

<template>
  <div class="tree-div">
    <el-scrollbar class="tree-scrollbar">
      <el-tree
        class="tree"
        node-key="key"
        :data="treeModelRef"
        :props="defaultProps"
        :default-expanded-keys="defaultExpandedKeys"
        :expand-on-click-node="false"
        :highlight-current="true"
        @node-click="handleNodeClick"
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
      </el-tree>
    </el-scrollbar>
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
