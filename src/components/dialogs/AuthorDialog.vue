<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        AuthorDialog.vue
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
 *  2025-11-18     xqyjlj       initial version
-->

<script lang="ts" setup>
import { shallowRef } from 'vue'

const visible = shallowRef(false)

function show() {
  visible.value = true
}

function hide() {
  visible.value = false
}

defineExpose({
  show,
  hide,
})
</script>

<template>
  <el-dialog
    v-model="visible"
    :title="$t('label.author')"
    :close-on-click-modal="false"
    :close-on-press-escape="false"
    :show-close="true"
    center
    append-to-body
  >
    <div class="author-content">
      <ContributorsList />
    </div>
  </el-dialog>
</template>
