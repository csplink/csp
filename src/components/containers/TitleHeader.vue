<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        TitleHeader.vue
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
 *  2025-04-25     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { ProcessRunModeType } from '@/electron/types'
import { onBeforeUnmount, onMounted, shallowRef } from 'vue'
import { useSystemStore } from '~/utils'

interface PropsType {
  showMenu: boolean
  showTitle: boolean
}
const props = defineProps<PropsType>()

const systemRunMode = shallowRef<ProcessRunModeType>('startup')
const title = shallowRef(document.title)

let titleObserver: MutationObserver

onMounted(() => {
  systemRunMode.value = useSystemStore().args.runMode

  titleObserver = new MutationObserver(() => {
    title.value = document.title
  })

  const titleElement = document.querySelector('title')
  if (titleElement) {
    titleObserver.observe(titleElement, { childList: true })
  }
})

onBeforeUnmount(() => {
  if (titleObserver) {
    titleObserver.disconnect()
  }
})
</script>

<template>
  <div class="window-titlebar window-title-drag">
    <div class="window-title-drag window-title-left flex items-center justify-center">
      <el-image class="window-title-drag window-app-icon" style="width: 18px; height: 18px" src="./images/logo.svg" />
      <template v-if="props.showMenu">
        <div class="window-title-no-drag">
          <slot />
        </div>
      </template>
    </div>
    <template v-if="props.showTitle">
      <div class="window-title-drag window-title-center">
        {{ title }}
      </div>
    </template>
    <div class="window-title-drag draggable-area" />
    <div class="window-title-no-drag window-controls-container" />
  </div>
</template>

<style lang="scss" scoped>
.window-titlebar {
  height: 35px;
  background: var(--ep-bg-color-page);
  display: flex;
  align-items: center;
  flex-shrink: 0;
  border-bottom: 1px solid var(--ep-menu-border-color);
}

.window-title-drag {
  -webkit-app-region: drag;
}

.window-title-no-drag {
  -webkit-app-region: no-drag;
}

.window-title-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  min-width: max-content;
}

.window-app-icon {
  padding: 0px 9px;
}

.window-title-center {
  flex: 1;
  text-align: center;
  color: var(--ep-text-color-primary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.draggable-area {
  flex: 0;
}

.window-controls-container {
  width: 150px;
  flex-shrink: 0;
}

::v-deep(.mx-menu-bar-content) {
  align-items: center;
  display: flex;
}

::v-deep(.mx-menu-bar-item) {
  display: flex;
  align-items: center;
  padding-top: 5px;
}
</style>
