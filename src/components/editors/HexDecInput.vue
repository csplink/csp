<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        HexDecInput.vue
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
 *  2025-08-04     xqyjlj       initial version
-->

<script setup lang="ts">
import { computed, shallowRef, watch } from 'vue'

interface PropsType {
  modelValue: number
  disabled?: boolean
  placeholder?: string
}

const props = withDefaults(defineProps<PropsType>(), {
  disabled: false,
  placeholder: '',
})

const emit = defineEmits(['change', 'update:modelValue'])

const baseMode = shallowRef<10 | 16>(16)
const inputValue = shallowRef('')
const previousValue = shallowRef('')

const baseOptions = [
  { label: 'Dec', value: 10 },
  { label: 'Hex', value: 16 },
]

/**
 * Parse a string value into a number, taking into account whether it's a hex or
 * decimal representation.
 *
 * @param {string} val - The string value to parse
 * @returns {number|null} The parsed number, or null if the string is invalid
 */
function parseValue(val: string): number | null {
  const isHex = val.toLowerCase().startsWith('0x')
  const parsed = Number.parseInt(isHex ? val.slice(2) : val, isHex ? 16 : 10)
  return Number.isNaN(parsed) ? null : parsed
}

/**
 * Format a number into a string representation that is either a decimal or
 * hexadecimal value, depending on the specified base.
 *
 * @param {number} num - The number to format
 * @param {10|16} base - The base to format the number to. 10 for decimal, 16 for
 *   hexadecimal.
 * @returns {string} The formatted string
 */
function formatValue(num: number, base: 10 | 16): string {
  return base === 16 ? `0x${num.toString(16).toUpperCase()}` : num.toString(10)
}

const hexDisplay = computed(() => {
  const num = parseValue(inputValue.value)
  return num !== null ? `(0x${num.toString(16).toUpperCase()})` : ''
})

function syncInputFromModelValue(newVal: number) {
  inputValue.value = formatValue(newVal, baseMode.value)
  previousValue.value = inputValue.value
}

watch(() => props.modelValue, syncInputFromModelValue, { immediate: true })

function handleInput() {
  let val = inputValue.value

  if (baseMode.value === 16 && val && !val.toLowerCase().startsWith('0x')) {
    val = `0x${val}`
    inputValue.value = val
  }

  if (baseMode.value === 16) {
    if (val === '0x') {
      val = '0x0'
      inputValue.value = val
    }
  }
  else {
    if (val === '') {
      val = '0'
      inputValue.value = val
    }
  }

  const isValid = baseMode.value === 16
    ? /^0x[0-9a-fA-F]+$/.test(val)
    : /^\d+$/.test(val)

  if (!isValid) {
    inputValue.value = previousValue.value
    return
  }

  if (baseMode.value === 16) {
    const num = Number.parseInt(val, 16)
    val = `0x${num.toString(16).toUpperCase()}`
    inputValue.value = val
  }

  let num: number
  if (baseMode.value === 16) {
    num = Number.parseInt(val, 16)
    val = `0x${num.toString(16).toUpperCase()}`
  }
  else {
    num = Number.parseInt(val, 10)
    val = num.toString(10)
  }

  inputValue.value = val
  previousValue.value = val
}

function commit() {
  const val = parseValue(inputValue.value)
  emit('change', val)
  emit('update:modelValue', val)
}

function handleBaseModeChange(newBase: 10 | 16) {
  baseMode.value = newBase
  inputValue.value = formatValue(props.modelValue, newBase)
}
</script>

<template>
  <div class="hex-dec-input-container">
    <el-input
      v-model="inputValue"
      :disabled="disabled"
      :placeholder="placeholder"
      @input="handleInput"
      @blur="commit"
      @keyup.enter="commit"
    >
      <template #suffix>
        <div class="hex-display">
          {{ hexDisplay }}
        </div>
      </template>
      <template #append>
        <el-select
          v-model="baseMode"
          class="base-select"
          :disabled="disabled"
          @change="handleBaseModeChange"
        >
          <el-option
            v-for="option in baseOptions"
            :key="option.value"
            :label="option.label"
            :value="option.value"
          />
        </el-select>
      </template>
    </el-input>
  </div>
</template>

<style scoped>
.hex-dec-input-container {
  display: flex;
  flex: 1;
}

.hex-display {
  min-width: 80px;
  padding: 0 8px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}

.base-select {
  width: 100px;
}
</style>
