<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        ClockView.vue
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
 *  2025-05-13     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { ElInput } from 'element-plus'
import type Konva from 'konva'
import type { PanZoomMenuItemModelType } from './containers/PanZoom'
import type { PanZoomInstance } from '~/components/instance'
import type { Ip, IpClockTreeElementUnit, IpParameter, IpParameterEnum, IpParameterRadio, Project, Summary } from '~/database'
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'
import { useClockTreeManager, useIpManager, useProjectManager, useSummaryManager } from '~/database'
import { escapeRegExp } from '~/utils/express'

type ModelType = RectModelType | CircleModelType

interface BaseModelType {
  cls: string
  x: number
  y: number
  path: string
  refParameter: string
  output: string[]
  input: string[]
  number: number
  name: string
  parameter: IpParameter
}

interface RectModelType extends BaseModelType {
  width: number
  height: number
  value: number | string
  display: string
  readonly: boolean
  type: string
  menu: PanZoomMenuItemModelType[]
}

interface CircleModelType extends BaseModelType {
  r: number
  value: boolean
  group: string
}

interface InputConfigType {
  x: number
  y: number
  scaleX: number
  scaleY: number
  show: boolean
  width: number
  height: number
  model?: ModelType[]
  value: string | number
}

const ipManager = useIpManager()
const clockTreeManager = useClockTreeManager()
const projectManager = useProjectManager()
const summaryManager = useSummaryManager()
const i18n = useI18n()

const projectRef = ref<Project>()
const summaryRef = ref<Summary>()
const clockTreeIpRef = ref<Ip>()
const panZoomRef = ref<PanZoomInstance>()
const svgImageRef = ref<HTMLImageElement>()
const rectModelsRef = ref<Record<string, RectModelType>>({}) /*! < 注意，此处的key为svg element name */
const circleModelsRef = ref<Record<string, CircleModelType>>({}) /*! < 注意，此处的key为svg element name */
const allModelsRef = ref<Record<string, ModelType>>({}) /*! < 注意，此处的key为refParameter */
const radioGroupModelsRef = ref<Record<string, Record<string, CircleModelType>>>({}) /*! < [group][svg element name] */
const inputConfigRef = ref<InputConfigType>({
  x: 0,
  y: 0,
  show: false,
  scaleX: 1,
  scaleY: 1,
  width: 0,
  height: 0,
  value: '',
})

const inputRef = ref<InstanceType<typeof ElInput>>()

const modelWidth = computed(() => svgImageRef.value?.width || 0)
const modelHeight = computed(() => svgImageRef.value?.height || 0)

let lastRectModel: RectModelType | null = null

function rescale() {
  panZoomRef.value?.rescale()
}

function zoomIn() {
  panZoomRef.value?.zoomIn()
}

function zoomOut() {
  panZoomRef.value?.zoomOut()
}

