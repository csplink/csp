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
 *  2025-05-18     xqyjlj       initial version
-->

<script setup lang="ts">
import { onActivated, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRoute, useRouter } from 'vue-router'

const { t } = useI18n()
const router = useRouter()
const route = useRoute()

interface CategoriesType {
  [key: string]: {
    title: string
    icon: string
  }
}

const categoriesRef = ref<CategoriesType>({
  system: { title: t('settings.systemSetting'), icon: 'Setting' },
  generate: { title: t('settings.generateSetting'), icon: 'Setting' },
})

const activeCategoryRef = ref('system')

function handleSelect(key: string) {
  if (activeCategoryRef.value !== key) {
    activeCategoryRef.value = key
    router.push(`/settings/${key}`)
  }
}

onActivated(() => {
  if (route.path === '/settings/system' && activeCategoryRef.value !== 'system') {
    router.push(`/settings/${activeCategoryRef.value}`)
  }
})
</script>

<template>
  <div class="setting-container">
    <div class="setting-sidebar">
      <el-menu
        class="setting-menu"
        :default-active="activeCategoryRef"
        @select="handleSelect"
      >
        <el-menu-item v-for="[key, category] in Object.entries(categoriesRef)" :key="key" :index="key">
          <el-icon><component :is="category.icon" /></el-icon>
          <span>{{ category.title }}</span>
        </el-menu-item>
      </el-menu>
    </div>
    <div class="setting-main">
      <h1>{{ categoriesRef[activeCategoryRef].title }}</h1>
      <el-divider />

      <el-scrollbar class="setting-scrollbar">
        <RouterView />
      </el-scrollbar>
    </div>
  </div>
</template>

<style scoped>
@import '~/styles/element/settings.scss';

.setting-container {
  display: flex;
  flex: 1;
}

.setting-sidebar {
  display: flex;
}

.setting-menu {
  width: 200px;
}

.setting-main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.setting-main h1 {
  text-align: left;
  margin-left: 20px;
}

.setting-scrollbar {
  flex: 1;
}
</style>
