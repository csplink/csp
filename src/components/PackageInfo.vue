<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PackageInfo.vue
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
 *  2025-08-03     xqyjlj       initial version
-->

<script setup lang="ts">
import type { PackageDescription } from '~/utils'
import { Link } from '@element-plus/icons-vue'
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { openUrl } from '~/utils'

interface PropsType {
  description: PackageDescription
}

const props = defineProps<PropsType>()
const i18n = useI18n()

const vendorUrl = computed(() => props.description.vendorUrl.get(i18n.locale.value))
const descriptionText = computed(() => props.description.description.get(i18n.locale.value))
const url = computed(() => props.description.url?.get(i18n.locale.value))
</script>

<template>
  <div class="package-info-container">
    <el-card class="package-info-card">
      <template #header>
        <div class="card-header">
          <h2>{{ props.description.name }}</h2>
          <el-tag type="success" size="small">
            {{ props.description.version }}
          </el-tag>
        </div>
      </template>

      <el-descriptions
        :column="2"
        :border="true"
      >
        <el-descriptions-item :label="$t('packageInfo.type')">
          <el-tag size="small">
            {{ props.description.type }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item :label="$t('packageInfo.license')">
          <el-tag type="warning" size="small">
            {{ props.description.license }}
          </el-tag>
        </el-descriptions-item>

        <el-descriptions-item :label="$t('packageInfo.vendor')" :span="2">
          <div class="vendor-info">
            <span>{{ props.description.vendor }}</span>
            <el-link
              v-if="vendorUrl"
              type="primary"
              underline="never"
              @click="openUrl(vendorUrl)"
            >
              <el-icon class="el-icon--right">
                <i class="ri-external-link-line" />
              </el-icon>
            </el-link>
          </div>
        </el-descriptions-item>

        <el-descriptions-item :label="$t('packageInfo.description')" :span="2">
          <div class="description-text">
            {{ descriptionText }}
          </div>
        </el-descriptions-item>

        <el-descriptions-item :label="$t('packageInfo.support')" :span="2">
          <el-tag type="info" size="small">
            {{ props.description.support }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <div class="divider">
        <el-divider content-position="center">
          {{ $t('packageInfo.authorInfo') }}
        </el-divider>
      </div>

      <el-descriptions
        :column="2"
        :border="true"
      >
        <el-descriptions-item :label="$t('packageInfo.author')">
          {{ props.description.author.name }}
        </el-descriptions-item>

        <el-descriptions-item :label="$t('packageInfo.email')">
          <el-link
            type="primary"
            underline="never"
            @click="openUrl(`mailto:${props.description.author.email}`)"
          >
            {{ props.description.author.email }}
          </el-link>
        </el-descriptions-item>

        <el-descriptions-item v-if="props.description.author.website.blog" :label="$t('packageInfo.blog')">
          <el-link
            type="success"
            underline="never"
            @click="openUrl(props.description.author.website.blog)"
          >
            <el-icon class="el-icon--left">
              <i class="ri-user-line" />
            </el-icon>
            {{ $t('packageInfo.visitBlog') }}
          </el-link>
        </el-descriptions-item>

        <el-descriptions-item v-if="props.description.author.website.github" label="GitHub">
          <el-link
            type="info"
            underline="never"
            @click="openUrl(props.description.author.website.github)"
          >
            <el-icon class="el-icon--left">
              <i class="ri-share-fill" />
            </el-icon>
            {{ $t('packageInfo.visitGitHub') }}
          </el-link>
        </el-descriptions-item>
      </el-descriptions>

      <div v-if="props.description.url" class="package-links">
        <el-divider content-position="center">
          {{ $t('packageInfo.relatedLinks') }}
        </el-divider>
        <el-button
          type="primary"
          :icon="Link"
          round
          @click="openUrl(url)"
        >
          <template #icon>
            <el-icon><i class="ri-link" /></el-icon>
          </template>
          {{ $t('packageInfo.visitProjectHomepage') }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<style scoped>
.package-info-container {
  padding: 16px;
  flex: 1;
}

.package-info-card {
  border-radius: 8px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.card-header h2 {
  margin: 0;
  font-size: 1.5rem;
  color: var(--el-text-color-primary);
}

.vendor-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.description-text {
  line-height: 1.6;
  white-space: pre-wrap;
}

.divider {
  margin: 20px 0;
}

.package-links {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
