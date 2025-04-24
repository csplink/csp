<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        PanZoom.vue
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
 *  2025-05-14     xqyjlj       initial version
-->

<script lang="ts" setup>
import type { MenuOptions } from '@imengyu/vue3-context-menu'
import type Konva from 'konva'
import type { StageConfig } from 'konva/lib/Stage'
import type { PanZoomMenuItemModelType } from './PanZoom'
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

interface PropsType {
  modelWidth: number
  modelHeight: number
}

interface MenuConfigType {
  key?: string
  model?: PanZoomMenuItemModelType[]
}

const props = defineProps<PropsType>()

const emit = defineEmits(['click', 'menuSelect', 'resize', 'zoom', 'dragstart'])

const tooltipTargetRef = ref<HTMLDivElement>()
const containerRef = ref<HTMLDivElement>()
const stageRef = ref<Konva.Stage>()
const stageConfigRef: StageConfig = ref({
  container: containerRef.value,
  scaleX: 0.5,
  scaleY: 0.5,
  draggable: true,
  x: 0,
  y: 0,
  offsetX: 0,
  offsetY: 0,
})
const tooltipConfigRef = ref({
  visible: false,
  x: 0,
  y: 0,
  placement: 'top',
  content: '',
})
const menuConfigRef = ref<MenuConfigType>({})
const menuShowRef = ref(false)
const menuOptionsComponentRef = ref<MenuOptions>()
let resizeObserver: ResizeObserver

watch(
  () => [props.modelWidth, props.modelHeight],
  () => {
    rescale()
  },
)

function openMenu(key: string, options: MenuOptions, model: PanZoomMenuItemModelType[], style: {
  noStyle?: boolean
  scaleX?: number
  scaleY?: number
} = {}) {
  menuConfigRef.value.key = key
  menuConfigRef.value.model = model

  const opts: MenuOptions = {
    getContainer: () => containerRef.value as HTMLElement,
    customClass: `${style.noStyle ? 'no-style-context-menu' : ''} custom-context-menu`,
    mouseScroll: true,
    ...options,
  }

  /* FIXME: 调用会发出警告
   * [Violation] Added non-passive event listener to a scroll-blocking 'wheel' event.
   * Consider marking event handler as 'passive' to make the page more responsive.
   * See https://www.chromestatus.com/feature/5745543795965952
   */
  menuOptionsComponentRef.value = opts
  menuShowRef.value = true

  if (style.scaleX !== undefined && style.scaleY !== undefined) {
    nextTick(() => {
      const menu = document.querySelector('.mx-context-menu.custom-context-menu') as HTMLElement
      if (menu) {
        menu.style.transform = `scale(${style.scaleX}, ${style.scaleY})`
        menu.style.transformOrigin = 'left top'
      }
    })
  }
}

function closeMenu() {
  menuShowRef.value = false
}

function showTooltip(x: number, y: number, placement: string, content: string) {
  tooltipConfigRef.value.x = x
  tooltipConfigRef.value.y = y
  tooltipConfigRef.value.placement = placement
  tooltipConfigRef.value.content = content
  tooltipConfigRef.value.visible = true
}

function hideTooltip() {
  tooltipConfigRef.value.visible = false
}

function rescale() {
  if (containerRef.value && stageRef.value) {
    const containerRect = containerRef.value.getBoundingClientRect()
    const stage = stageRef.value.getStage()
    const containerWidth = containerRect.width
    const containerHeight = containerRect.height
    const width = props.modelWidth || 1
    const height = props.modelHeight || 1

    const scaleX = containerWidth / width
    const scaleY = containerHeight / height

    const scale = Math.min(scaleX, scaleY)

    stageConfigRef.value.scaleX = scale
    stageConfigRef.value.scaleY = scale

    stage.position({
      x: (containerWidth - width * scale) / 2,
      y: (containerHeight - height * scale) / 2,
    })
    stage.batchDraw()
    emit('zoom')
  }
}

function zoomIn() {
  const scaleBy = 1.05
  const oldScale = stageConfigRef.value.scaleX
  const newScale = oldScale * scaleBy
  stageConfigRef.value.scaleX = newScale
  stageConfigRef.value.scaleY = newScale
  emit('zoom')
}

function zoomOut() {
  const scaleBy = 1.05
  const oldScale = stageConfigRef.value.scaleX
  const newScale = oldScale / scaleBy
  if (newScale >= 0.1) {
    stageConfigRef.value.scaleX = newScale
    stageConfigRef.value.scaleY = newScale
  }
  emit('zoom')
}

function moveRel(x: number, y: number) {
  if (containerRef.value && stageRef.value) {
    const stage = stageRef.value.getStage()
    const pos = stage.position()

    stage.position({
      x: pos.x + x,
      y: pos.y + y,
    })
    stage.batchDraw()
  }
}