function setClockTree(vendor: string, name: string) {
  const clockTree = clockTreeManager.get(vendor, name)
  if (!clockTree) {
    console.error('Clock tree content not found')
    return
  }
  if (!clockTreeIpRef.value?.clockTree) {
    console.error('Clock tree not found')
    return
  }

  let svg = clockTree.svg
  for (const [name, lang] of Object.entries(clockTreeIpRef.value.clockTree.i18n)) {
    const value = lang.get(i18n.locale.value)
    if (value !== '') {
      svg = svg.replace(new RegExp(escapeRegExp(name), 'g'), value)
    }
  }

  const project = projectRef.value!
  const rectModels: Record<string, RectModelType> = {}
  const circleModels: Record<string, CircleModelType> = {}
  const radioGroupModels: Record<string, Record<string, CircleModelType>> = {}
  const allModels: Record<string, ModelType> = {}
  for (const [name, geometry] of Object.entries(clockTree.widgets)) {
    const element: IpClockTreeElementUnit = clockTreeIpRef.value.clockTree.elements[name]
    const refParameter = element.refParameter
    const parameter = clockTreeIpRef.value.parameters[refParameter]
    const path = `${summaryRef.value!.clockTree.ip}.${refParameter}`
    let result = project.configs.get(path)

    const baseModel: BaseModelType = {
      x: geometry.x,
      y: geometry.y,
      path,
      refParameter,
      output: element.output,
      input: element.input,
      cls: parameter.type === 'radio' ? 'circle' : 'rect',
      number: 0,
      name,
      parameter,
    }

    if (result == null) {
      result = parameter.default
      project.configs.set(path, result)
    }

    if (parameter.type === 'radio') {
      const parameterTyped = parameter as IpParameterRadio
      if (!radioGroupModels[parameterTyped.group]) {
        radioGroupModels[parameterTyped.group] = {}
      }

      let model
      if (allModels[refParameter]) {
        model = allModels[refParameter] as CircleModelType
      }
      else {
        model = {
          ...baseModel,
          r: geometry.width / 2,
          value: result,
          group: parameterTyped.group,

        }
        allModels[refParameter] = model
      }
      if (result) {
        projectRef.value?.configs.set(`${summaryRef.value!.clockTree.ip}.${parameterTyped.group}`, refParameter)
      }
      radioGroupModels[parameterTyped.group][name] = model
      circleModels[name] = model
    }
    else {
      let model
      if (allModels[refParameter]) {
        model = allModels[refParameter] as RectModelType
      }
      else {
        const menuModel: PanZoomMenuItemModelType[] = []
        let display = ''
        if (parameter.type === 'enum') {
          const parameterTyped = parameter as IpParameterEnum
          display = parameterTyped.values[result].comment.get(i18n.locale.value)
          for (const [key, uint] of Object.entries(parameterTyped.values)) {
            menuModel.push({
              key,
              command: uint.comment.get(i18n.locale.value),
              divided: false,
              preserveIconWidth: false,
            })
          }
        }

        model = {
          ...baseModel,
          width: geometry.width,
          height: geometry.height,
          value: result ?? parameter.default,
          display,
          readonly: parameter.readonly,
          type: parameter.type,
          menu: menuModel,
        }
        allModels[refParameter] = model
      }
      rectModels[name] = model
    }
  }
  allModelsRef.value = allModels
  rectModelsRef.value = rectModels
  circleModelsRef.value = circleModels
  radioGroupModelsRef.value = radioGroupModels

  const blob = new Blob([svg], { type: 'image/svg+xml' })
  const url = URL.createObjectURL(blob)

  const img = new window.Image()
  img.src = url
  img.onload = () => {
    URL.revokeObjectURL(url)
    svgImageRef.value = img
  }
}

function onProjectConfigChanged(payload: { path: string[], oldValue: any, newValue: any }) {
  const [path, value] = [payload.path, payload.newValue]
  if (path.length === 2) {
    const instance = clockTreeIpRef.value!.instance
    if (instance === path[0]) {
      const param = path[1]
      if (param in allModelsRef.value) {
        const model = allModelsRef.value[param]
        if (model.cls === 'rect') {
          const modelTyped = model as RectModelType
          if (modelTyped.type === 'enum') {
            modelTyped.display = (modelTyped.parameter as IpParameterEnum).values[value].comment.get(i18n.locale.value)
          }
        }
        else {
          const modelTyped = model as CircleModelType
          modelTyped.value = value
        }
      }
    }
  }
}

function clampRectToContainer(
  x: number,
  y: number,
  width: number,
  height: number,
  scaleX: number,
  scaleY: number,
) {
  const container = panZoomRef.value?.container
  if (!container)
    return { x, y }

  const { width: limitX, height: limitY } = container.getBoundingClientRect()
  const realWidth = width * scaleX
  const realHeight = height * scaleY

  const clamp = (coord: number, size: number, limit: number, move: (delta: number) => void) => {
    if (coord < 0) {
      move(-coord)
      return 0
    }
    if (coord + size > limit) {
      const delta = coord + size - limit
      move(-delta)
      return limit - size
    }
    return coord
  }

  x = clamp(x, realWidth, limitX, dx => panZoomRef.value?.moveRel(dx, 0))
  y = clamp(y, realHeight, limitY, dy => panZoomRef.value?.moveRel(0, dy))

  return { x, y }
}

