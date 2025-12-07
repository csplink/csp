<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        index.vue
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
 *  2025-05-11     xqyjlj       initial version
-->

<script setup lang="ts">
import type { ChipPackageInstance } from '~/components/instance'
import { nextTick, onBeforeUnmount, onMounted, shallowReactive, shallowRef, watch } from 'vue'
import { useIpManager } from '~/database'
import { useProjectManager } from '~/utils'

const projectManager = useProjectManager()
const ipManager = useIpManager()

const project = projectManager.get()!

const chipPackageRef = shallowRef<ChipPackageInstance>()
const ipInfoRef = shallowReactive({
  ip: '',
  containers: [] as string[],
  channel: '',
})
let stopConfigurationsWatchHandle: (() => void) | null = null

function handZoomIn() {
  chipPackageRef.value?.zoomIn()
}

function handRescale() {
  chipPackageRef.value?.rescale()
}

function handZoomOut() {
  chipPackageRef.value?.zoomOut()
}

async function handDownload() {
  chipPackageRef.value?.rescale() /* !< 强制重新缩放，否则会导致下载的图像不正确 */
  await nextTick()
  chipPackageRef.value?.downloadSvg()
}

function handModuleTreeClick(name: string) {
  const ip = ipManager.getPeripheral(project.vendor, name)

  chipPackageRef.value?.highlightByNames([])
  stopConfigurationsWatch()
  const containers = []

  if (!ip) {
    console.error(`The ip '${name}' is not found.`)
    return
  }

  if (Object.keys(ip.containers.overview.refParameters.value).length > 0) {
    containers.push('overview')
  }
  if (Object.keys(ip.containers.modes.refParameters.value).length > 0) {
    containers.push('modes')
  }
  if (Object.keys(ip.containers.configurations.refParameters.value).length > 0 || ip.diagrams.images.value.length > 0) {
    containers.push('configurations')
  }

  stopConfigurationsWatchHandle = watch(
    () => [ip.containers.configurations.refParameters.value, ip.diagrams.images.value],
    () => {
      handModuleTreeClick(name)
    },
    { immediate: false },
  )

  ipInfoRef.ip = name
  ipInfoRef.containers = containers
  ipInfoRef.channel = ''
}

function handModuleTreeCommand(command: string, args: any) {
  chipPackageRef.value?.highlightByNames([])
  if (command === 'highlight') {
    chipPackageRef.value?.highlightBySignals(args)
  }
}

function handIpConfiguratorPinSelect(pins: string[]) {
  chipPackageRef.value?.highlightByNames(pins)
}

function handIpConfiguratorSelect(pins: string[]) {
  if (pins.length > 0) {
    ipInfoRef.channel = pins[0]
  }
  else {
    ipInfoRef.channel = ''
  }
}

function stopConfigurationsWatch() {
  if (stopConfigurationsWatchHandle) {
    stopConfigurationsWatchHandle()
    stopConfigurationsWatchHandle = null
  }
}

onMounted(() => {
})

onBeforeUnmount(() => {
  stopConfigurationsWatch()
})
</script>

<template>
  <el-splitter>
    <el-splitter-panel min="250" size="250">
      <ModuleTree
        @click="handModuleTreeClick"
        @command="handModuleTreeCommand"
      />
    </el-splitter-panel>
    <el-splitter-panel min="5%" size="30%">
      <el-splitter layout="vertical">
        <el-splitter-panel v-for="container in ipInfoRef.containers" :key="container">
          <el-card>
            <template #header>
              {{ $t(`chipConfigure.${container}`) }}
            </template>
            <IpConfigurator
              :instance="ipInfoRef.ip"
              :type="container"
              channel=""
              @pin-select="handIpConfiguratorPinSelect"
              @select="handIpConfiguratorSelect"
            />
          </el-card>
        </el-splitter-panel>
        <!-- channel 用于修改外设多通道场景，例如 GPIO 的 pin -->
        <el-splitter-panel v-if="ipInfoRef.channel">
          <el-card>
            <template #header>
              {{ ipInfoRef.channel }} {{ $t(`chipConfigure.configurations`) }}
            </template>
            <IpConfigurator
              :instance="`${ipInfoRef.ip}@${ipInfoRef.channel}`"
              type="channel"
              @pin-select="handIpConfiguratorPinSelect"
              @select="handIpConfiguratorSelect"
            />
          </el-card>
        </el-splitter-panel>
      </el-splitter>
    </el-splitter-panel>
    <el-splitter-panel min="20%" size="60%">
      <div class="chip-package-div flex">
        <ChipPackage ref="chipPackageRef" />
      </div>
      <div class="my-4 items-center justify-center" style="text-align: center;">
        <el-tooltip :content="$t('command.zoomIn')">
          <el-button circle @click="handZoomIn">
            <el-icon><i class="ri-zoom-in-line" /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.fullScreen')">
          <el-button circle @click="handRescale">
            <el-icon><i class="ri-fullscreen-line" /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.zoomOut')">
          <el-button circle @click="handZoomOut">
            <el-icon><i class="ri-zoom-out-line" /></el-icon>
          </el-button>
        </el-tooltip>
        <el-tooltip :content="$t('command.export')">
          <el-button circle @click="handDownload">
            <el-icon><i class="ri-export-line" /></el-icon>
          </el-button>
        </el-tooltip>
      </div>
    </el-splitter-panel>
  </el-splitter>
</template>

<style scoped>
.ep-splitter {
  position: static;
  display: flex;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-splitter-panel) {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-card) {
  flex-direction: column;
  display: flex;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-card__header) {
  padding: 10px 20px;
  background-color: var(--ep-menu-hover-bg-color);
  color: var(--ep-menu-hover-text-color);
}

::v-deep(.ep-card__body) {
  padding: 0px;
  display: flex;
  min-width: 0;
  min-height: 0;
}

.chip-package-div {
  flex: 1;
  min-width: 0;
  min-height: 0;
}
</style>
