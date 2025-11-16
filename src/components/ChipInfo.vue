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
import { computed, onMounted, ref, shallowRef, watch } from 'vue'
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
const chipSummary = shallowRef<Summary | null>(null)
const loading = ref(false)
const activeTab = ref('basic')
const docs = shallowRef<Record<string, Record<string, SummaryDocumentUnit>>>({})

const renderedContent = computed(() => {
  return md.render(chipSummary.value?.illustrate.value || '')
})

function processDocuments(summary: Summary): Record<string, Record<string, SummaryDocumentUnit>> {
  const processedDocs: Record<string, Record<string, SummaryDocumentUnit>> = {}

  let title = '数据手册'
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.datasheets)) {
    processedDocs[title][name] = unit
  }
  title = '勘误表'
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.references)) {
    processedDocs[title][name] = unit
  }
  title = '参考文档'
  processedDocs[title] = {}
  for (const [name, unit] of Object.entries(summary.documents.errata)) {
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
    console.error('加载芯片信息失败:', error)
    ElMessage.error('加载芯片信息失败')
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
        <el-tab-pane label="基本信息" name="basic">
          <el-descriptions
            :column="5"
            :border="true"
          >
            <el-descriptions-item label="名称">
              <div class="url-div" @click="openUrl(chipSummary.url.value)">
                <el-tooltip :content="chipSummary.url.value">
                  {{ chipSummary.name }}
                </el-tooltip>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="厂商">
              <div class="url-div" @click="openUrl(chipSummary.vendorUrl.value)">
                <el-tooltip :content="chipSummary.vendorUrl.value">
                  {{ chipSummary.vendor }}
                </el-tooltip>
              </div>
            </el-descriptions-item>
            <el-descriptions-item label="IO">
              {{ chipSummary.io }}
            </el-descriptions-item>
            <el-descriptions-item label="售价" />
            <el-descriptions-item :rowspan="2" label="封装图">
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
            <el-descriptions-item label="封装">
              {{ chipSummary.package }}
            </el-descriptions-item>
            <el-descriptions-item label="简介">
              {{ chipSummary.introduction }}
            </el-descriptions-item>
          </el-descriptions>

          <el-scrollbar class="markdown-scrollbar my-2 px-4 py-2">
            <div class="markdown-body" v-html="renderedContent" />
          </el-scrollbar>
        </el-tab-pane>
        <el-tab-pane label="文档" name="docs">
          <el-scrollbar class="docs-scrollbar">
            <el-collapse class="mx-4">
              <template v-for="[type, docItems] of Object.entries(docs)" :key="type">
                <el-collapse-item
                  v-if="Object.keys(docItems).length > 0"
                  :title="type"
                >
                  <div class="docs-list">
                    <div
                      v-for="[name, doc] of Object.entries(docItems)"
                      :key="name"
                      class="doc-card"
                      @click="openUrl(doc.url.value)"
                    >
                      <div class="doc-icon">
                        <el-icon size="24">
                          <i class="ri-file-pdf-2-line" />
                        </el-icon>
                      </div>
                      <div class="doc-info">
                        <div class="doc-title">
                          {{ name }}
                        </div>
                        <div class="doc-meta">
                          {{ doc.type || 'PDF' }} · {{ doc.size }}
                        </div>
                      </div>
                    </div>
                  </div>
                </el-collapse-item>
              </template>
            </el-collapse>
          </el-scrollbar>
        </el-tab-pane>
      </el-tabs>
    </div>

    <el-empty v-else description="请选择芯片以查看详细信息" />
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

/* ::v-deep(.ep-descriptions__content) {
  user-select: text;
} */

.markdown-scrollbar {
  flex: 1;
  border: 1px solid var(--ep-border-color);
  border-radius: 6px;
}

.markdown-body {
  flex: 1;
  text-align: left;
  user-select: text;
}

.docs-scrollbar {
  flex: 1;
  border: 1px solid var(--ep-border-color);
  border-radius: 6px;
}

.docs-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.doc-card {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 6px;
  background-color: var(--ep-fill-color-blank);
  border: 1px solid var(--ep-border-color);
  transition: all 0.2s;
  cursor: pointer;
}

.doc-card:hover {
  background-color: var(--ep-fill-color);
  transform: translateY(-2px);
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.doc-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 4px;
  background-color: var(--ep-color-primary-light-9);
  color: var(--ep-color-primary);
  margin-right: 12px;
}

.doc-info {
  flex: 1;
}

.doc-title {
  font-weight: bold;
  margin-bottom: 4px;
  white-space: nowrap;
  text-overflow: ellipsis;
  text-align: left;
}

.doc-meta {
  font-size: 12px;
  color: var(--ep-text-color-secondary);
  text-align: left;
}
</style>