function showInput(x: number, y: number, width: number, height: number, scaleX: number, scaleY: number, model: RectModelType) {
  if (!(panZoomRef.value && panZoomRef.value.container)) {
    return
  }
  ({ x, y } = clampRectToContainer(x, y, width, height, scaleX, scaleY))

  inputConfigRef.value.x = x
  inputConfigRef.value.y = y
  inputConfigRef.value.scaleX = scaleX
  inputConfigRef.value.scaleY = scaleY
  inputConfigRef.value.width = width
  inputConfigRef.value.height = height
  inputConfigRef.value.show = true

  model.display = '' /* !< 隐藏当前文本（使用input显示） */
  if (lastRectModel) {
    lastRectModel.display = '1111111' // TODO
  }

  lastRectModel = model

  nextTick(() => {
    inputRef.value?.focus()
  })
}

function hideInput() {
  if (lastRectModel) {
    lastRectModel.display = '1111111' // TODO
  }

  inputConfigRef.value.show = false

  lastRectModel = null
}

function showSelect(x: number, y: number, width: number, height: number, scaleX: number, scaleY: number, model: RectModelType) {
  panZoomRef.value?.openMenu(model.refParameter, {
    x,
    y: y + (height * scaleY),
    maxWidth: width,
    minWidth: width,
    adjustPadding: 0,
    adjustPosition: false,
    yOffset: 0,
  }, model.menu, {
    noStyle: true,
    scaleX,
    scaleY,
  })
}

function handClick(event: Konva.KonvaEventObject<MouseEvent>) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const shape = event.target
    const stage = shape.getStage()
    const model: ModelType | undefined = shape.attrs.model

    if (model === undefined) {
      hideInput()
    }
    else if (model.cls === 'circle') {
      const modelTyped = model as CircleModelType
      for (const [key, unit] of Object.entries(radioGroupModelsRef.value[modelTyped.group])) {
        if (key !== model.name) {
          projectRef.value?.configs.set(unit.path, false)
        }
        else {
          projectRef.value?.configs.set(unit.path, true)
          projectRef.value?.configs.set(`${summaryRef.value!.clockTree.ip}.${modelTyped.group}`, unit.refParameter)
        }
      }
    }
    else if (model.cls === 'rect') {
      const modelTyped = model as RectModelType
      const x = shape.getAbsolutePosition().x
      const y = shape.getAbsolutePosition().y

      if (!modelTyped.readonly) {
        if (modelTyped.type === 'enum') {
          showSelect(x, y, shape.attrs.width, shape.attrs.height, stage?.attrs.scaleX, stage?.attrs.scaleY, modelTyped)
          hideInput()
        }
        else {
          showInput(x, y, shape.attrs.width, shape.attrs.height, stage?.attrs.scaleX, stage?.attrs.scaleY, modelTyped)
        }
      }
    }
  }
}

function handMenuSelect(name: string, _command: string, item: PanZoomMenuItemModelType) {
  const model = allModelsRef.value[name]
  if (model === undefined) { /* empty */ }
  else if (model.cls === 'rect') {
    const modelTyped = model as RectModelType
    projectRef.value?.configs.set(modelTyped.path, item.key)
  }
}

function handResize() {
  hideInput()
}

function handZoom() {
  hideInput()
}

function handDragstart() {
  hideInput()
}

function handRectMouseenter(event: Konva.KonvaEventObject<MouseEvent>) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const container = panZoomRef.value.container
    const shape = event.target
    const model: RectModelType = shape.attrs.model

    if (!model.readonly) {
      if (model.type === 'enum') {
        container.style.cursor = 'pointer'
      }
      else {
        container.style.cursor = 'text'
      }
    }
  }
}

function handRectMouseleave(event: Konva.KonvaEventObject<MouseEvent>) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const container = panZoomRef.value.container
    container.style.cursor = 'default'
  }
}

function handRadioMouseenter(event: Konva.KonvaEventObject<MouseEvent>) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const container = panZoomRef.value.container
    container.style.cursor = 'pointer'
  }
}

