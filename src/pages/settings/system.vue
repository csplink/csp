<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        system.vue
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
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

// interface CategoriesType {
//   [key: string]: {
//     title: string
//     icon: string
//   }
// }

// const categories = ref<CategoriesType>({
//   system: { title: t('settings.systemSetting'), icon: 'Setting' },
// })
// const activeCategoryRef = ref('system')
const langOptions = ref([
  { label: '简体中文', value: 'zh-cn' },
  { label: 'English', value: 'en' },
])
const themeOptions = ref([
  { label: t('settings.light'), value: 'light' },
  { label: t('settings.dark'), value: 'dark' },
  { label: t('settings.autoTheme'), value: 'dark' },
])
</script>

<template>
  <div class="setting-content">
    <h2>{{ $t('settings.personalization') }}</h2>
    <el-card shadow="never">
      <el-row :gutter="20">
        <el-col class="label-col" :span="20">
          <el-text>
            {{ $t('settings.applicationTheme') }}
          </el-text>
        </el-col>
        <el-col class="widget-col" :span="4">
          <el-select class="settings-options">
            <el-option v-for="(lang, index) in themeOptions" :key="index" :label="lang.label" :value="lang.value" />
          </el-select>
        </el-col>
      </el-row>
      <el-divider />
      <el-row :gutter="20">
        <el-col class="label-col" :span="20">
          <el-text>
            {{ $t('settings.themeColor') }}
          </el-text>
        </el-col>
        <el-col class="widget-col" :span="4">
          <el-color-picker />
        </el-col>
      </el-row>
    </el-card>

    <h2>{{ $t('settings.system') }}</h2>
    <el-card shadow="never">
      <el-row :gutter="20">
        <el-col class="label-col" :span="20">
          <el-text>
            {{ $t('settings.language') }}
          </el-text>
        </el-col>
        <el-col class="widget-col" :span="4">
          <el-select class="settings-options">
            <el-option v-for="(lang, index) in langOptions" :key="index" :label="lang.label" :value="lang.value" />
          </el-select>
        </el-col>
      </el-row>
    </el-card>

    <h2>{{ $t('settings.softwareUpdate') }}</h2>
    <el-card shadow="never">
      <el-row :gutter="20">
        <el-col class="label-col" :span="20">
          <el-text>
            {{ $t('settings.update') }}
          </el-text>
        </el-col>
        <el-col class="widget-col" :span="4">
          <el-switch />
        </el-col>
      </el-row>
    </el-card>

    <h2>{{ $t('settings.about') }}</h2>
    <el-card shadow="never">
      <el-row :gutter="20">
        <el-col class="label-col" :span="20">
          <el-text>
            {{ $t('settings.help') }}
          </el-text>
        </el-col>
        <el-col class="widget-col" :span="4">
          <el-button circle>
            <el-icon><More /></el-icon>
          </el-button>
        </el-col>
      </el-row>
      <el-divider />
      <el-row :gutter="20">
        <el-col class="label-col" :span="20">
          <el-text>
            {{ $t('settings.feedback') }}
          </el-text>
        </el-col>
        <el-col class="widget-col" :span="4">
          <el-button circle>
            <el-icon><More /></el-icon>
          </el-button>
        </el-col>
      </el-row>
      <el-divider />
      <el-row :gutter="20">
        <el-col class="label-col" :span="20">
          <el-text>
            {{ $t('settings.about') }}
          </el-text>
        </el-col>
        <el-col class="widget-col" :span="4">
          <el-button circle>
            <el-icon><More /></el-icon>
          </el-button>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<style scoped>
@import '~/styles/element/settings.scss';
</style>
