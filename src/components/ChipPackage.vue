<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ChipPackage.vue
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
 *  2025-05-05     xqyjlj       initial version
-->

<script lang="ts" setup>
import type Konva from 'konva'
import type { ComputedRef, ShallowRef } from 'vue'
import type { PanZoomMenuItemModelType } from './containers/PanZoom'
import type { PanZoomInstance } from '~/components/instance'
import type { IPackageBase, PackageModelPinType, PackageModelType } from '~/composables/packages/base'
import { ElMessageBox } from 'element-plus'
import { computed, onBeforeUnmount, onMounted, shallowReactive, shallowRef, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import * as chipPackages from '~/composables/packages'
import { useSummaryManager } from '~/database'
import { getTextColorPrimary, usePinsManager, useProjectManager, useThemeStore } from '~/utils'

interface PinModelType {
  base: PackageModelPinType
  highlight: ShallowRef<boolean>
  color: ComputedRef<string>
  textColor: ComputedRef<string>
  comment: ComputedRef<string>
}

/*! < see more https://zhongguose.com/ */
const DEFAULT_COLOR = '#b2bbbe' /*! < 星灰 */
const POWER_COLOR = '#e9ddb6' /*! < 菊蕾白 */
const RESET_COLOR = '#add5a2' /*! < 嘉陵水绿 */
const NC_COLOR = '#f8ebe6' /*! < 草珠红 */
const BOOT_COLOR = '#b0d5df' /*! < 湖水蓝 */
const SELECTED_COLOR = '#41ae3c' /*! < 宝石绿 */
const UNSUPPORTED_COLOR = '#fbb612' /*! < 鸡蛋黄 */
const HIGHLIGHT_BG_COLOR = '#2d0c13' /*! < 茄皮紫 */
const HIGHLIGHT_FG_COLOR = '#cdd1d3' /*! < 银鱼白 */
const FG_COLOR = '#1f2623' /*! < 苷蓝绿 */

const projectManager = useProjectManager()
const summaryManager = useSummaryManager()
const pinsManager = usePinsManager()
const { t } = useI18n()

const project = projectManager.get()!
const summary = summaryManager.get(project.vendor, project.targetChip)!
const pins = pinsManager.pins

const pinModels = shallowReactive<Record<string, PinModelType>>({})
const packageModelRef = shallowRef<PackageModelType>()
const panZoomRef = shallowRef<PanZoomInstance>()
const textColorPrimaryRef = shallowRef('#ff0000')
const modelWidth = computed(() => packageModelRef.value?.width || 0)
const modelHeight = computed(() => packageModelRef.value?.height || 0)
let intervalTimerId: number | null = null
let highlightedNames: string[] = []

const themeStore = useThemeStore()

watch(() => themeStore.theme, (_newTheme) => {
  textColorPrimaryRef.value = getTextColorPrimary()
})

function getPinColor(model: PinModelType): string {
  let color: string = 'white'
  switch (model.base.pin.type) {
    case 'I/O':
    {
      if (model.base.pin.locked.value) {
        color = SELECTED_COLOR
      }
      else if (model.base.pin.function.value) {
        color = UNSUPPORTED_COLOR
      }
      else {
        color = DEFAULT_COLOR
      }

      break
    }
    case 'monoIO':
    case 'power':
    {
      color = POWER_COLOR
      break
    }
    case 'reset':
    {
      color = RESET_COLOR
      break
    }
    case 'nc':
    {
      color = NC_COLOR
      break
    }
    case 'boot':
    {
      color = BOOT_COLOR
      break
    }
  }

  return color
}

function getPinComment(model: PinModelType): string {
  if (model.base.pin.type !== 'I/O') {
    return ''
  }

  const label = model.base.pin.label.value
  const fn = model.base.pin.function.value

  if (!label && !fn)
    return ''
  if (!label)
    return fn ?? ''
  if (!fn)
    return label

  return `${label}(${fn})`
}

async function loadPackageModel() {
  if (!summary) {
    return
  }

  const chipPackagesTyped = chipPackages as Record<string, typeof IPackageBase>
  const chipPackageKeys = Object.keys(chipPackagesTyped)
  let packType = summary.package
  if (summary.package.startsWith('LQFP')) {
    packType = 'LQFP'
  }

  if (chipPackageKeys.includes(packType)) {
    const ChipPackageClass = chipPackagesTyped[packType]
    const instance = new ChipPackageClass(summary.name, summary.vendor, pinsManager.pins)
    const packageModel = await instance.getPackageModel()
    if (packageModel) {
      for (const pin of packageModel.pins) {
        const model: PinModelType = {
          base: pin,
          highlight: shallowRef(false),
          color: computed((): string => {
            if (model.highlight.value) {
              return HIGHLIGHT_BG_COLOR
            }
            return getPinColor(model)
          }),
          textColor: computed((): string => {
            if (model.highlight.value) {
              return HIGHLIGHT_FG_COLOR
            }
            return FG_COLOR
          }),
          comment: computed((): string => getPinComment(model)),
        }

        pinModels[pin.name] = model
      }
      packageModelRef.value = packageModel
    }
  }
}

function rescale() {
  panZoomRef.value?.rescale()
}

function zoomIn() {
  panZoomRef.value?.zoomIn()
}

function zoomOut() {
  panZoomRef.value?.zoomOut()
}

function highlightByNames(names: string[]) {
  cleanUpTimer()

  highlightedNames = names
  if (names.length > 0) {
    intervalTimerId = setInterval(onTimerTimeout, 500) as unknown as number
  }
}

function highlightBySignals(signals: string[]) {
  cleanUpTimer()

  const names: string[] = []
  for (const signal of signals) {
    for (const [_name, pin] of Object.entries(pinModels)) {
      if (pin.base.pin.functions.includes(signal)) {
        names.push(_name)
      }
    }
  }

  highlightedNames = names
  if (signals.length > 0) {
    intervalTimerId = setInterval(onTimerTimeout, 500) as unknown as number
  }
}

function downloadSvg() {
  panZoomRef.value?.downloadSvg(`${summary.name}-chip-package.png`)
}

function handMouseenter(event: Konva.KonvaEventObject<MouseEvent>, pin: PinModelType) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const container = panZoomRef.value.container
    container.style.cursor = 'pointer'

    const shape = event.target
    const stage = shape.getStage()
    const containerRect = container.getBoundingClientRect()
    const width = (shape.attrs.width * stage?.attrs.scaleX)
    const height = (shape.attrs.height * stage?.attrs.scaleY)
    const placement = pin.base.direction
    let x = 0
    let y = 0

    if (pin.base.direction === 'left') {
      x = shape.getAbsolutePosition().x + containerRect.left
      y = shape.getAbsolutePosition().y + containerRect.top + height / 2
    }
    else if (pin.base.direction === 'bottom') {
      x = shape.getAbsolutePosition().x + containerRect.left + height / 2
      y = shape.getAbsolutePosition().y + containerRect.top
    }
    else if (pin.base.direction === 'right') {
      x = shape.getAbsolutePosition().x + containerRect.left + width
      y = shape.getAbsolutePosition().y + containerRect.top + height / 2
    }
    else {
      x = shape.getAbsolutePosition().x + containerRect.left + height / 2
      y = shape.getAbsolutePosition().y + containerRect.top - width
    }
    panZoomRef.value.showTooltip(x, y, placement, `${pin.base.position + 1}: ${pin.base.name}`)
  }
}