function handWheel(event: Konva.KonvaEventObject<WheelEvent>) {
  event.evt.preventDefault()

  hideTooltip()
  closeMenu()

  if (stageRef.value) {
    const stage = stageRef.value.getStage()
    const oldScale = stageConfigRef.value.scaleX
    const pointer = stage.getPointerPosition()
    const scaleBy = 1.05
    const direction = event.evt.deltaY > 0 ? -1 : 1
    const newScale = direction > 0 ? oldScale * scaleBy : oldScale / scaleBy
    if (newScale >= 0.1 && pointer) {
      const contentCenter = {
        x: (pointer.x - stage.x()) / oldScale,
        y: (pointer.y - stage.y()) / oldScale,
      }

      const centerScreenPos = {
        x: contentCenter.x * oldScale + stage.x(),
        y: contentCenter.y * oldScale + stage.y(),
      }

      stageConfigRef.value.scaleX = newScale
      stageConfigRef.value.scaleY = newScale

      const newPos = {
        x: centerScreenPos.x - contentCenter.x * newScale,
        y: centerScreenPos.y - contentCenter.y * newScale,
      }

      stage.position(newPos)
      stage.batchDraw()

      emit('zoom')
    }
  }
}

function handDragstart(event: Konva.KonvaEventObject<MouseEvent>) {
  hideTooltip()
  closeMenu()
  emit('dragstart', event)
}

function handClick(event: Konva.KonvaEventObject<MouseEvent>) {
  emit('click', event)
}

function handCommand(item: PanZoomMenuItemModelType) {
  emit('menuSelect', menuConfigRef.value.key, item.command, item)
}

onMounted(() => {
  let firstResize = false
  if (containerRef.value) {
    menuOptionsComponentRef.value = {
      x: 0,
      y: 0,
      getContainer: () => containerRef.value as HTMLElement,
    }

    resizeObserver = new ResizeObserver((entries) => {
      const rect = entries[0].contentRect

      hideTooltip()
      closeMenu()

      emit('resize')

      if (!firstResize) {
        rescale()
        firstResize = true
      }

      stageConfigRef.value.width = rect.width
      stageConfigRef.value.height = rect.height
    })
    resizeObserver.observe(containerRef.value)
  }
})

onBeforeUnmount(() => {
  if (resizeObserver && containerRef.value) {
    resizeObserver.unobserve(containerRef.value)
  }
})

defineExpose({
  container: containerRef,

  openMenu,
  closeMenu,
  showTooltip,
  hideTooltip,
  rescale,
  zoomIn,
  zoomOut,
  moveRel,
})
</script>

<template>
  <div ref="containerRef" class="zoom-stage-container">
    <v-stage
      ref="stageRef"
      :config="stageConfigRef"
      @wheel="handWheel($event)"
      @dragstart="handDragstart($event)"
      @click="handClick($event)"
    >
      <slot />
    </v-stage>
    <!-- hidden binding point for mounting el-tooltip -->
    <div
      ref="tooltipTargetRef"
      :style="{
        position: 'absolute',
        top: `${tooltipConfigRef.y}px`,
        left: `${tooltipConfigRef.x}px`,
        width: '1px',
        height: '1px',
        pointerEvents: 'none',
      }"
    />
    <!-- el-tooltip manual display -->
    <el-tooltip
      :visible="tooltipConfigRef.visible"
      :virtual-ref="tooltipTargetRef"
      virtual-triggering
      :placement="tooltipConfigRef.placement"
    >
      <template #content>
        <div class="tooltip-content">
          <div>
            {{ tooltipConfigRef.content }}
          </div>
        </div>
      </template>
    </el-tooltip>
    <context-menu
      v-if="menuOptionsComponentRef"
      v-model:show="menuShowRef"
      :options="menuOptionsComponentRef"
    >
      <div
        v-for="menuModel in menuConfigRef.model"
        :key="menuModel.key"
      >
        <context-menu-separator v-if="menuModel.divided" />
        <context-menu-item
          :class="menuModel.highlight ? 'bg-dropdown-item' : ''"
          :label="menuModel.command"
          :checked="menuModel.highlight"
          :preserve-icon-width="menuModel.preserveIconWidth"
          @click="handCommand(menuModel)"
        />
      </div>
    </context-menu>
  </div>
</template>

<style scoped>
.zoom-stage-container {
  flex: 1 1 auto;
  min-width: 0;
  min-height: 0;
  overflow: hidden;
}

::v-deep(.bg-dropdown-item) {
  background-color: var(--ep-color-primary);
  color: var(--ep-text-color-primary);
  --mx-menu-hover-backgroud: var(--ep-color-primary);
  --mx-menu-hover-text: var(--ep-text-color-primary);
}

::v-deep(.no-style-context-menu) {
  padding: 0;
  border-radius: 0px;
  border: 1px solid black;
  box-shadow: none;
}

::v-deep(.mx-context-menu-item) {
  padding: 6px 0px 6px 6px;
}
</style>
