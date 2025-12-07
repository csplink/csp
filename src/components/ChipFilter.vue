<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ChipFilter.vue
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
 *  2025-08-14     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { AutocompleteFetchSuggestionsCallback } from 'element-plus'
import type { Repository } from '~/database'
import { ElMessage } from 'element-plus'
import { onMounted, reactive, ref, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useRepositoryManager } from '~/database'

interface SearchResultItem {
  value: string
  path: string
}

interface RangeItem {
  min: number
  max: number
}

const emit = defineEmits(['update:modelValue'])

const { t } = useI18n()
const repositoryManager = useRepositoryManager()
const repository = shallowRef<Repository>()
const loading = shallowRef(false)

const searchQuery = shallowRef('')
const searchResults = shallowRef<SearchResultItem[]>([])

const filters = reactive({
  vendors: [] as string[],
  series: [] as string[],
  lines: [] as string[],
  packages: [] as string[],
  cores: [] as string[],
  ram: { min: 0, max: 0 } as RangeItem,
  flash: { min: 0, max: 0 } as RangeItem,
  frequency: { min: 0, max: 0 } as RangeItem,
})

const tempSliderValues = reactive({
  ram: [0, 0] as number[],
  flash: [0, 0] as number[],
  frequency: [0, 0] as number[],
})

const filterOptions = reactive({
  vendors: [] as string[],
  series: [] as string[],
  lines: [] as string[],
  packages: [] as string[],
  cores: [] as string[],
  ram: { min: 0, max: 0 } as RangeItem,
  flash: { min: 0, max: 0 } as RangeItem,
  frequency: { min: 0, max: 0 } as RangeItem,
})

const mainActiveNames = ref(['products', 'memory'])
const productsActiveNames = ref(['vendors', 'series', 'lines', 'packages', 'cores'])

onMounted(async () => {
  loading.value = true
  try {
    repository.value = await repositoryManager.get()
    initFilterOptions()
    updateFilteredUnits()
  }
  catch (error) {
    ElMessage.error(t('chipFilter.loadChipDataFailed'))
    console.error(error)
  }
  finally {
    loading.value = false
  }
})

function initFilterOptions() {
  if (!repository.value)
    return

  const vendorsSet = new Set<string>()
  const seriesSet = new Set<string>()
  const linesSet = new Set<string>()
  const packagesSet = new Set<string>()
  const coresSet = new Set<string>()

  let minRam = Infinity
  let maxRam = 0
  let minFlash = Infinity
  let maxFlash = 0
  let minFreq = Infinity
  let maxFreq = 0

  const chips = repository.value.chips
  for (const [vendorName, vendor] of Object.entries(chips)) {
    vendorsSet.add(vendorName)

    for (const [seriesName, series] of Object.entries(vendor.content)) {
      seriesSet.add(seriesName)

      for (const [lineName, line] of Object.entries(series.lines)) {
        linesSet.add(lineName)

        for (const [_unitName, unit] of Object.entries(line.units)) {
          packagesSet.add(unit.package)
          coresSet.add(unit.core)

          minRam = Math.min(minRam, unit.ram)
          maxRam = Math.max(maxRam, unit.ram)

          minFlash = Math.min(minFlash, unit.flash)
          maxFlash = Math.max(maxFlash, unit.flash)

          minFreq = Math.min(minFreq, unit.frequency)
          maxFreq = Math.max(maxFreq, unit.frequency)
        }
      }
    }
  }

  filterOptions.vendors = Array.from(vendorsSet).sort()
  filterOptions.series = Array.from(seriesSet).sort()
  filterOptions.lines = Array.from(linesSet).sort()
  filterOptions.packages = Array.from(packagesSet).sort()
  filterOptions.cores = Array.from(coresSet).sort()

  filterOptions.ram = { min: minRam, max: maxRam }
  filters.ram = { min: minRam, max: maxRam }
  tempSliderValues.ram = [minRam, maxRam]

  filterOptions.flash = { min: minFlash, max: maxFlash }
  filters.flash = { min: minFlash, max: maxFlash }
  tempSliderValues.flash = [minFlash, maxFlash]

  filterOptions.frequency = { min: minFreq, max: maxFreq }
  filters.frequency = { min: minFreq, max: maxFreq }
  tempSliderValues.frequency = [minFreq, maxFreq]
}

