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
import type { PanZoomMenuItemModelType } from './containers/PanZoom'
import type { PanZoomInstance } from '~/components/instance'
import type { IPackageBase, PackageModelPinType, PackageModelType } from '~/composables/packages/base'
import type { Project, ProjectConfigsPinUnitType, Summary } from '~/database'
import { ElMessageBox } from 'element-plus'
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import * as chipPackages from '~/composables/packages'
import { useIpManager, useProjectManager, useSummaryManager } from '~/database'

interface PinModelType {
  base: PackageModelPinType
  color: string
  originColor: string
  textColor: string
  comment: string
  label?: string
  function?: string
  locked?: boolean
  mode?: string
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

const ipManager = useIpManager()
const projectManager = useProjectManager()
const summaryManager = useSummaryManager()
const { t } = useI18n()

const projectRef = ref<Project>()
const summaryRef = ref<Summary>()
const pinsModelRef = ref<Record<string, PinModelType>>({})
const packageModelRef = ref<PackageModelType>()
const panZoomRef = ref<PanZoomInstance>()
const modelWidth = computed(() => packageModelRef.value?.width || 0)
const modelHeight = computed(() => packageModelRef.value?.height || 0)
let intervalTimerId: number | null = null
let highlightedNames: string[] = []

function updatePinColor(pin: PinModelType) {
  switch (pin.base.type) {
    case 'I/O':
    {
      if (pin.locked) {
        pin.originColor = SELECTED_COLOR
      }
      else if (pin.function) {
        pin.originColor = UNSUPPORTED_COLOR
      }
      else {
        pin.originColor = DEFAULT_COLOR
      }

      break
    }
    case 'monoIO':
    case 'power':
    {
      pin.originColor = POWER_COLOR
      break
    }
    case 'reset':
    {
      pin.originColor = RESET_COLOR
      break
    }
    case 'nc':
    {
      pin.originColor = NC_COLOR
      break
    }
    case 'boot':
    {
      pin.originColor = BOOT_COLOR
      break
    }
  }

  pin.color = pin.originColor
}

function updatePinComment(pin: PinModelType) {
  if (pin.base.type === 'I/O') {
    if (!pin.label && !pin.function) {
      pin.comment = ''
      return
    }

    if (!pin.label) {
      pin.comment = pin.function ?? ''
    }
    else {
      if (!pin.function) {
        pin.comment = pin.label
      }
      else {
        pin.comment = `${pin.label}(${pin.function})`
      }
    }
  }
}

function updataPinUI(pin: PinModelType) {
  updatePinColor(pin)
  updatePinComment(pin)
}

function updatePin(pin: PinModelType) {
  const pinInstance = summaryRef.value!.pinInstance()

  if (pin.function) { /*! < set function */
    const instance = pin.function.split(':')[0]
    const ip = ipManager.getPeripheral(projectRef.value!.vendor, instance)

    if (!ip) {
      console.error(`The define '${instance}' not found.`)
      return
    }

    let func = pin.function
    if (pinInstance !== instance) {
      if (!pin.mode) {
        return
      }
      func = pin.mode
    }

    const seqs = func.split(':')
    if (seqs.length !== 2) {
      console.error(`Invalid function '${func}'.`)
      return
    }

    const mode = seqs[1]
    let presets = null
    if (mode in ip.presets) {
      presets = ip.presets[mode]
    }
    else {
      console.error(`Invalid mode '${mode}'.`)
      return
    }

    const model: Record<string, any> = {}
    for (const [key, refParameter] of Object.entries(presets.refParameters)) {
      model[key] = refParameter.default
    }
    projectRef.value!.configs.set(`${pinInstance}.${pin.base.name}`, model)
  }
  else { /*! < clear function */
    projectRef.value!.configs.set(`${pinInstance}.${pin.base.name}`, {})
  }
}

async function loadPackageModel() {
  if (!projectRef.value || !summaryRef.value) {
    return
  }

  const summary = summaryRef.value
  const project = projectRef.value
  const chipPackagesTyped = chipPackages as Record<string, typeof IPackageBase>
  const chipPackageKeys = Object.keys(chipPackagesTyped)
  let packType = ''
  if (summary.package.startsWith('LQFP')) {
    packType = 'LQFP'
  }

  if (chipPackageKeys.includes(packType)) {
    const ChipPackageClass = chipPackagesTyped[packType]
    const instance = new ChipPackageClass(summary)
    const model = await instance.getPackageModel()
    if (model) {
      for (const pin of model.pins) {
        const pinConfig = project.configs.get<ProjectConfigsPinUnitType | null>(`pins.${pin.name}`)
        const model: PinModelType = {
          color: 'white',
          originColor: 'white',
          textColor: FG_COLOR,
          base: pin,
          comment: '',
          label: pinConfig?.label,
          function: pinConfig?.function,
          mode: pinConfig?.mode,
          locked: pinConfig?.locked,
        }
        pinsModelRef.value[pin.name] = model
        updataPinUI(model)
      }
      packageModelRef.value = model
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
    for (const [_name, pin] of Object.entries(pinsModelRef.value)) {
      if (pin.base.functions.includes(signal)) {
        names.push(_name)
      }
    }
  }

  highlightedNames = names
  if (signals.length > 0) {
    intervalTimerId = setInterval(onTimerTimeout, 500) as unknown as number
  }
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
    const pin: PinModelType = shape.attrs.pin
    if (pin && pin.base.functions.length > 0) {
      /*! < mouse left click */
      if (event.evt.button === 0) {
        /*! < alt + mouse left click */
        if (event.evt.altKey) {
          ElMessageBox.prompt(t('chipPackage.labelMessageBoxMessage'), t('chipPackage.labelMessageBoxTitle'), {
            confirmButtonText: t('base.ok'),
            cancelButtonText: t('base.cancel'),
            inputPattern: /^[A-Z_]\w+$/i,
            inputValue: pin.label,
            inputPlaceholder: t('chipPackage.labelMessageBoxInputPlaceholder'),
            inputErrorMessage: t('chipPackage.labelMessageBoxInputErrorMessage'),
          })
            .then(({ value }) => {
              projectRef.value?.configs.set(`pins.${pin.base.name}.label`, value)
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

          if (pin.base.direction === 'left') {
            x = shape.getAbsolutePosition().x + containerRect.left + width
            y = shape.getAbsolutePosition().y + containerRect.top + height
          }
          else if (pin.base.direction === 'bottom') {
            x = shape.getAbsolutePosition().x + containerRect.left + height / 2
            y = shape.getAbsolutePosition().y + containerRect.top - width
          }
          else if (pin.base.direction === 'right') {
            x = shape.getAbsolutePosition().x + containerRect.left
            y = shape.getAbsolutePosition().y + containerRect.top + height
          }
          else {
            x = shape.getAbsolutePosition().x + containerRect.left + height / 2
            y = shape.getAbsolutePosition().y + containerRect.top
          }

          const model: PanZoomMenuItemModelType[] = [
            { key: 'Reset State', command: t('chipPackage.resetState'), divided: false },
          ]

          let divided = true
          for (const func of pin.base.functions) {
            model.push({ key: func, command: func, divided, highlight: pin.function === func })
            divided = false
          }

          panZoomRef.value.openMenu(pin.base.name, { x, y }, model)
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
  if (command === t('chipPackage.resetState')) {
    projectRef.value!.configs.set<ProjectConfigsPinUnitType>(`pins.${pinName}`, {
      locked: false,
      function: '',
      mode: '',
      label: '',
    })
  }
  else {
    const pinConfig = projectRef.value!.configs.get<ProjectConfigsPinUnitType | null>(`pins.${pinName}`)
    if (command === pinConfig?.function) { /*! < unset function */
      projectRef.value!.configs.set<ProjectConfigsPinUnitType>(`pins.${pinName}`, {
        locked: false,
        function: '',
        mode: '',
        label: pinConfig?.label,
      })
    }
    else { /*! < set function */
      const seqs = command.split(':')
      const instance = seqs[0]
      let locked = false
      if (instance === summaryRef.value?.pinInstance() && summaryRef.value?.pins[pinName].modes.includes(command)) {
        locked = true
      }
      projectRef.value!.configs.set<ProjectConfigsPinUnitType>(`pins.${pinName}`, {
        locked,
        function: command,
        mode: '',
        label: pinConfig?.label,
      })
    }
  }
}

function onPinConfigChanged(payload: { path: string[], oldValue: any, newValue: any }) {
  if (payload.path.length === 2) {
    const name = payload.path.at(-1)!
    const value = payload.newValue as ProjectConfigsPinUnitType

    const model = pinsModelRef.value[name]
    model.label = value?.label
    model.function = value?.function
    model.mode = value?.mode
    model.locked = value?.locked

    updataPinUI(model)
    updatePin(model)
  }
  else if (payload.path.length === 3) {
    const name = payload.path[1]

    switch (payload.path.at(-1)) {
      case 'label':{
        pinsModelRef.value[name].label = payload.newValue as string
        break
      }
      case 'function':{
        pinsModelRef.value[name].function = payload.newValue as string
        updatePin(pinsModelRef.value[name])
        break
      }
      case 'mode':{
        pinsModelRef.value[name].mode = payload.newValue as string
        updatePin(pinsModelRef.value[name])
        break
      }
      case 'locked':{
        pinsModelRef.value[name].locked = payload.newValue as boolean
        break
      }
    }

    updataPinUI(pinsModelRef.value[name])
  }
}

function onTimerTimeout() {
  for (const [name, pin] of Object.entries(pinsModelRef.value)) {
    if (highlightedNames.includes(name)) {
      if (pin.color === HIGHLIGHT_BG_COLOR) {
        pin.color = pin.originColor
        pin.textColor = FG_COLOR
      }
      else {
        pin.color = HIGHLIGHT_BG_COLOR
        pin.textColor = HIGHLIGHT_FG_COLOR
      }
    }
  }
}

function cleanUpTimer() {
  if (intervalTimerId !== null) {
    clearInterval(intervalTimerId)
    intervalTimerId = null
    for (const [_name, pin] of Object.entries(pinsModelRef.value)) {
      if (pin.color === HIGHLIGHT_BG_COLOR) {
        pin.color = pin.originColor
        pin.textColor = FG_COLOR
      }
    }
  }
}

onMounted(async () => {
  const project = projectManager.get()
  if (project) {
    projectRef.value = project
    project.configs.emitter.on('pinConfigChanged', onPinConfigChanged)
    const summary = summaryManager.get(project.vendor, project.targetChip)
    if (summary) {
      summaryRef.value = summary
      loadPackageModel()
    }
  }
})

onBeforeUnmount(() => {
  cleanUpTimer()
  if (projectRef.value) {
    projectRef.value.configs.emitter.off('pinConfigChanged', onPinConfigChanged)
  }
})

defineExpose({
  rescale,
  zoomIn,
  zoomOut,
  highlightByNames,
  highlightBySignals,
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
          v-for="[name, pin] in Object.entries(pinsModelRef)"
          :key="`${name}-l`"
          :config="{
            x: pin.base.rotation ? pin.base.label.x : pin.base.label.x + 5,
            y: pin.base.rotation ? pin.base.label.y - 5 : pin.base.label.y,
            width: pin.base.label.width - 10,
            height: pin.base.label.height,
            ellipsis: true,
            text: pin.comment,
            fontSize: 12,
            fontStyle: 'bold',
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
          v-for="[name, pin] in Object.entries(pinsModelRef)"
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
              fill: pin.color,
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
              fill: pin.textColor,
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
