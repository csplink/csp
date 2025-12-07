<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        LazyInputNumber.vue
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
 *  2025-09-11     xqyjlj       initial version
-->

<script setup lang="ts">
import { computed, shallowRef, watch } from 'vue'

interface Props {
  modelValue: number
  step?: number
  stepStrictly?: boolean
  controls?: boolean
  min?: number
  max?: number
  disabled?: boolean
  placeholder?: string
}

const props = withDefaults(defineProps<Props>(), {
  max: Number.MAX_SAFE_INTEGER,
  min: Number.MIN_SAFE_INTEGER,
})
const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
  (e: 'change', value: number): void
}>()

const tempValue = shallowRef<number>(props.modelValue)
const valid = computed(() => tempValue.value <= props.max && tempValue.value >= props.min)

watch(
  () => props.modelValue,
  (val) => {
    if (val !== tempValue.value) {
      tempValue.value = val
    }
  },
)

function commit() {
  emit('update:modelValue', tempValue.value)
  emit('change', tempValue.value)
}
</script>

<template>
  <el-tooltip :content="`请输入正确的数值(${min}~${max})`" :disabled="valid">
    <el-input-number
      v-model="tempValue"
      :class="{ 'is-invalid': !valid }"
      :step="step ?? 1"
      :step-strictly="stepStrictly"
      :controls="controls ?? false"
      :disabled="disabled"
      :placeholder="placeholder"
      @blur="commit"
      @keyup.enter="commit"
    />
  </el-tooltip>
</template>

<style scoped>
.is-invalid :deep(.ep-input__wrapper) {
  box-shadow: 0 0 0 1px var(--ep-color-error) inset;
}
</style>
