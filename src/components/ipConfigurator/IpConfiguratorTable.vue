<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        IpConfiguratorTable.vue
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
import type { ElTable } from 'element-plus'
import type { ComputedRef } from 'vue'
import type { Ip, IpParameter, IpParameterEnum, IpRefParameter } from '~/database'
import type { Pin } from '~/utils'
import { computed, isRef, onBeforeUnmount, onMounted, shallowRef, watch } from 'vue'
import { useIpManager, useSummaryManager } from '~/database'
import { usePinsManager, useProjectManager } from '~/utils'

export interface ModelType {
  name: string
  key: string
  refParameters: Record<string, IpRefParameter>
  pin?: Pin
}

interface PropsType {
  instance: string
}

const props = defineProps<PropsType>()
const emit = defineEmits(['pinSelect', 'select'])

const projectManager = useProjectManager()
const ipManager = useIpManager()
const summaryManager = useSummaryManager()
const pinsManager = usePinsManager()

const project = projectManager.get()!
const summary = summaryManager.get(project.vendor, project.targetChip)!
const pins = pinsManager.pins

const models = shallowRef<ModelType[]>([])
const tableRef = shallowRef<InstanceType<typeof ElTable>>()
const currentIp = shallowRef<Ip | null>(null)

project.configs.emitter.on('changed', _onProjectConfigsChanged.bind(this))
watch(
  () => props.instance,
  (_newVal, _oldVal) => {
    setIp(props.instance)
  },
)

const titles = computed((): Record<string, string> => {
  if (!currentIp.value) {
    return {}
  }

  const rtn: Record<string, string> = {}
  if (currentIp.value.instance === summary.pinInstance) {
    const refs = currentIp.value.containers.overview.refParameters.value
    for (const name of Object.keys(refs)) {
      rtn[name] = refs[name].parameter.value.display.value
    }
  }

  return rtn
})

function setIp(instance: string) {
  cleanUpCurrentIp()

  if (!instance || !summary) {
    return
  }

  const ip = ipManager.getPeripheral(project.vendor, instance)
  if (!ip) {
    console.error(`IP '${instance}' not found in project.`)
    return
  }

  models.value = createModels(ip)
  currentIp.value = ip
}

function tr(parameter: IpParameter | ComputedRef<IpParameter>): string | number | boolean {
  if (isRef(parameter)) {
    parameter = parameter.value
  }

  if (parameter.type === 'enum') {
    return (parameter as IpParameterEnum).values[parameter.value.value as string].comment.value
  }

  return parameter.value.value
}

function handCurrentChange(newSelection: ModelType | null, _oldSelection: ModelType | null) {
  if (newSelection) {
    if (currentIp.value?.instance === summary.pinInstance) {
      emit('pinSelect', newSelection ? [newSelection.name] : [])
    }
    emit('select', newSelection ? [newSelection.name] : [])
  }
}

function cleanUpCurrentIp() {
  currentIp.value = null
  models.value = []
}

function createModels(ip: Ip): ModelType[] {
  const ms: ModelType[] = []
  if (ip.instance === summary.pinInstance) {
    const names = Object.keys(project.configs.get('pins', {}))
    for (const name of names) {
      ms.push({
        name,
        key: name,
        refParameters: pins[name].refParameters.value,
        pin: pins[name],
      })
    }
  }

  return ms
}

function _onProjectConfigsChanged(payload: { path: string[], newValue: any, oldValue: any }) {
  if (!currentIp.value) {
    return
  }

  if (currentIp.value.instance === summary.pinInstance) {
    if ((payload.path[0] ?? '') !== 'pins') {
      return
    }

    models.value = createModels(currentIp.value)
  }
}

onMounted(() => {
  setIp(props.instance)
})

onBeforeUnmount(() => {
  cleanUpCurrentIp()
})
</script>

<template>
  <el-table
    ref="tableRef"
    class="ip-configurator-table"
    row-key="key"
    :data="models"
    :border="true"
    :highlight-current-row="true"
    :tree-props="{ children: 'children' }"
    @current-change="handCurrentChange"
  >
    <el-table-column
      :label="$t('label.name')"
      :sortable="true"
      :show-overflow-tooltip="true"
      :min-width="50"
      prop="name"
      :width="78"
    />
    <el-table-column
      v-for="[prop, label] in Object.entries(titles)"
      :key="prop"
      :label="label"
      :min-width="50"
      :show-overflow-tooltip="true"
    >
      <template #default="{ row }: { row: ModelType }">
        <template v-if="prop in row.refParameters">
          {{ tr(row.refParameters[prop].parameter) }}
        </template>
      </template>
    </el-table-column>
    <template v-if="props.instance === summary.pinInstance">
      <el-table-column
        :label="$t('pin.function')"
        :sortable="true"
        :show-overflow-tooltip="true"
        :min-width="50"
      >
        <template #default="{ row }: { row: ModelType }">
          {{ row.pin!.function }}
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('pin.locked')"
        :sortable="true"
        :show-overflow-tooltip="true"
        :min-width="50"
      >
        <template #default="{ row }: { row: ModelType }">
          {{ row.pin!.locked ? '✔' : '✘' }}
        </template>
      </el-table-column>
      <el-table-column
        :label="$t('pin.label')"
        :sortable="true"
        :show-overflow-tooltip="true"
        :min-width="50"
      >
        <template #default="{ row }: { row: ModelType }">
          {{ row.pin!.label }}
        </template>
      </el-table-column>
    </template>
  </el-table>
</template>

<style scoped>
.ep-select-dropdown__item {
  text-align: left;
}

.ip-configurator-table {
  flex: 1;
  height: auto;
  --ep-table-row-hover-bg-color: var(--ep-table-current-row-bg-color);
}

::v-deep(.cell) {
  text-wrap: nowrap;
  text-overflow: ellipsis;
}

::v-deep(.ep-input-number) {
  flex: 1;
}

::v-deep(.ep-input__inner) {
  text-align: left;
}

::v-deep(.ep-input-number.is-without-controls .ep-input__wrapper) {
  padding-left: 12px;
}
</style>