function handRadioMouseleave(event: Konva.KonvaEventObject<MouseEvent>) {
  event.evt.preventDefault()
  if (panZoomRef.value && panZoomRef.value.container) {
    const container = panZoomRef.value.container
    container.style.cursor = 'default'
  }
}

onMounted(() => {
  const project = projectManager.get()
  if (project) {
    projectRef.value = project
    const summary = summaryManager.get(project.vendor, project.targetChip)
    if (summary) {
      summaryRef.value = summary
      const ip = ipManager.getPeripheral(project.vendor, summary.clockTree.ip)
      if (ip) {
        clockTreeIpRef.value = ip
        setClockTree(project.vendor, summary.clockTree.svg)
        project.configs.emitter.on('configChanged', onProjectConfigChanged)
      }
    }
  }
})

onBeforeUnmount(() => {
  if (projectRef.value && summaryRef.value && clockTreeIpRef.value) {
    projectRef.value.configs.emitter.off('configChanged', onProjectConfigChanged)
  }
})

defineExpose({
  rescale,
  zoomIn,
  zoomOut,
})
</script>

<template>
  <div class="pan-zoom-container flex">
    <PanZoom
      ref="panZoomRef"
      :model-width="modelWidth"
      :model-height="modelHeight"
      @click="handClick"
      @resize="handResize"
      @zoom="handZoom"
      @dragstart="handDragstart"
      @menu-select="handMenuSelect"
    >
      <v-layer>
        <v-image
          v-if="svgImageRef"
          :config="{
            image: svgImageRef,
          }"
        />
        <v-group
          v-for="[name, model] of Object.entries(rectModelsRef)"
          :key="name"
          @mouseenter="handRectMouseenter($event)"
          @mouseleave="handRectMouseleave($event)"
        >
          <v-rect
            :config="{
              x: model.x,
              y: model.y,
              width: model.width,
              height: model.height,
              stroke: `${model.readonly ? 'black' : '#409eff'}`,
              fill: 'transparent',
              strokeWidth: model.readonly ? 1 : 2,
              model,
            }"
          />
          <v-text
            :config="{
              x: model.x,
              y: model.y,
              width: model.width,
              height: model.height,
              fill: 'black',
              wrap: 'none',
              verticalAlign: 'middle',
              ellipsis: true,
              text: ` ${model.display}`,
              fontSize: 14,
              model,
            }"
          />
        </v-group>
        <v-group
          v-for="[name, model] of Object.entries(circleModelsRef)"
          :key="name"
          @mouseenter="handRadioMouseenter($event)"
          @mouseleave="handRadioMouseleave($event)"
        >
          <v-circle
            :config="{
              x: model.x + model.r,
              y: model.y + model.r,
              radius: model.r,
              stroke: 'black',
              fill: 'white',
              strokeWidth: 1,
              model,
            }"
          />
          <v-circle
            v-if="model.value"
            :config="{
              x: model.x + model.r,
              y: model.y + model.r,
              radius: model.r * 0.5,
              fill: '#41ae3c',
              model,
            }"
          />
        </v-group>
      </v-layer>
    </PanZoom>
    <el-input
      v-show="inputConfigRef.show"
      ref="inputRef"
      v-model="inputConfigRef.value"
      :style="{
        position: 'absolute',
        top: `${inputConfigRef.y}px`,
        left: `${inputConfigRef.x}px`,
        width: `${inputConfigRef.width}px`,
        height: `${inputConfigRef.height}px`,
        transform: `scale(${inputConfigRef.scaleX}, ${inputConfigRef.scaleY})`,
        transformOrigin: 'left top',
      }"
    />
  </div>
</template>

<style scoped>
.pan-zoom-container {
  flex: 1;
  min-width: 0;
  min-height: 0;
  position: relative;
}

::v-deep(.ep-input__wrapper) {
  box-shadow: none;
  border-radius: 0px;
  border-image: none;
  border-image-width: 0px;
  background-color: transparent;
  transition-duration: 0s;
  color: black;
  padding: 0px 0px 1px 0px;
}

::v-deep(.ep-input__inner) {
  color: black;
}
</style>