function updateFilteredUnits() {
  if (!repository.value)
    return

  const results: string[] = []

  const chips = repository.value.chips
  for (const [vendorName, vendor] of Object.entries(chips)) {
    if (filters.vendors.length > 0 && !filters.vendors.includes(vendorName))
      continue
    for (const [seriesName, series] of Object.entries(vendor.content)) {
      if (filters.series.length > 0 && !filters.series.includes(seriesName))
        continue
      for (const [lineName, line] of Object.entries(series.lines)) {
        if (filters.lines.length > 0 && !filters.lines.includes(lineName))
          continue
        for (const [unitName, unit] of Object.entries(line.units)) {
          if (filters.packages.length > 0 && !filters.packages.includes(unit.package))
            continue
          if (filters.cores.length > 0 && !filters.cores.includes(unit.core))
            continue
          if (unit.ram < filters.ram.min || unit.ram > filters.ram.max)
            continue
          if (unit.flash < filters.flash.min || unit.flash > filters.flash.max)
            continue
          if (unit.frequency < filters.frequency.min || unit.frequency > filters.frequency.max)
            continue
          results.push(unitName)
        }
      }
    }
  }

  emit('update:modelValue', results)
}

function searchChips(query: string) {
  if (!repository.value || !query) {
    searchResults.value = []
    return
  }

  query = query.toLowerCase()
  const results: SearchResultItem[] = []

  const chips = repository.value.chips
  for (const [vendorName, vendor] of Object.entries(chips)) {
    for (const [seriesName, series] of Object.entries(vendor.content)) {
      for (const [lineName, line] of Object.entries(series.lines)) {
        for (const [unitName, _] of Object.entries(line.units)) {
          if (unitName.toLowerCase().includes(query)) {
            results.push({
              value: unitName,
              path: `${vendorName} > ${seriesName} > ${lineName} > ${unitName}`,
            })
          }
        }
      }
    }
  }

  searchResults.value = results
}

function selectSearchResult(item: Record<string, any>) {
  emit('update:modelValue', [item.value])
}

watch(filters, () => {
  updateFilteredUnits()
}, { deep: true })

function resetFilters() {
  filters.vendors = []
  filters.series = []
  filters.lines = []
  filters.packages = []
  filters.cores = []

  filters.ram = filterOptions.ram
  tempSliderValues.ram = [filterOptions.ram.min, filterOptions.ram.max]

  filters.flash = filterOptions.flash
  tempSliderValues.flash = [filterOptions.flash.min, filterOptions.flash.max]

  filters.frequency = filterOptions.frequency
  tempSliderValues.frequency = [filterOptions.frequency.min, filterOptions.frequency.max]

  searchQuery.value = ''
  searchResults.value = []
}
</script>

