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
import type { Ip, Project, Summary } from '~/database'
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { useIpManager, useProjectManager, useSummaryManager } from '~/database'

const projectManager = useProjectManager()
const ipManager = useIpManager()
const summaryManager = useSummaryManager()

const chipPackageRef = ref<ChipPackageInstance>()
const ipInfoRef = ref({
  ip: '',
  containers: [] as string[],
  channel: '',
})
const projectRef = ref<Project>()
const summaryRef = ref<Summary>()
let currentIp: Ip | null = null

function chipPackageZoomIn() {
  chipPackageRef.value?.zoomIn()
}

function chipPackageRescale() {
  chipPackageRef.value?.rescale()
}

function chipPackageZoomOut() {
  chipPackageRef.value?.zoomOut()
}

function handModuleTreeClick(name: string) {
  if (projectRef.value) {
    const project = projectRef.value
    const ip = ipManager.getPeripheral(project.vendor, name)

    cleanUpCurrentIp()
    const containers = []

    if (!ip) {
      console.error(`The ip '${name}' is not found.`)
      return
    }

    currentIp = ip

    if (Object.keys(ip.containers.overview.refParameters).length > 0) {
      containers.push('overview')
    }
    if (Object.keys(ip.containers.modes.refParameters).length > 0) {
      containers.push('modes')
    }
    if (Object.keys(ip.containers.configurations.refParameters).length > 0) {
      containers.push('configurations')
    }

    ip.containers.configurations.emitter.on('changed', onIpContainersChanged)

    ipInfoRef.value = {
      ip: name,
      containers,
      channel: '',
    }
  }
}

function handModuleTreeCommand(command: string, args: any) {
  if (command === 'highlight') {
    chipPackageRef.value?.highlightBySignals(args)
  }
}

function handIpConfiguratorPinSelect(pins: string[]) {
  chipPackageRef.value?.highlightByNames(pins)
}

function handIpConfiguratorSelect(pins: string[]) {
  if (pins.length > 0) {
    ipInfoRef.value.channel = pins[0]
  }
  else {
    ipInfoRef.value.channel = ''
  }
}

function onIpContainersChanged() {
  handModuleTreeClick(currentIp?.instance ?? '')
}

function cleanUpCurrentIp() {
  if (currentIp) {
    currentIp.containers.configurations.emitter.off('changed', onIpContainersChanged)
    currentIp = null
  }
}

onMounted(async () => {
  const project = projectManager.get()
  if (project) {
    projectRef.value = project
    const summary = summaryManager.get(project.vendor, project.targetChip)
    if (summary) {
      summaryRef.value = summary
    }
  }
})

onBeforeUnmount(() => {
  cleanUpCurrentIp()
})
</script>

<template>
  <el-splitter>
    <el-splitter-panel min="5%">
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
        <el-splitter-panel v-if="ipInfoRef.channel">
          <el-card>
            <template #header>
              {{ ipInfoRef.channel }} {{ $t(`chipConfigure.configurations`) }}
            </template>
            <IpConfigurator
              :instance="ipInfoRef.ip"
              type="channel"
              :channel="ipInfoRef.channel"
              @pin-select="handIpConfiguratorPinSelect"
              @select="handIpConfiguratorSelect"
            />
          </el-card>
        </el-splitter-panel>
      </el-splitter>
    </el-splitter-panel>
    <el-splitter-panel min-size="20%" size="56%">
      <div class="chip-package-div flex">
        <ChipPackage ref="chipPackageRef" />
      </div>
      <div class="my-4 items-center justify-center">
        <el-button circle @click="chipPackageZoomIn">
          <el-icon><ZoomIn /></el-icon>
        </el-button>
        <el-button circle @click="chipPackageRescale">
          <el-icon><FullScreen /></el-icon>
        </el-button>
        <el-button circle @click="chipPackageZoomOut">
          <el-icon><ZoomOut /></el-icon>
        </el-button>
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
