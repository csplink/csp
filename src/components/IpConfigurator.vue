<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        IpConfigurator.vue
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
 *  2025-06-01     xqyjlj       initial version
-->

<script setup lang="ts">
import type { ElTable } from 'element-plus'
import type {
  Ip,
  IpParameterEnum,
  IpParameterNumber,
  IpRefParameter,
  Project,
  ProjectConfigsPinUnitType,
  Summary,
} from '~/database'
import { onBeforeUnmount, onMounted, ref, toRefs, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { useIpManager, useProjectManager, useSummaryManager } from '~/database'

// #region type

type IpParameterModelType =
  IpParameterModelEnumType |
  IpParameterModelNumberType |
  IpParameterModelBooleanType |
  IpParameterModelStringType |
  IpParameterModelLabelType

type IpParameterModelTypeType =
  'enum' |
  'integer' |
  'float' |
  'boolean' |
  'radio' |
  'string' |
  'group' |
  'label'

interface ModelType {
  name: string
  key: string
  items: Record<string, IpParameterModelType>
  children: ModelType[]
}

interface IpParameterModelBaseType {
  key: string
  path: string
  param: string
  description: string
  readonly: boolean
  type: IpParameterModelTypeType
  children?: IpParameterModelType[]
}

interface IpParameterModelEnumType extends IpParameterModelBaseType {
  values: Record<string, string>
  value: string
  default: string
}

interface IpParameterModelNumberType extends IpParameterModelBaseType {
  max: number
  min: number
  value: number
  default: number
}

interface IpParameterModelBooleanType extends IpParameterModelBaseType {
  value: boolean
  default: boolean
}

interface IpParameterModelStringType extends IpParameterModelBaseType {
  value: string
  default: string
}

interface IpParameterModelLabelType extends IpParameterModelBaseType {
  value: string
}

interface PropsType {
  type: string
  instance: string
  channel: string
}

// #endregion

const props = defineProps<PropsType>()
const emit = defineEmits(['pinSelect', 'select'])

const projectManager = useProjectManager()
const ipManager = useIpManager()
const summaryManager = useSummaryManager()
const i18n = useI18n()
const { t } = i18n

const { type: typeRef } = toRefs(props)
const projectRef = ref<Project>()
const summaryRef = ref<Summary>()
const modelsRef = ref<ModelType[]>([])
const titleRef = ref<Record<string, string>>({})
const tableRef = ref<InstanceType<typeof ElTable>>()

const pinConfigKeys = ['function', 'locked', 'label']
let usedRefParameters: { refParameter: IpRefParameter, func: (payload: { name: string, oldValue: boolean, newValue: boolean }) => void }[] = []
let currentIp: Ip | null = null

watch(
  () => [props.instance, props.channel],
  (_newVal, _oldVal) => {
    setIp(props.instance, props.channel)
  },
)

function setIp(instance: string, channel: string) {
  cleanUp()

  if (!instance) {
    return
  }

  const ip = ipManager.getPeripheral(projectRef.value!.vendor, instance)
  if (!ip) {
    console.error(`IP '${instance}' not found in project.`)
    return
  }

  currentIp = ip

  let title: Record<string, string>
  let models: ModelType[]
  if (props.type === 'overview') {
    ({ title, models } = buildOverviewModels(ip))
  }
  else if (props.type === 'modes') {
    ({ title, models } = buildModesModels(ip))
  }
  else if (props.type === 'configurations') {
    ({ title, models } = buildConfigurationsModels(ip))
  }
  else if (props.type === 'channel') {
    ({ title, models } = buildChannelModels(ip, channel))
  }
  else {
    console.error(`Unknown type '${props.type}'.`)
    currentIp = null
    return
  }

  modelsRef.value = models
  titleRef.value = title
}

function buildParameterModelItem(
  param: string,
  refParameter: IpRefParameter,
  ip: Ip,
  path: string = `${ip.instance}.${param}`,
  update: boolean = true,
  type: IpParameterModelTypeType | null = null,
): IpParameterModelType | null {
  const parameter = refParameter.parameter
  if (!parameter.visible) {
    return null
  }

  const project = projectRef.value!
  const base: IpParameterModelBaseType = {
    key: param,
    path,
    param,
    description: parameter.description.get(i18n.locale.value),
    readonly: refParameter.readonly,
    type: type || parameter.type,
  }

  let result = project.configs.get(path)
  let model: IpParameterModelType | null = null

  if (!refParameter.condition) {
    base.readonly = true
    result = null /*! < 当前条件不满足时，切换为默认值 */
  }

  switch (parameter.type) {
    case 'enum': {
      const parameterTyped = parameter as IpParameterEnum
      const values = {} as Record<string, string>
      for (const key of refParameter.values) {
        const originValue = parameterTyped.values[key]
        values[originValue.comment.get(i18n.locale.value)] = key
      }

      if (update) {
        if (result) {
          if (!(result in parameterTyped.values)) {
            result = refParameter.default
            project.configs.set(path, result)
          }
        }
        else {
          result = refParameter.default
          project.configs.set(path, result)
        }
      }

      model = {
        ...base,
        values,
        value: (result === null) ? null : parameterTyped.values[result].comment.get(i18n.locale.value),
        default: parameterTyped.values[refParameter.default as string].comment.get(i18n.locale.value),
      } as IpParameterModelEnumType

      break
    }
    case 'boolean': {
      if (update) {
        if (result == null) {
          result = refParameter.default
          project.configs.set(path, result)
        }
      }

      model = {
        ...base,
        value: result,
        default: refParameter.default,
      } as IpParameterModelNumberType

      break
    }
    case 'integer':
    case 'float':
    {
      const parameterTyped = parameter as IpParameterNumber

      if (update) {
        if (result) {
          if (result > parameterTyped.max || result < parameterTyped.min) {
            result = refParameter.default
            project.configs.set(path, result)
          }
        }
        else {
          result = refParameter.default
          project.configs.set(path, result)
        }
      }

      model = {
        ...base,
        max: parameterTyped.max,
        min: parameterTyped.min,
        value: result,
        default: refParameter.default,
      } as IpParameterModelNumberType

      break
    }
    case 'string' :{
      model = {
        ...base,
        value: result || '',
        default: refParameter.default,
      } as IpParameterModelStringType
      break
    }
  }

  return model
}

function buildPinParameterModelItem(_ip: Ip, channel: string, param: string, readonly: boolean, type: IpParameterModelTypeType): IpParameterModelStringType | IpParameterModelLabelType {
  const project = projectRef.value!
  const path = `pins.${channel}.${param}`
  const base: IpParameterModelBaseType = {
    key: `${channel}.${param}`,
    path,
    param,
    description: t(`ipConfigurator.${param}Pin`),
    readonly,
    type,
  }

  let result = project.configs.get(path)
  if (param === 'locked') {
    result = result ? '✔' : '✘'
  }

  let model: IpParameterModelStringType | IpParameterModelLabelType | null = null
  switch (type) {
    case 'string' :{
      model = {
        ...base,
        value: result,
        default: '',
      } as IpParameterModelStringType
      break
    }
    default :{ /*! < label */
      model = {
        ...base,
        value: result,
      } as IpParameterModelLabelType
      break
    }
  }

  return model
}

function buildOverviewModels(ip: Ip): { title: Record<string, string>, models: ModelType[] } {
  const project = projectRef.value!
  const title: Record<string, string> = {}
  const models: ModelType[] = []
  const configs = project.configs.get(ip.instance)
  const refParameters = ip.containers.overview.refParameters
  const pinInstance = summaryRef.value!.pinInstance()

  for (const [param, _refParameter] of Object.entries(refParameters)) {
    const parameter = _refParameter.parameter
    title[param] = parameter.display.get(i18n.locale.value)
  }

  if (typeof configs === 'object') {
    /*! < e.q:
       *  PE1:
       *    gpio_level_t: low
       *    gpio_mode_t: output
       *    gpio_output_type_t: pp
       *    gpio_speed_t: 2mhz
       */
    for (const [channel, config] of Object.entries(configs)) {
      const modelItems: Record<string, IpParameterModelType> = {}
      if (typeof config === 'object' && config !== null) {
        for (const [param, refParameter] of Object.entries(refParameters)) {
          const parameterModel = buildParameterModelItem(
            param,
            refParameter,
            ip,
            `${ip.instance}.${channel}.${param}`,
            false,
            'label',
          )
          if (parameterModel) {
            modelItems[param] = parameterModel
          }
        }
        models.push({
          name: channel,
          key: channel,
          items: modelItems,
          children: [],
        })
      }
      else {
        continue
        // TODO: warning?
      }

      if (pinInstance === ip.instance) {
        modelItems.label = buildPinParameterModelItem(ip, channel, 'label', true, 'label')
        modelItems.function = buildPinParameterModelItem(ip, channel, 'function', true, 'label')
        modelItems.locked = buildPinParameterModelItem(ip, channel, 'locked', true, 'label')
      }
    }
  }

  if (pinInstance === ip.instance) {
    for (const key of pinConfigKeys) {
      title[key] = t(`ipConfigurator.${key}Pin`)
    }
  }

  return { title, models }
}

function buildCommonModels(ip: Ip, refParameters: Record<string, IpRefParameter>): { title: Record<string, string>, models: ModelType[] } {
  const title: Record<string, string> = {}
  const models: ModelType[] = []

  for (const [param, refParameter] of Object.entries(refParameters)) {
    const parameter = refParameter.parameter
    const parameterModel = buildParameterModelItem(param, refParameter, ip)
    if (parameterModel) {
      models.push({
        name: parameter.display.get(i18n.locale.value),
        key: param,
        items: {
          value: parameterModel,
        },
        children: [],
      })
      const handler = (payload: { name: string, oldValue: boolean, newValue: boolean }) => {
        updateParameterModelByCondition(payload.newValue, refParameter, parameterModel)
      }
      refParameter.emitter.on('conditionChanged', handler)
      usedRefParameters.push ({ refParameter, func: handler })
    }
  }
  title.value = t('ipConfigurator.value')
  return { title, models }
}

function buildModesModels(ip: Ip): { title: Record<string, string>, models: ModelType[] } {
  const { title, models } = buildCommonModels(ip, ip.containers.modes.refParameters)

  return { title, models }
}

function buildConfigurationsModels(ip: Ip): { title: Record<string, string>, models: ModelType[] } {
  const { title, models } = buildCommonModels(ip, ip.containers.configurations.refParameters)
  if (props.type === 'configurations') {
    ip.containers.configurations.emitter.on('changed', onIpConfigurationsChanged)
  }
  return { title, models }
}

function buildChannelModels(ip: Ip, channel: string): { title: Record<string, string>, models: ModelType[] } {
  const title: Record<string, string> = {}
  const models: ModelType[] = []
  let refParameters: Record<string, IpRefParameter> = {}
  if (channel) {
    if (summaryRef.value!.pinInstance() === ip.instance) {
      const pinConfig = projectRef.value!.configs.get<ProjectConfigsPinUnitType | null>(`pins.${channel}`)
      if (pinConfig) {
        const key = pinConfig.mode || pinConfig.function
        if (key && key.includes(':')) {
          const pre = key.split(':')[1]
          if (pre) {
            refParameters = ip.presets[pre].refParameters
          }
        }
      }
      if (Object.keys(refParameters).length === 0) {
        console.error(`Pin '${channel}' not found in project.`)
      }
    }
  }

  for (const [param, refParameter] of Object.entries(refParameters)) {
    const parameter = refParameter.parameter
    const parameterModel = buildParameterModelItem(param, refParameter, ip, `${ip.instance}.${channel}.${param}`)
    if (parameterModel) {
      models.push({
        name: parameter.display.get(i18n.locale.value),
        key: param,
        items: {
          value: parameterModel,
        },
        children: [],
      })

      const handler = (payload: { name: string, oldValue: boolean, newValue: boolean }) => {
        updateParameterModelByCondition(payload.newValue, refParameter, parameterModel)
      }
      refParameter.emitter.on('conditionChanged', handler)
      usedRefParameters.push ({ refParameter, func: handler })
    }
  }

  if (summaryRef.value!.pinInstance() === ip.instance) {
    const parameterModel = buildPinParameterModelItem(ip, channel, 'label', false, 'string')
    models.push({
      name: t('ipConfigurator.labelPin'),
      key: 'label',
      items: {
        value: parameterModel,
      },
      children: [],
    })
  }

  title.value = t('ipConfigurator.value')
  return { title, models }
}

function updateParameterModelByCondition(condition: boolean, refParameter: IpRefParameter, parameterModel: IpParameterModelType) {
  if (!currentIp) {
    return
  }
  const parameter = refParameter.parameter
  const project = projectRef.value!

  if (!condition) {
    const defaultValue = refParameter.default
    parameterModel.readonly = true
    if (parameter.type === 'enum') {
      const values = (parameterModel as IpParameterModelEnumType).values
      const key = Object.keys(values).find(k => values[k as keyof typeof values] === defaultValue) as string
      parameterModel.value = key
      project.configs.set(parameterModel.path, defaultValue)
    }
    else {
      parameterModel.value = defaultValue
      project.configs.set(parameterModel.path, defaultValue)
    }
  }
  else {
    parameterModel.readonly = refParameter.readonly
  }
}

function findModelIndex(key: string): number {
  for (let i = 0; i < modelsRef.value.length; i++) {
    if (modelsRef.value[i].key === key) {
      return i
    }
  }
  return -1
}

function tr(param: string, value: any): string {
  if (typeof value === 'boolean' && param === 'locked') {
    return value ? '✔' : '✘'
  }

  if (currentIp === null) {
    return value
  }

  if (param in currentIp.parameters && currentIp.parameters[param].type === 'enum') {
    return (currentIp.parameters[param] as IpParameterEnum).values[value].comment.get(i18n.locale.value)
  }

  return value
}

function getRefParameterByPath(param: string): IpRefParameter | null {
  if (props.type === 'overview') {
    return currentIp?.containers.overview.refParameters[param] || null
  }
  return null
}

function updateOverviewModelByPath(path: string[], value: any) {
  const instance = path[0]

  if (typeof value === 'object') {
    tableRef.value?.setCurrentRow(-1)
  }

  if (path.length === 2) {
    const name = path[1]
    const index = findModelIndex(name)
    if ((value === null)
      || (typeof value === 'string' && value.length === 0)
      || (Array.isArray(value) && value.length === 0)
      || (typeof value === 'object' && Object.keys(value).length === 0)
    ) { /*! < 清空 */
      if (index >= 0) { /*! < 已经存在了该节点，将其删除 */
        modelsRef.value.splice(index, 1)
      }
    }
    else {
      if (typeof value === 'object') {
        /*! < 构建 model */
        const model: Record<string, IpParameterModelType> = {}
        for (const [param, _val] of Object.entries(value)) {
          const refParameter = getRefParameterByPath(param)
          let parameterModel: IpParameterModelType | null = null
          if (refParameter) {
            parameterModel = buildParameterModelItem(
              param,
              refParameter,
              currentIp!,
              `${currentIp!.instance}.${name}.${param}`,
              false,
              'label',
            )
          }
          else {
            parameterModel = buildPinParameterModelItem(
              currentIp!,
              name,
              param,
              true,
              'label',
            )
          }

          if (parameterModel) {
            model[param] = parameterModel
          }
        }

        if (index >= 0) { /*! < 已经存在了该节点，在 GPIO + pins 场景出现时，需要合并 */
          const origin = modelsRef.value[index]
          if (instance === summaryRef.value!.pinInstance()) { /*! < GPIO, 合并 pins 数据 */
            for (const [param, val] of Object.entries(origin.items)) {
              if (pinConfigKeys.includes(param)) {
                model[param] = val
              }
            }
          }
          else if (instance === 'pins') { /*! < pins, 合并 GPIO 数据 */
            for (const [param, val] of Object.entries(origin.items)) {
              if (!pinConfigKeys.includes(param)) {
                model[param] = val
              }
            }
          }
          modelsRef.value[index].items = model
        }
        else { /*! < 不存在，创建该节点 */
          if (instance === 'pins'
            && projectRef.value?.configs.get(`${summaryRef.value!.pinInstance()}.${name}`) == null) {
            /*! < 当GPIO没有配置的时候, pins 无需自动创建 */
          }
          else {
            modelsRef.value.push({
              name,
              key: name,
              items: model,
              children: [],
            })
          }
        }
      }
      else {
        console.warn(`The config '${name}' not found.`)
      }
    }
  }
  else if (path.length === 3) {
    const name = path[1]
    const param = path[2]
    const index = findModelIndex(name)
    const display = tr(param, value)
    if (index >= 0) { /*! < 已经存在了该节点 */
      modelsRef.value[index].items[param].value = display
    }
    else { /*! < 不存在，创建该节点 */
      const refParameter = getRefParameterByPath(param)
      if (refParameter === null) {
        console.warn(`The config '${name}' not found.`)
        return
      }

      const parameterModel = buildParameterModelItem(
        param,
        refParameter,
        currentIp!,
        `${currentIp!.instance}.${name}.${param}`,
        false,
        'label',
      )
      if (parameterModel) {
        modelsRef.value.push({
          name,
          key: name,
          items: {
            [param]: parameterModel,
          },
          children: [],
        })
      }
    }
  }
}

// #region slot

function onIpConfigurationsChanged() {
  setIp(props.instance, props.channel)
}

function onProjectConfigChanged(payload: { path: string[], oldValue: any, newValue: any }) {
  const [path, value] = [payload.path, payload.newValue]
  const instance = path[0]
  console.log(path, value)
  if (instance === currentIp?.instance) {
    if (props.type === 'overview') {
      updateOverviewModelByPath(path, value)
    }
    else {
      if (typeof value !== 'object') {
        console.log(path, value)
      }
    }
  }
}

function onProjectPinConfigChanged(payload: { path: string[], oldValue: any, newValue: any }) {
  const [path, value] = [payload.path, payload.newValue]
  console.log(path, value)
  if (currentIp?.instance === summaryRef.value!.pinInstance()) {
    if (props.type === 'overview') {
      updateOverviewModelByPath(path, value)
    }
    else {
      if (typeof value !== 'object') {
        console.log(path, value)
      }
    }
  }
}

// #endregion

// #region type guard

function isEnumModel(model: IpParameterModelType): model is IpParameterModelEnumType {
  return model.type === 'enum'
}

function isNumberModel(model: IpParameterModelType): model is IpParameterModelNumberType {
  return model.type === 'integer' || model.type === 'float'
}

function isBooleanModel(model: IpParameterModelType): model is IpParameterModelBooleanType {
  return model.type === 'boolean'
}

function isStringModel(model: IpParameterModelType): model is IpParameterModelStringType {
  return model.type === 'string'
}

function isLabelModel(model: IpParameterModelType): model is IpParameterModelLabelType {
  return model.type === 'label'
}

// #endregion

function handSelectChange(value: string, model: IpParameterModelEnumType) {
  projectRef.value!.configs.set(model.path, model.values[value])
}

function handNumberChange(value: number | null, model: IpParameterModelNumberType) {
  if (value === null) {
    model.value = model.default
    return
  }

  projectRef.value!.configs.set(model.path, value)
}

function handCheckboxChange(value: boolean, model: IpParameterModelBooleanType) {
  projectRef.value!.configs.set(model.path, value)
}

function handStringChange(value: string, model: IpParameterModelStringType) {
  projectRef.value!.configs.set(model.path, value)
}

function handCurrentChange(newSelection: ModelType | null, _oldSelection: ModelType | null) {
  if (newSelection && props.type === 'overview') {
    if (currentIp?.instance === summaryRef.value!.pinInstance()) {
      emit('pinSelect', newSelection ? [newSelection.name] : [])
    }

    emit('select', newSelection ? [newSelection.name] : [])
  }
}

function cleanUp() {
  if (currentIp) {
    if (props.type === 'configurations') {
      currentIp.containers.configurations.emitter.off('changed', onIpConfigurationsChanged)
    }
    currentIp = null
  }

  if (usedRefParameters.length > 0) {
    for (const value of usedRefParameters) {
      value.refParameter.emitter.off('conditionChanged', value.func)
    }
    usedRefParameters = []
  }

  titleRef.value = {}
  modelsRef.value = []
}

onMounted(async () => {
  const project = projectManager.get()
  if (project) {
    projectRef.value = project
    const summary = summaryManager.get(project.vendor, project.targetChip)
    if (summary) {
      summaryRef.value = summary
      setIp(props.instance, props.channel)

      project.configs.emitter.on('configChanged', onProjectConfigChanged)
      project.configs.emitter.on('pinConfigChanged', onProjectPinConfigChanged)
    }
  }
})

onBeforeUnmount(() => {
  if (projectRef.value && summaryRef.value) {
    projectRef.value.configs.emitter.off('configChanged', onProjectConfigChanged)
    projectRef.value.configs.emitter.off('pinConfigChanged', onProjectPinConfigChanged)
  }

  cleanUp()
})
</script>

<template>
  <el-table
    ref="tableRef"
    class="ip-configurator-table"
    row-key="key"
    :data="modelsRef"
    :border="true"
    :highlight-current-row="typeRef === 'overview'"
    :tree-props="{ children: 'children' }"
    @current-change="handCurrentChange"
  >
    <el-table-column
      :label="$t('ipConfigurator.name')"
      :sortable="true"
      :show-overflow-tooltip="true"
      :min-width="50"
      prop="name"
      :width="(Object.keys(titleRef).length === 1) ? undefined : 78"
    />
    <el-table-column
      v-for="([prop, label], index) in Object.entries(titleRef)"
      :key="prop"
      :label="label"
      :min-width="50"
      :show-overflow-tooltip="true"
      :width="index === (Object.keys(titleRef).length - 1) ? undefined : label.length * 14 + 50"
    >
      <template #default="{ row }: { row: ModelType }">
        <template v-for="(itemModel, idx) in [(row.items[prop] ?? {})]" :key="idx">
          <template v-if="isEnumModel(itemModel)">
            <el-select
              v-model="itemModel.value"
              value-key="key"
              :placeholder="$t('ipConfigurator.select')"
              :disabled="itemModel.readonly"
              @change="(value) => handSelectChange(value, itemModel)"
            >
              <el-option
                v-for="[display, key] in Object.entries(itemModel.values)"
                :key="key"
                :value="display"
              />
            </el-select>
          </template>
          <template v-else-if="isNumberModel(itemModel)">
            <el-input-number
              v-model="itemModel.value"
              :step="1"
              :step-strictly="itemModel.type === 'integer'"
              :controls="false"
              :min="itemModel.min"
              :max="itemModel.max"
              :disabled="itemModel.readonly"
              :placeholder="`${itemModel.min} ~ ${itemModel.max}`"
              @change="(newValue, _oldValue) => handNumberChange(newValue ?? null, itemModel)"
            />
          </template>
          <template v-else-if="isStringModel(itemModel)">
            <el-input
              v-model="itemModel.value"
              :disabled="itemModel.readonly"
              :placeholder="itemModel.description"
              @change="(value) => handStringChange(value, itemModel)"
            />
          </template>
          <template v-else-if="isBooleanModel(itemModel)">
            <el-checkbox
              v-model="itemModel.value"
              :disabled="itemModel.readonly"
              @change="(value) => handCheckboxChange(value as boolean, itemModel)"
            />
          </template>
          <template v-else-if="isLabelModel(itemModel)">
            {{ itemModel.value }}
          </template>
        </template>
      </template>
    </el-table-column>
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
