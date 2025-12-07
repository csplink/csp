<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ChipInfo.vue
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
 *  2025-08-17     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { Summary, SummaryDocumentUnit } from '~/database'
import { ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it'
import { computed, onMounted, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useSummaryManager } from '~/database'
import { openUrl } from '~/utils'

import 'github-markdown-css/github-markdown-light.css'

const props = defineProps({
  chip: {
    type: String,
    default: '',
  },
})

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
})

const i18n = useI18n()
const summaryManager = useSummaryManager()

const { t } = useI18n()
const chipSummary = shallowRef<Summary | null>(null)
const loading = shallowRef(false)
const activeTab = shallowRef('basic')
const docs = shallowRef<Record<string, Record<string, SummaryDocumentUnit>>>({})

const renderedContent = computed(() => {
  return md.render(chipSummary.value?.illustrate.value || '')
})

function processDocuments(summary: Summary): Record<string, Record<string, SummaryDocumentUnit>> {
  const processedDocs: Record<string, Record<string, SummaryDocumentUnit>> = {}

  let title = t('chipInfo.datasheets')
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.datasheets)) {
    processedDocs[title][name] = unit
  }
  title = t('chipInfo.referenceDocs')
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.references)) {
    processedDocs[title][name] = unit
  }
  title = t('chipInfo.errata')
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.errata)) {
    processedDocs[title][name] = unit
  }
  title = t('chipInfo.applicationDocs')
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.applications)) {
    processedDocs[title][name] = unit
  }
  title = t('chipInfo.faqs')
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.faqs)) {
    processedDocs[title][name] = unit
  }

  return processedDocs
}

async function loadChipInfo() {
  const parts = props.chip.split('@')
  if (parts.length <= 1) {
    chipSummary.value = null
    docs.value = {}
    return
  }

  const vendor = parts[0]
  const chipName = parts[1]

  if (!chipName || !vendor) {
    chipSummary.value = null
    docs.value = {}
    return
  }

  loading.value = true
  try {
    let summary = summaryManager.get(vendor, chipName)

    if (!summary) {
      await summaryManager.load(vendor, chipName, i18n.locale)
      summary = summaryManager.get(vendor, chipName)
    }

    chipSummary.value = summary

    if (summary) {
      docs.value = processDocuments(summary)
    }
  }
  catch (error) {
    console.error('Failed to load chip info', error)
    ElMessage.error(t('chipInfo.loadChipInfoFailed'))
  }
  finally {
    loading.value = false
  }
}

watch(
  () => props.chip,
  () => {
    loadChipInfo()
  },
  { immediate: true },
)

onMounted(() => {
  if (props.chip) {
    loadChipInfo()
  }
})
</script>

<template>
  <div class="chip-info-container">
    <el-skeleton v-if="loading" animated :rows="10" />
    <div v-else-if="chipSummary" class="chip-info-content">
      <h2 class="chip-title">
        {{ chipSummary.name }}
      </h2>
      <el-tabs v-model="activeTab" class="chip-tabs">
        <el-tab-pane :label="$t('chipInfo.basicInfo')" name="basic">
          <el-descriptions
            :column="5"
            :border="true"
          >
            <el-descriptions-item :label="$t('chipInfo.name')">
              <div class="url-div" @click="openUrl(chipSummary.url.value)">
                <el-tooltip :content="chipSummary.url.value">
                  {{ chipSummary.name }}
                </el-tooltip>
              </div>
            </el-descriptions-item>
            <el-descriptions-item :label="$t('chipInfo.manufacturer')">
              <div class="url-div" @click="openUrl(chipSummary.vendorUrl.value)">
                <el-tooltip :content="chipSummary.vendorUrl.value">
                  {{ chipSummary.vendor }}
                </el-tooltip>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="IO">
              {{ chipSummary.io }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('chipInfo.price')" />
            <el-descriptions-item :rowspan="2" :label="$t('chipInfo.packageDiagram')">
              <el-tooltip>
                <template #content>
                  <el-image
                    style="max-width: 200px; max-height: 200px"
                    :src="`./images/packages/${chipSummary.package}.png`"
                    fit="contain"
                  />
                </template>
                <el-image
                  style="width: 64px; height: 64px"
                  :src="`/images/packages/${chipSummary.package}.png`"
                />
              </el-tooltip>
            </el-descriptions-item>
            <el-descriptions-item :label="$t('chipInfo.package')">
              {{ chipSummary.package }}
            </el-descriptions-item>
            <el-descriptions-item :label="$t('chipInfo.introduction')">
              {{ chipSummary.introduction }}
            </el-descriptions-item>
          </el-descriptions>

          <el-scrollbar class="markdown-scrollbar my-2 px-4 py-2">
            <div class="markdown-body" v-html="renderedContent" />
          </el-scrollbar>
        </el-tab-pane>
        <el-tab-pane :label="$t('chipInfo.documents')" name="docs">
          <el-scrollbar class="docs-scrollbar">
            <el-card>
              <el-collapse class="docs-collapse mx-4">
                <template v-for="[type, docItems] of Object.entries(docs)" :key="type">
                  <el-collapse-item
                    v-if="Object.keys(docItems).length > 0"
                    :title="type"
                  >
                    <div class="docs-list">
                      <template v-for="[name, doc] of Object.entries(docItems)" :key="name">
                        <div
                          class="doc-item"
                          @click="openUrl(doc.url.value)"
                        >
                          <div class="doc-icon">
                            <i class="ri-file-pdf-2-line" />
                          </div>
                          <div class="doc-name">
                            {{ name }}
                            <el-tag type="primary">
                              {{ (doc.version.startsWith('v') || doc.version.startsWith('V')) ? doc.version : `v${doc.version}` }}
                            </el-tag>
                          </div>
                          <div class="doc-type">
                            {{ doc.type || 'PDF' }}
                          </div>
                          <div class="doc-size">
                            {{ doc.size }}
                          </div>
                        </div>
                      </template>
                    </div>
                  </el-collapse-item>
                </template>
              </el-collapse>
            </el-card>
          </el-scrollbar>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-empty v-else :description="$t('chipInfo.selectChipToViewDetails')" />
  </div>
</template>

<style scoped>
.chip-info-container {
  display: flex;
  flex: 1;
  flex-direction: column;
  padding: 16px;
  min-width: 0;
  min-height: 0;
  user-select: text;
}

.chip-info-content {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
  min-height: 0;
}

.chip-title {
  margin: 0 0 16px 0;
  font-size: 1.5rem;
  color: var(--ep-color-primary);
}

.chip-tabs {
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.ep-tab-pane {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-tabs__content) {
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

.url-div {
  cursor: pointer;
}

.url-div:hover {
  text-decoration: underline;
}

.markdown-scrollbar {
  flex: 1;
  border: 1px solid var(--ep-border-color);
  border-radius: 6px;
}

.markdown-body {
  flex: 1;
  text-align: left;
  user-select: text;
  padding: 20px;
}

.docs-scrollbar {
  flex: 1;
  border: 1px solid var(--ep-border-color);
  border-radius: 6px;
}

.docs-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
}

.doc-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 0px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.doc-item:hover {
  background-color: var(--ep-fill-color-light);
}

.doc-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ep-color-primary);
  font-size: 16px;
  flex-shrink: 0;
}

.doc-name {
  flex: 1;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.doc-type {
  color: var(--ep-text-color-regular);
  font-size: 13px;
  white-space: nowrap;
  opacity: 0.9;
}

.doc-size {
  color: var(--ep-text-color-secondary);
  font-size: 12px;
  white-space: nowrap;
  opacity: 0.7;
}
</style>
