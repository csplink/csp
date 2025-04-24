<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        CodeView.vue
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
 *  2025-07-10     xqyjlj       initial version
-->

<script setup lang="ts">
import Prism from 'prismjs'
import { nextTick, ref, watch } from 'vue'

interface PropsType {
  code: string
  language: string
}

const props = defineProps<PropsType>()

const htmlRef = ref<string>('')
const codeRef = ref<HTMLElement>()

watch(
  () => [props.code],
  async () => {
    const grammar = Prism.languages.c
    htmlRef.value = Prism.highlight(props.code, grammar, props.language)
    await nextTick()
    Prism.highlightElement(codeRef.value!)
  },
  { immediate: true },
)
</script>

<template>
  <div class="main-div">
    <el-scrollbar class="code-view-scrollbar">
      <pre class="code-pre"><code ref="codeRef" :class="`language-${language} line-numbers match-braces rainbow-braces`" v-html="htmlRef" /></pre>
    </el-scrollbar>
  </div>
</template>

<style scoped>
.main-div {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.code-view-scrollbar {
  display: flex;
  flex: 1;
  min-width: 0;
  min-height: 0;
  background: var(--ep-bg-color-page); /* !< 这里还需要适配其他主题，暂时先强制使用 --ep-bg-color-page */
}

.code-pre {
  user-select: text;
  margin: 0;
  overflow: hidden;
  width: fit-content;
  background: var(--ep-bg-color-page); /* !< 这里还需要适配其他主题，暂时先强制使用 --ep-bg-color-page */
}
</style>