function handMouseleave(event: Konva.KonvaEventObject<MouseEvent>, _pin: any) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const container = panZoomRef.value.container
    container.style.cursor = 'default'

    panZoomRef.value.hideTooltip()
  }
}

function handClick(event: Konva.KonvaEventObject<MouseEvent>) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const container = panZoomRef.value.container
    const shape = event.target
    const model: PinModelType = shape.attrs.pin
    if (model && model.base.pin.functions.length > 0) {
      /*! < mouse left click */
      if (event.evt.button === 0) {
        /*! < alt + mouse left click */
        if (event.evt.altKey) {
          ElMessageBox.prompt(t('chipPackage.labelMessageBoxMessage'), t('chipPackage.labelMessageBoxTitle'), {
            confirmButtonText: t('command.ok'),
            cancelButtonText: t('command.cancel'),
            closeOnClickModal: false,
            inputPattern: /^[A-Z_]\w+$/i,
            inputValue: model.base.pin.label.value,
            inputPlaceholder: t('chipPackage.labelMessageBoxInputPlaceholder'),
            inputErrorMessage: t('chipPackage.labelMessageBoxInputErrorMessage'),
          })
            .then(({ value }) => {
              model.base.pin.label.value = value
            })
            .catch(() => {
            })
        }
        else {
          const stage = shape.getStage()
          const containerRect = container.getBoundingClientRect()
          const width = (shape.attrs.width * stage?.attrs.scaleX)
          const height = (shape.attrs.height * stage?.attrs.scaleY)
          let x = 0
          let y = 0

          const direction = model.base.direction
          if (direction === 'left') {
            x = shape.getAbsolutePosition().x + containerRect.left + width
            y = shape.getAbsolutePosition().y + containerRect.top + height
          }
          else if (direction === 'bottom') {
            x = shape.getAbsolutePosition().x + containerRect.left + height / 2
            y = shape.getAbsolutePosition().y + containerRect.top - width
          }
          else if (direction === 'right') {
            x = shape.getAbsolutePosition().x + containerRect.left
            y = shape.getAbsolutePosition().y + containerRect.top + height
          }
          else {
            x = shape.getAbsolutePosition().x + containerRect.left + height / 2
            y = shape.getAbsolutePosition().y + containerRect.top
          }

          const menuModel: PanZoomMenuItemModelType[] = [
            { key: 'Reset State', command: t('chipPackage.resetState'), divided: false, icon: 'ri-refresh-line' },
          ]

          let divided = true
          for (const func of model.base.pin.functions) {
            menuModel.push({ key: func, command: func, divided, highlight: model.base.pin.function.value === func })
            divided = false
          }

          panZoomRef.value.openMenu(model.base.name, { x, y }, menuModel)
        }
      }
      else {
        panZoomRef.value.closeMenu()
      }
    }
    else {
      panZoomRef.value.closeMenu()
    }
  }
  cleanUpTimer()
}

