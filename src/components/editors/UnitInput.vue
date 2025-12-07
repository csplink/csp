<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        UnitInput.vue
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
 *  2025-09-30     xqyjlj       initial version
-->

<script setup lang="ts">
import { computed, shallowRef, watch, watchEffect } from 'vue'

type UnitType = 'U' | 'K' | 'M'

interface PropsType {
  modelValue: number
  unit?: UnitType
  disabled?: boolean
  placeholder?: string
  readonly?: boolean
  max?: number
  min?: number
}

const props = withDefaults(defineProps<PropsType>(), {
  unit: 'U',
  disabled: false,
  placeholder: '',
  readonly: false,
  max: Number.MAX_SAFE_INTEGER,
  min: Number.MIN_SAFE_INTEGER,
})

const emit = defineEmits(['change', 'update:modelValue'])

const unitOptions = [
  { label: 'U', value: 'U', multiplier: 1 },
  { label: 'K', value: 'K', multiplier: 1000 },
  { label: 'M', value: 'M', multiplier: 1000000 },
]

const unitMode = shallowRef<UnitType>(props.unit)
const realValue = shallowRef(props.modelValue)
const multiplier = computed(() => {
  const option = unitOptions.find(opt => opt.value === unitMode.value)
  return option?.multiplier || 1
})
const displayValue = shallowRef(calculateDisplayValue(props.modelValue))
const valid = computed(() => realValue.value <= props.max && realValue.value >= props.min)

/* !< 监听 modelValue 变化，非编辑状态才更新显示 */
watch(
  () => props.modelValue,
  (v: number) => {
    realValue.value = v
  },
  { immediate: true },
)

watch(
  () => displayValue.value,
  (v: string, old: string) => {
    if (v === '' || v === '-') {
      realValue.value = 0
    }
    else if (v.endsWith('.')) {
      /* !< 保留一位小数 */
    }
    else if (/^-?\d+(?:\.\d+)?$/.test(v)) {
      realValue.value = calculateRealValue(v)
    }
    else {
      displayValue.value = old
    }
  },
)

watch(
  () => unitMode.value,
  () => {
    displayValue.value = calculateDisplayValue(realValue.value)
  },
  { immediate: true },
)

watchEffect(() => {
  displayValue.value = calculateDisplayValue(realValue.value)
})

/**
 * 格式化基础值为显示值
 */
function calculateDisplayValue(real: number): string {
  const display = real / multiplier.value
  return display.toString()
}

/**
 * 计算基础值
 */
function calculateRealValue(display: string): number {
  if (display === '')
    return 0
  const num = Number.parseFloat(display)
  return Number.isNaN(num) ? 0 : num * multiplier.value
}

/**
 *  提交值
 */
function commit() {
  const value = realValue.value
  emit('change', value)
  emit('update:modelValue', value)
}
</script>

<template>
  <el-tooltip :content="`请输入正确的数值(${calculateDisplayValue(min)}~${calculateDisplayValue(max)})`" :disabled="valid">
    <el-input
      v-model="displayValue"
      :disabled="disabled"
      :placeholder="placeholder"
      :readonly="readonly"
      :class="{ 'is-invalid': !valid }"
      @blur="commit"
      @keyup.enter="commit"
    >
      <template #append>
        <el-select
          v-model="unitMode"
          class="unit-select"
          :disabled="disabled"
        >
          <el-option
            v-for="option in unitOptions"
            :key="option.value"
            :label="option.label || 'U'"
            :value="option.value"
          />
        </el-select>
      </template>
    </el-input>
  </el-tooltip>
</template>

<style scoped>
.unit-select {
  width: 65px;
}

.is-invalid :deep(.ep-input__wrapper) {
  box-shadow: 0 0 0 1px var(--ep-color-error) inset;
}
</style>
