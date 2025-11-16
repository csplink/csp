<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        IpConfiguratorForm.vue
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
 *  2025-08-28     xqyjlj       initial version
-->

<script setup lang="ts">
import type { ComputedRef } from 'vue'
import type { Ip, IpRefParameter } from '~/database'
import { computed, onBeforeUnmount, onMounted, shallowRef, watch } from 'vue'
import {
  isBooleanParameter,
  isEnumParameter,
  isNumberParameter,
  isStringParameter,
  useIpManager,
  useSummaryManager,
} from '~/database'
import { usePinsManager, useProjectManager } from '~/utils'

interface PropsType {
  type: 'modes' | 'configurations' | 'channel'
  instance: string
}

const props = defineProps<PropsType>()
defineEmits(['pinSelect', 'select'])

const projectManager = useProjectManager()
const ipManager = useIpManager()
const summaryManager = useSummaryManager()
const pinsManager = usePinsManager()

const project = projectManager.get()!
const summary = summaryManager.get(project.vendor, project.targetChip)
const pins = pinsManager.pins

const stopCommonWatchHandles: (() => void)[] = []

const currentIp = shallowRef<Ip | null>(null)
const channelRefParameters = shallowRef<ComputedRef<Record<string, IpRefParameter>> | null>(null)

let stopBaseWatchHandle: (() => void) | null = null

watch(
  () => props.instance,
  (value: string) => {
    setIp(value)
  },
)

const refParameters = computed((): Record<string, IpRefParameter> => {
  let rtn: Record<string, IpRefParameter> = {}

  if (!currentIp.value) {
    rtn = {}
  }
  else {
    if (props.type === 'modes') {
      rtn = currentIp.value.containers.modes.refParameters.value
    }
    else if (props.type === 'configurations') {
      rtn = currentIp.value.containers.configurations.refParameters.value
    }
    else if (props.type === 'channel') {
      rtn = channelRefParameters.value?.value ?? {}
    }
  }

  return rtn
})

function setIp(instance: string) {
  const parts = instance.split('@')
  let name = ''
  let channel = ''
  if (parts.length === 1) {
    name = parts[0]
  }
  else if (parts.length === 2) {
    name = parts[0]
    channel = parts[1]
  }

  cleanUpCurrentIp()

  if (!name) {
    currentIp.value = null
    return
  }

  const ip = ipManager.getPeripheral(project.vendor, name)
  if (!ip) {
    console.error(`IP '${name}' not found in project.`)
    currentIp.value = null
    return
  }

  currentIp.value = ip

  if (props.type === 'channel') {
    if (ip.instance === summary!.pinInstance) {
      channelRefParameters.value = pins[channel]?.refParameters ?? null
    }
  }
}

function stopConfigurationsWatch() {
  if (stopBaseWatchHandle) {
    stopBaseWatchHandle()
    stopBaseWatchHandle = null
  }
}

function cleanUpCurrentIp() {
  stopConfigurationsWatch()

  for (const handle of stopCommonWatchHandles) {
    handle()
  }
  stopCommonWatchHandles.length = 0
}

onMounted(() => {
  setIp(props.instance)
})

onBeforeUnmount(() => {
  cleanUpCurrentIp()
})
</script>

<template>
  <el-scrollbar class="ip-configurator-form-scrollbar">
    <div class="ip-configurator-form">
      <el-form v-if="Object.keys(refParameters).length > 0" label-position="left" label-width="auto">
        <template v-for="refParameter in Object.values(refParameters)" :key="refParameter.name">
          <el-form-item
            v-if="refParameter.parameter.value.visible"
            :label="refParameter.parameter.value.display.value"
          >
            <el-select
              v-if="isEnumParameter(refParameter.parameter.value)"
              v-model="refParameter.parameter.value.value.value"
              :placeholder="$t('label.pleaseSelect')"
              :disabled="refParameter.readonly.value"
            >
              <el-option
                v-for="[key, value] in Object.entries(refParameter.values.value)"
                :key="key"
                :value="key"
                :label="value.comment.value"
                :disabled="!value.valid.value.isEnabled"
              >
                <el-tooltip
                  :disabled="value.valid.value.isEnabled"
                  :content="value.valid.value.reason"
                  placement="right"
                  popper-class="g-tooltip-with-newline"
                >
                  {{ value.comment.value }}
                </el-tooltip>
              </el-option>
            </el-select>
            <LazyInputNumber
              v-else-if="isNumberParameter(refParameter.parameter.value)"
              v-model="refParameter.parameter.value.value.value"
              :step="1"
              :step-strictly="refParameter.parameter.value.type === 'integer'"
              :controls="false"
              :min="refParameter.parameter.value.min.value"
              :max="refParameter.parameter.value.max.value"
              :disabled="refParameter.parameter.value.readonly"
              :placeholder="`${refParameter.parameter.value.min.value} ~ ${refParameter.parameter.value.max.value}`"
            />
            <el-input
              v-else-if="isStringParameter(refParameter.parameter.value)"
              v-model="refParameter.parameter.value.value.value"
              :disabled="refParameter.parameter.value.readonly"
              :placeholder="refParameter.parameter.value.description.value"
            />
            <el-checkbox
              v-else-if="isBooleanParameter(refParameter.parameter.value)"
              v-model="refParameter.parameter.value.value.value"
              :disabled="refParameter.parameter.value.readonly"
            />
          </el-form-item>
        </template>
      </el-form>
    </div>
  </el-scrollbar>
</template>

<style>
.g-tooltip-with-newline {
  text-align: left;
  white-space: pre-line;
}
</style>

<style scoped>
.ip-configurator-form-scrollbar {
  flex: 1;
  min-width: 0;
  min-height: 0;
}

.ip-configurator-form {
  flex: 1;
  padding: 16px;
}

.form-text {
  line-height: 32px;
}

::v-deep(.ep-input-number) {
  width: 100%;
}

::v-deep(.ep-input__inner) {
  text-align: left;
}
</style>