<template>
  <el-scrollbar class="filter-scrollbar">
    <el-card>
      <template #header>
        <div class="filter-header">
          <h3>{{ $t('chipFilter.title') }}</h3>
          <el-button type="primary" size="small" @click="resetFilters">
            {{ $t('chipFilter.resetFilters') }}
          </el-button>
        </div>
      </template>
      <template v-if="loading">
        <el-skeleton :loading="loading" animated :rows="10" />
      </template>
      <template v-else>
        <div>
          <div class="search-section">
            <el-autocomplete
              v-model="searchQuery"
              :fetch-suggestions="(query:string, cb:AutocompleteFetchSuggestionsCallback) => {
                searchChips(query);
                cb(searchResults);
              }"
              :placeholder="$t('chipFilter.searchChipPlaceholder')"
              popper-class="search-autocomplete"
              clearable
              class="search-input"
              @select="selectSearchResult"
            >
              <template #default="{ item }">
                <div class="search-result-item my-2">
                  <div class="name">
                    {{ item.value }}
                  </div>
                  <div class="path">
                    {{ item.path }}
                  </div>
                </div>
              </template>
            </el-autocomplete>
          </div>

          <div class="filter-section">
            <el-collapse v-model="mainActiveNames">
              <el-collapse-item name="products" :title="$t('chipFilter.productInfo')">
                <el-collapse v-model="productsActiveNames">
                  <el-collapse-item name="vendors" :title="$t('chipFilter.vendor')">
                    <el-scrollbar class="filter-content-scrollbar">
                      <el-checkbox-group v-model="filters.vendors">
                        <el-checkbox
                          v-for="vendor in filterOptions.vendors"
                          :key="vendor"
                          :label="vendor"
                          :value="vendor"
                        />
                      </el-checkbox-group>
                    </el-scrollbar>
                  </el-collapse-item>
                  <el-collapse-item name="series" :title="$t('chipFilter.series')">
                    <el-scrollbar class="filter-content-scrollbar">
                      <el-checkbox-group v-model="filters.series">
                        <el-checkbox
                          v-for="series in filterOptions.series"
                          :key="series"
                          :label="series"
                          :value="series"
                        />
                      </el-checkbox-group>
                    </el-scrollbar>
                  </el-collapse-item>
                  <el-collapse-item name="lines" :title="$t('chipFilter.line')">
                    <el-scrollbar class="filter-content-scrollbar">
                      <el-checkbox-group v-model="filters.lines">
                        <el-checkbox
                          v-for="line in filterOptions.lines"
                          :key="line"
                          :label="line"
                          :value="line"
                        />
                      </el-checkbox-group>
                    </el-scrollbar>
                  </el-collapse-item>
                  <el-collapse-item name="packages" :title="$t('chipFilter.package')">
                    <el-scrollbar class="filter-content-scrollbar">
                      <el-checkbox-group v-model="filters.packages">
                        <el-checkbox
                          v-for="pkg in filterOptions.packages"
                          :key="pkg"
                          :label="pkg"
                          :value="pkg"
                        />
                      </el-checkbox-group>
                    </el-scrollbar>
                  </el-collapse-item>
                  <el-collapse-item name="cores" :title="$t('chipFilter.core')">
                    <el-scrollbar class="filter-content-scrollbar">
                      <el-checkbox-group v-model="filters.cores">
                        <el-checkbox
                          v-for="core in filterOptions.cores"
                          :key="core"
                          :label="core"
                          :value="core"
                        />
                      </el-checkbox-group>
                    </el-scrollbar>
                    <div class="filter-group">
                      <div class="filter-title">
                        {{ $t('chipFilter.frequency') }}
                      </div>
                      <el-slider
                        v-model="tempSliderValues.frequency"
                        range
                        :min="filterOptions.frequency.min"
                        :max="filterOptions.frequency.max"
                        @change="() => {
                          filters.frequency = { min: tempSliderValues.frequency[0], max: tempSliderValues.frequency[1] }
                        }"
                      />
                    </div>
                  </el-collapse-item>
                </el-collapse>
              </el-collapse-item>
              <el-collapse-item name="memory" :title="$t('chipFilter.memoryInfo')">
                <div class="filter-group">
                  <div class="filter-title">
                    {{ $t('chipFilter.ram') }}
                  </div>
                  <el-slider
                    v-model="tempSliderValues.ram"
                    range
                    :min="filterOptions.ram.min"
                    :max="filterOptions.ram.max"
                    @change="() => {
                      filters.ram = { min: tempSliderValues.ram[0], max: tempSliderValues.ram[1] }
                    }"
                  />
                </div>
                <div class="filter-group">
                  <div class="filter-title">
                    {{ $t('chipFilter.flash') }}
                  </div>
                  <el-slider
                    v-model="tempSliderValues.flash"
                    range
                    :min="filterOptions.flash.min"
                    :max="filterOptions.flash.max"
                    @change="() => {
                      filters.flash = { min: tempSliderValues.flash[0], max: tempSliderValues.flash[1] }
                    }"
                  />
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </div>
      </template>
    </el-card>
  </el-scrollbar>
</template>

<style scoped>
.filter-scrollbar {
  flex: 1;
}

.filter-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-section {
  margin-bottom: 20px;
}

.search-result-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.search-result-item .name {
  font-weight: bold;
  line-height: normal;
}

.search-result-item .path {
  font-size: 12px;
  color: #999;
  line-height: normal;
}

::v-deep(.ep-collapse-item__header) {
  font-weight: bold;
  border-bottom: 1px solid var(--ep-collapse-border-color);
}

::v-deep(.ep-collapse-item__wrap) {
  padding-left: 10px;
  border-bottom: none;
}

::v-deep(.ep-collapse-item__content) {
  padding-bottom: 0px;
}

.filter-group {
  padding: 0 12px;
}

.filter-title {
  font-weight: bold;
  text-align: left;
}

.ep-checkbox-group {
  display: flex;
  flex-direction: column;
}
</style>
