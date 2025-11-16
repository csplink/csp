<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        IpConfigurator.vue
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
 *  2025-08-28     xqyjlj       initial version
-->

<script setup lang="ts">
interface PropsType {
  type: string
  instance: string
}

defineProps<PropsType>()
const emit = defineEmits(['pinSelect', 'select'])

function handlePinSelect(pins: string[]) {
  emit('pinSelect', pins)
}

function handleSelect(selection: string[]) {
  emit('select', selection)
}
</script>

<template>
  <div class="ip-configurator-div">
    <DiagramsViewer v-if="type === 'configurations'" :instance="instance" />

    <IpConfiguratorTable
      v-if="type === 'overview'"
      :instance="instance"
      @pin-select="handlePinSelect"
      @select="handleSelect"
    />

    <IpConfiguratorForm
      v-else
      :type="(type as 'modes' | 'configurations' | 'channel')"
      :instance="instance"
      @pin-select="handlePinSelect"
      @select="handleSelect"
    />
  </div>
</template>

<style scoped>
.ip-configurator-div {
  flex: 1;
  display: flex;
  flex-direction: column;
}
</style>
