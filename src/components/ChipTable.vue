<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ChipTable.vue
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
 *  2025-08-16     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { Repository } from '~/database'
import { ElMessage } from 'element-plus'
import { computed, onMounted, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import * as XLSX from 'xlsx'
import { useRepositoryManager } from '~/database'
import { saveFileWithDialog } from '~/utils'

interface ChipData {
  vendor: string
  series: string
  line: string
  name: string
  unit: {
    package: string
    core: string
    ram: number
    flash: number
    frequency: number
    [key: string]: any
  }
}

const props = defineProps({
  filterResult: {
    type: Array as () => string[],
    default: () => [],
  },
})

const emit = defineEmits(['select', 'update:modelValue'])

const { t } = useI18n()
const loading = shallowRef(false)
const repository = shallowRef<Repository>()
const repositoryManager = useRepositoryManager()
const searchText = shallowRef('')
const allChipsMap = shallowRef<Map<string, ChipData>>(new Map())
const tableData = computed(() => {
  if (props.filterResult.length === 0)
    return []

  return props.filterResult
    .map(chipName => allChipsMap.value.get(chipName))
    .filter(chip => chip !== undefined) as ChipData[]
})

const filteredTableData = computed(() => {
  if (!searchText.value) {
    return tableData.value
  }

  const keyword = searchText.value.toLowerCase()
  return tableData.value.filter((chip) => {
    return chip.name.toLowerCase().includes(keyword)
  })
})

const hasData = computed(() => tableData.value.length > 0)

async function initRepository() {
  loading.value = true
  try {
    repository.value = await repositoryManager.get()
    buildChipsMap()
  }
  catch (error) {
    console.error('Failed to load repository', error)
  }
  finally {
    loading.value = false
  }
}

function buildChipsMap() {
  if (!repository.value)
    return

  const map = new Map<string, ChipData>()
  const chips = repository.value.chips

  for (const [vendorName, vendor] of Object.entries(chips)) {
    for (const [seriesName, series] of Object.entries(vendor.content)) {
      for (const [lineName, line] of Object.entries(series.lines)) {
        for (const [unitName, unit] of Object.entries(line.units)) {
          map.set(unitName, {
            vendor: vendorName,
            series: seriesName,
            line: lineName,
            name: unitName,
            unit,
          })
        }
      }
    }
  }

  allChipsMap.value = map
}

function handCurrentChange(row: ChipData | null, _old: ChipData | null) {
  const name = row?.name ?? ''
  const vendor = row?.vendor ?? ''
  emit('select', vendor, name)
  if (name === '' || vendor === '') {
    emit('update:modelValue', '')
  }
  else {
    emit('update:modelValue', `${vendor}@${name}`)
  }
}

function exportToExcel() {
  try {
    const exportData = filteredTableData.value.map(item => ({
      [t('chipTable.chipModel')]: item.name,
      [t('chipTable.manufacturer')]: item.vendor,
      [t('chipTable.series')]: item.series,
      [t('chipTable.productLine')]: item.line,
      [t('chipTable.package')]: item.unit.package,
      [t('chipTable.core')]: item.unit.core,
      [t('chipTable.ram')]: item.unit.ram,
      [t('chipTable.flash')]: item.unit.flash,
      [t('chipTable.frequency')]: item.unit.frequency,
    }))

    const worksheet = XLSX.utils.json_to_sheet(exportData)
    const workbook = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(workbook, worksheet, t('chipTable.chipList'))

    const columnWidths = [
      { wch: 15 },
      { wch: 10 },
      { wch: 10 },
      { wch: 10 },
      { wch: 10 },
      { wch: 10 },
      { wch: 10 },
      { wch: 10 },
      { wch: 10 },
    ]
    worksheet['!cols'] = columnWidths

    const fileName = `${t('chipTable.chipList')}_${new Date().toISOString().split('T')[0]}.xlsx`

    const arrayBuffer: ArrayBuffer = XLSX.write(workbook, {
      bookType: 'xlsx',
      type: 'array',
    })

    saveFileWithDialog(arrayBuffer, { defaultPath: fileName })

    ElMessage.success(t('chipTable.exportSuccess'))
  }
  catch (error) {
    console.error('Failed to export to Excel', error)
    ElMessage.error(t('chipTable.exportFailed'))
  }
}

watch(() => props.filterResult, (newVal) => {
  if (allChipsMap.value.size === 0 && newVal.length > 0) {
    initRepository()
  }

  searchText.value = ''
}, { immediate: true })

onMounted(() => {
  initRepository()
})
</script>

<template>
  <div class="chip-table-dev flex">
    <el-card v-if="!loading && hasData" shadow="never" class="results-card">
      <template #header>
        <div class="results-header">
          <h3>{{ $t('chipTable.filterResults') }} ({{ tableData.length }})</h3>
          <div class="tools-dev">
            <el-input
              v-model="searchText"
              :placeholder="$t('chipTable.searchChipPlaceholder')"
            >
              <template #prefix>
                <el-icon><i class="ri-search-line" /></el-icon>
              </template>
            </el-input>
            <el-tooltip
              :content="$t('chipTable.exportToExcel')"
              placement="top"
            >
              <el-button circle @click="exportToExcel">
                <el-icon><i class="ri-file-excel-line" /></el-icon>
              </el-button>
            </el-tooltip>
          </div>
        </div>
      </template>

      <el-table
        class="chip-table"
        :data="filteredTableData"
        :border="true"
        :highlight-current-row="true"
        @current-change="handCurrentChange"
      >
        <el-table-column prop="name" :label="$t('chipTable.chipModel')" sortable />
        <el-table-column prop="vendor" :label="$t('chipTable.manufacturer')" sortable />
        <el-table-column prop="series" :label="$t('chipTable.series')" sortable />
        <el-table-column prop="line" :label="$t('chipTable.productLine')" sortable />
        <el-table-column prop="unit.package" :label="$t('chipTable.package')" sortable />
        <el-table-column prop="unit.core" :label="$t('chipTable.core')" sortable />
        <el-table-column prop="unit.ram" :label="$t('chipTable.ram')" sortable />
        <el-table-column prop="unit.flash" :label="$t('chipTable.flash')" sortable />
        <el-table-column prop="unit.frequency" :label="$t('chipTable.frequency')" sortable />
      </el-table>
    </el-card>
    <el-empty v-else-if="!loading && !hasData" :description="$t('chipTable.noMatchingChipFound')" />
    <el-skeleton v-else animated :rows="5" />
  </div>
</template>

<style scoped>
.chip-table-dev {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

.results-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
  min-height: 0;
}

::v-deep(.ep-card__body) {
  display: flex;
  padding: 10px;
  min-width: 0;
  min-height: 0;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
}

.results-header h3 {
  margin: 0;
  white-space: nowrap;
}

.tools-dev {
  display: flex;
  align-items: center;
  gap: 8px;
}

.chip-table {
  flex: 1;
  height: auto;
  --ep-table-row-hover-bg-color: var(--ep-table-current-row-bg-color);
}
</style>
