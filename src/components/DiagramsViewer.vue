<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        DiagramsViewer.vue
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
 *  2025-10-22     xqyjlj       initial version
-->

<script setup lang="ts">
import type { Ip } from '~/database'
import { computed, onMounted, shallowRef, watch } from 'vue'
import { useIpManager } from '~/database'
import { useProjectManager, useThemeStore } from '~/utils'

interface PropsType {
  instance: string
}

const props = defineProps<PropsType>()

const projectManager = useProjectManager()
const ipManager = useIpManager()
const themeStore = useThemeStore()

const project = projectManager.get()!

const ip = shallowRef<Ip | null>()
const images = computed((): string[] => ip.value?.diagrams.images.value ?? [])

watch(
  () => props.instance,
  (value: string) => {
    setIp(value)
  },
)

function setIp(instance: string) {
  const parts = instance.split('@')
  let name = ''
  if (parts.length === 1) {
    name = parts[0]
  }
  else if (parts.length === 2) {
    name = parts[0]
  }

  ip.value = ipManager.getPeripheral(project.vendor, name)
}

onMounted(() => {
  setIp(props.instance)
})
</script>

<template>
  <div>
    <template v-if="images.length === 1">
      <el-image :src="`${images[0]}?theme=${themeStore.theme}`" :preview-src-list="images" />
    </template>
    <template v-else-if="images.length >= 1">
      <el-carousel>
        <el-carousel-item v-for="image in images" :key="image">
          <el-image :src="`${image}?theme=${themeStore.theme}`" />
        </el-carousel-item>
      </el-carousel>
    </template>
  </div>
</template>

<style scoped>
::v-deep(.ep-image__inner) {
  object-fit: contain !important;
  max-height: 120px !important;
}
</style>
