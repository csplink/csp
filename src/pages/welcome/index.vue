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
 *  2025-08-12     xqyjlj       initial version
-->
<script setup lang="ts">
import MarkdownIt from 'markdown-it'
import { shallowRef, watchEffect } from 'vue'
import { useI18n } from 'vue-i18n'
import 'github-markdown-css/github-markdown-light.css'

const renderedContent = shallowRef('')
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
})
const i18n = useI18n()

async function loadMarkdown(lang: string) {
  try {
    const res = await fetch(`./markdown/hello/${lang}.md`)
    if (!res.ok)
      throw new Error('Markdown not found')
    const text = await res.text()
    renderedContent.value = md.render(text)
  }
  catch (err) {
    console.error(err)
    renderedContent.value = '<p>Markdown not found</p>'
  }
}

watchEffect(() => {
  loadMarkdown(i18n.locale.value)
})
</script>

<template>
  <el-scrollbar class="markdown-scrollbar">
    <div class="markdown-body" v-html="renderedContent" />
  </el-scrollbar>
</template>

<style scoped>
.markdown-scrollbar {
  flex: 1;
}

.markdown-body {
  flex: 1;
  text-align: left;
  padding: 20px;
  border-radius: 6px;
  user-select: text;
}
</style>
