<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CodeFileTree.vue
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
 *  2025-07-11     xqyjlj       initial version
-->
<script setup lang="ts">
import type { MenuOptions } from '@imengyu/vue3-context-menu'
import type { ElTree, TreeNode } from 'element-plus'
import { onBeforeUnmount, onMounted, shallowReactive, shallowRef, watch } from 'vue'

interface TreeType {
  key: string
  label: string
  type: string
  highlight: boolean
  children?: TreeType[]
}
interface PropsType {
  files: {
    [k: string]: boolean
  }
}

const props = defineProps<PropsType>()
const emit = defineEmits(['content', 'diff', 'save', 'generate'])

const defaultProps = {
  children: 'children',
  label: 'label',
}

const treeModelRef = shallowRef<TreeType[]>([])
const menuShowRef = shallowRef(false)
const menuCurrentDataRef = shallowRef<TreeType>()
const menuOptionsComponentRef = shallowReactive<MenuOptions>({
  x: 0,
  y: 0,
  minWidth: 230,
})

watch(
  () => [props.files],
  () => {
    treeModelRef.value = buildTreeFromPaths(props.files)
  },
)

function getFileType(file: string) {
  const ext = file.split('.').pop() ?? ''

  switch (ext) {
    case 'c':
    case 'h':
      return 'c'
    case 'cpp':
    case 'hpp':
      return 'cpp'
    case 's':
    case 'S':
      return 'armasm'
    case 'ld':
    case 'lds':
      return 'linker-script'
    case 'yaml':
    case 'yml':
      return 'yaml'
    case 'json':
      return 'json'
    case 'xml':
    case 'uvprojx':
      return 'xml'
    case 'gitignore':
      return 'gitignore'
    case 'lua':
      if (file === 'xmake.lua') {
        return 'xmake'
      }
      return 'lua'
    case 'xmake':
      return 'xmake'
    case 'txt':
      if (file === 'CMakeLists.txt') {
        return 'cmake'
      }
      return ''
    case 'cmake':
      return 'cmake'
    default:
      return ''
  }
}

function buildTreeFromPaths(files: Record<string, boolean>): TreeType[] {
  const root: TreeType[] = []

  for (const [path, diff] of Object.entries(files)) {
    const parts = path.split('/')
    let currentLevel = root
    let currentPath = ''

    for (let i = 0; i < parts.length; i++) {
      const part = parts[i]
      currentPath = currentPath ? `${currentPath}/${part}` : part

      let existing = currentLevel.find(node => node.label === part)

      if (!existing) {
        existing = {
          key: currentPath,
          label: part,
          type: getFileType(part),
          highlight: diff,
          children: [],
        }
        currentLevel.push(existing)
      }

      if (i === parts.length - 1) {
        delete existing.children
      }
      else {
        currentLevel = existing.children!
      }
    }
  }
  sortTree(root)
  return root
}

function sortTree(nodes: TreeType[]) {
  nodes.sort((a, b) => {
    const aIsFolder = !!a.children
    const bIsFolder = !!b.children

    if (aIsFolder && !bIsFolder)
      return -1
    if (!aIsFolder && bIsFolder)
      return 1
    return a.label.localeCompare(b.label)
  })

  for (const node of nodes) {
    if (node.children) {
      sortTree(node.children)
    }
  }
}

function handleNodeClick(data: TreeType) {
  if (data.children === undefined) {
    emit('content', data.key, data.type)
  }
}

function handleContextMenu(event: MouseEvent, data: TreeType, _node: TreeNode, _component: InstanceType<typeof ElTree>) {
  event.preventDefault()

  menuCurrentDataRef.value = data

  const position = { x: event.clientX, y: event.clientY }

  setTimeout(() => {
    menuOptionsComponentRef.x = position.x
    menuOptionsComponentRef.y = position.y
    menuShowRef.value = true
  }, 1)
}

function collectAllKeys(root: TreeType): string[] {
  const result: string[] = []

  function traverse(node: TreeType) {
    if (node.children === undefined) {
      result.push(node.key)
    }
    else {
      for (const child of node.children) {
        traverse(child)
      }
    }
  }

  traverse(root)
  return result
}

function handSaveAsCommand() {
  const data = menuCurrentDataRef.value
  if (!data) {
    return
  }

  if (data.children) {
    emit('save', collectAllKeys(data), data.label)
  }
  else {
    emit('save', [data.key], data.label)
  }
}

function handGenerateCommand() {
  const data = menuCurrentDataRef.value
  if (!data) {
    return
  }

  if (data.children) {
    emit('generate', collectAllKeys(data))
  }
  else {
    emit('generate', [data.key])
  }
}

function handDiffMenuCommand() {
  const data = menuCurrentDataRef.value
  if (!data) {
    return
  }

  emit('diff', data.key)
}

onMounted(() => {
  treeModelRef.value = buildTreeFromPaths(props.files)
})

onBeforeUnmount(() => {
})
</script>

<template>
  <div class="tree-div">
    <el-scrollbar class="tree-scrollbar">
      <el-tree
        class="file-tree"
        node-key="key"
        :data="treeModelRef"
        :props="defaultProps"
        :highlight-current="true"
        :default-expand-all="true"
        :expand-on-click-node="false"
        @current-change="handleNodeClick"
        @node-contextmenu="handleContextMenu"
      >
        <template #default="{ node, data }">
          <div class="tree-node-icon mr-2">
            <template v-if="data.children">
              <MaterialFolderSrc />
            </template>
            <template v-else-if="data.type === 'c'">
              <MaterialC />
            </template>
            <template v-else-if="data.type === 'cpp'">
              <MaterialCpp />
            </template>
            <template v-else-if="data.type === 'armasm'">
              <MaterialAssembly />
            </template>
            <template v-else-if="data.type === 'yaml'">
              <MaterialYaml />
            </template>
            <template v-else-if="data.type === 'json'">
              <MaterialJson />
            </template>
            <template v-else-if="data.type === 'xml'">
              <MaterialXml />
            </template>
            <template v-else-if="data.type === 'gitignore'">
              <MaterialGit />
            </template>
            <template v-else-if="data.type === 'lua'">
              <MaterialLua />
            </template>
            <template v-else-if="data.type === 'xmake'">
              <MaterialXmake />
            </template>
            <template v-else-if="data.type === 'cmake'">
              <MaterialCmake />
            </template>
            <template v-else>
              <MaterialFile />
            </template>
          </div>
          <span :class="data.highlight ? 'bg-tree-node-item' : ''">
            {{ node.label }}
          </span>
        </template>
      </el-tree>
    </el-scrollbar>
    <context-menu
      v-model:show="menuShowRef"
      :options="menuOptionsComponentRef"
    >
      <context-menu-item icon="ri-ai-generate" :label="$t('command.generate')" @click="handGenerateCommand()" />
      <context-menu-item icon="ri-save-3-line" :label="$t('command.saveAs')" @click="handSaveAsCommand()" />
      <context-menu-separator />
      <context-menu-item icon="ri-exchange-2-line" :label="$t('command.diff')" :disabled="(!menuCurrentDataRef?.highlight) || menuCurrentDataRef?.children !== undefined" @click="handDiffMenuCommand()" />
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
</style>
