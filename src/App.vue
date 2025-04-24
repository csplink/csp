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
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const i18n = useI18n()
const locale = computed(() => (i18n.messages.value[i18n.locale.value] as import('element-plus/es/locale').Language))
</script>

<template>
  <el-config-provider namespace="ep" :locale="locale">
    <TitleHeader />
    <div class="main_window flex">
      <NavigationSide />
      <RouterView v-slot="{ Component }">
        <KeepAlive>
          <Component :is="Component" />
        </KeepAlive>
      </RouterView>
    </div>
  </el-config-provider>
</template>

<style>
html,
body,
#app {
  text-align: center;
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