function handMenuSelect(pinName: string, command: string) {
  const pin = pins[pinName]
  if (command === t('chipPackage.resetState')) {
    pin.reset()
  }
  else {
    if (command === pin.function.value) { /*! < unset function */
      pin.unsetFunction()
    }
    else { /*! < set function */
      pin.setFunction(command)
    }
  }
}

function onTimerTimeout() {
  for (const [name, model] of Object.entries(pinModels)) {
    if (highlightedNames.includes(name)) {
      model.highlight.value = !model.highlight.value
    }
  }
}

function cleanUpTimer() {
  if (intervalTimerId !== null) {
    clearInterval(intervalTimerId)
    intervalTimerId = null
    for (const [_name, model] of Object.entries(pinModels)) {
      model.highlight.value = false
    }
  }
}

onMounted(() => {
  textColorPrimaryRef.value = getTextColorPrimary()
  loadPackageModel()
})

onBeforeUnmount(() => {
  cleanUpTimer()
})

defineExpose({
  rescale,
  zoomIn,
  zoomOut,
  highlightByNames,
  highlightBySignals,
  downloadSvg,
})
</script>

<template>
  <div class="pan-zoom-div flex">
    <PanZoom
      ref="panZoomRef"
      :model-width="modelWidth"
      :model-height="modelHeight"
      @click="handClick"
      @menu-select="handMenuSelect"
    >
      <v-layer>
        <!-- pin label -->
        <v-text
          v-for="[name, pin] in Object.entries(pinModels)"
          :key="`${name}-l`"
          :config="{
            x: pin.base.rotation ? pin.base.label.x : pin.base.label.x + 5,
            y: pin.base.rotation ? pin.base.label.y - 5 : pin.base.label.y,
            width: pin.base.label.width - 10,
            height: pin.base.label.height,
            ellipsis: true,
            text: pin.comment.value,
            fontSize: 12,
            fontStyle: 'bold',
            fill: textColorPrimaryRef,
            wrap: 'none',
            align: pin.base.label.align,
            verticalAlign: 'middle',
            rotation: pin.base.rotation,
          }"
        />
        <!-- chip body -->
        <v-group>
          <!-- chip body background -->
          <v-rect
            v-if="packageModelRef"
            :config="{
              x: packageModelRef.body.x + packageModelRef.body.width / 2,
              y: packageModelRef.body.y + packageModelRef.body.height / 2,
              width: packageModelRef.body.width,
              height: packageModelRef.body.height,
              stroke: 'black',
              fill: '#323232',
              offsetX: packageModelRef.body.width / 2,
              offsetY: packageModelRef.body.height / 2,
              rotation: packageModelRef.body.rotation,
              strokeWidth: 1,
            }"
          />
          <!-- chip body stroke -->
          <v-rect
            v-if="packageModelRef"
            :config="{
              x: packageModelRef.body.x + 6,
              y: packageModelRef.body.y + 6,
              width: packageModelRef.body.width - 12,
              height: packageModelRef.body.height - 12,
              stroke: 'white',
              strokeWidth: 1,
            }"
          />
          <!-- pin1 circle -->
          <v-circle
            v-if="packageModelRef"
            :config="{
              x: packageModelRef.body.x + 25,
              y: packageModelRef.body.y + 25,
              radius: 10,
              fill: '#DCE6F0',
              strokeWidth: 0,
            }"
          />
          <!-- pin text -->
          <v-text
            v-if="packageModelRef"
            :config="{
              x: packageModelRef.body.x,
              y: packageModelRef.body.y,
              width: packageModelRef.body.width,
              height: packageModelRef.body.height,
              ellipsis: true,
              text: packageModelRef.body.name,
              fontSize: packageModelRef.body.height / 15,
              fontStyle: 'bold',
              align: 'center',
              fill: 'white',
              verticalAlign: 'middle',
            }"
          />
          <v-text
            v-if="packageModelRef"
            :config="{
              x: packageModelRef.body.x,
              y: packageModelRef.body.y,
              width: packageModelRef.body.width,
              height: packageModelRef.body.height * 0.9,
              ellipsis: true,
              text: `${packageModelRef.body.vendor}\n\n${packageModelRef.body.package}`,
              fontSize: packageModelRef.body.height / 20,
              fontStyle: 'italic',
              align: 'center',
              fill: 'white',
              verticalAlign: 'bottom',
            }"
          />
        </v-group>
        <!-- chip pin body -->
        <v-group
          v-for="[name, pin] in Object.entries(pinModels)"
          :key="name"
          @mouseenter="handMouseenter($event, pin)"
          @mouseleave="handMouseleave($event, pin)"
        >
          <!-- pin body -->
          <v-rect
            :config="{
              x: pin.base.x,
              y: pin.base.y,
              width: pin.base.width,
              height: pin.base.height,
              fill: pin.color.value,
              stroke: 'black',
              rotation: pin.base.rotation,
              strokeWidth: 1,
              pin,
            }"
          />
          <!-- pin text -->
          <v-text
            :config="{
              x: pin.base.x,
              y: pin.base.y,
              width: pin.base.width,
              height: pin.base.height,
              fill: pin.textColor.value,
              ellipsis: true,
              text: ` ${name}`,
              fontSize: 12,
              fontStyle: 'bold',
              wrap: 'none',
              align: 'left',
              verticalAlign: 'middle',
              rotation: pin.base.rotation,
              pin,
            }"
          />
        </v-group>
      </v-layer>
    </PanZoom>
  </div>
</template>

<style scoped>
.zoom-stage-container {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

.pan-zoom-div {
  flex: 1;
  min-width: 0;
  min-height: 0;
}
</style>
