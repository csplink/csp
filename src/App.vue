<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        App.vue
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
 *  2025-04-27     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { ProcessRunModeType } from '@/electron/types'
import type { TitleMenuBarInstance } from './components/instance'
import { computed, onMounted, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSystemStore } from '~/utils'

const i18n = useI18n()

const systemRunMode = shallowRef<ProcessRunModeType>('startup')
const menuBar = shallowRef<TitleMenuBarInstance>()

const locale = computed(() => (i18n.messages.value[i18n.locale.value] as import('element-plus/es/locale').Language))
const showMenuTitle = computed(() => systemRunMode.value === 'main')

onMounted(() => {
  const runMode = useSystemStore().args.runMode
  systemRunMode.value = runMode
})
</script>

<template>
  <el-config-provider namespace="ep" :locale="locale">
    <TitleHeader :show-menu="showMenuTitle" :show-title="showMenuTitle">
      <TitleMenuBar ref="menuBar" />
    </TitleHeader>
    <div class="main_window flex">
      <template v-if="systemRunMode === 'main'">
        <NavigationSide
          @generate="() => menuBar?.generate()"
        />
      </template>
      <el-splitter layout="vertical">
        <el-splitter-panel>
          <RouterView v-slot="{ Component }">
            <KeepAlive>
              <Component :is="Component" />
            </KeepAlive>
          </RouterView>
        </el-splitter-panel>
        <el-splitter-panel v-if="systemRunMode === 'main'" size="250">
          <el-tabs type="border-card">
            <el-tab-pane :label="$t('label.logs')">
              <LogViewer />
            </el-tab-pane>
            <el-tab-pane :label="$t('label.problems')">
              User
            </el-tab-pane>
          </el-tabs>
        </el-splitter-panel>
      </el-splitter>
    </div>
  </el-config-provider>
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
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.ep-tabs {
  flex: 1;
  display: flex;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-tabs__content) {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

::v-deep(.ep-tab-pane) {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}
</style>

<style>
html,
body,
#app {
  color: var(--ep-text-color-primary);
  display: flex;
  flex-direction: column;
  width: 100vw;
  height: 100vh;
}

.main_window {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 0;
}
</style>
