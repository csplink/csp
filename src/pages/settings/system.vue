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
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import pkg from '~/../package.json'
import { useSettingsManager } from '~/utils'

const { t } = useI18n()
const settings = useSettingsManager().settings

const themeOptions = computed(() => [
  { label: t('label.light'), value: 'light' },
  { label: t('label.dark'), value: 'dark' },
  { label: t('label.autoTheme'), value: 'auto' },
])

const langOptions = [
  { label: '简体中文', value: 'zh-cn' },
  { label: 'English', value: 'en' },
]

const formModel = {
  theme: settings.system.theme,
  themeColor: settings.system.themeColor,
  language: settings.system.language,
  autoUpdate: settings.system.autoUpdate,
  telemetry: settings.system.telemetry,
  crashReports: settings.system.crashReports,
  autoSave: settings.system.autoSave,
}
</script>

<template>
  <div class="g-settings-container">
    <el-form :model="formModel" label-position="left" label-width="auto">
      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.personalization') }}
        </h2>
        <el-form-item class="g-settings-item" :label="$t('label.applicationTheme')">
          <el-select v-model="formModel.theme.value">
            <el-option
              v-for="option in themeOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.themeColor')">
          <el-color-picker v-model="formModel.themeColor.value" show-alpha />
        </el-form-item>
      </div>

      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.system') }}
        </h2>
        <el-form-item class="g-settings-item" :label="$t('label.language')">
          <el-select v-model="formModel.language.value" class="settings-select">
            <el-option
              v-for="option in langOptions"
              :key="option.value"
              :label="option.label"
              :value="option.value"
            />
          </el-select>
        </el-form-item>
      </div>

      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.softwareUpdate') }}
        </h2>
        <el-form-item class="g-settings-item">
          <el-switch
            v-model="formModel.autoUpdate.value"
            :active-text="$t('label.autoUpdate')"
          />
        </el-form-item>
      </div>

      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.privacy') }}
        </h2>
        <el-form-item class="g-settings-item">
          <el-switch
            v-model="formModel.telemetry.value"
            :active-text="$t('label.telemetry')"
          />
        </el-form-item>
        <el-form-item class="g-settings-item">
          <el-switch
            v-model="formModel.crashReports.value"
            :active-text="$t('label.crashReports')"
          />
        </el-form-item>
      </div>

      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.about') }}
        </h2>
        <el-descriptions class="g-settings-item" :column="1" :border="true">
          <el-descriptions-item :label="$t('label.version')">
            {{ pkg.version }}
          </el-descriptions-item>
          <el-descriptions-item :label="$t('label.license')">
            Apache License 2.0
          </el-descriptions-item>
          <el-descriptions-item :label="$t('label.author')">
            xqyjlj
          </el-descriptions-item>
        </el-descriptions>
      </div>

      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('startup.contributors') }}
        </h2>
        <ContributorsList />
      </div>
    </el-form>
  </div>
</template>
