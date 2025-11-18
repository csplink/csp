<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        generate.vue
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
 *  2025-05-18     xqyjlj       initial version
-->

<script setup lang="ts">
import type { FormRules } from 'element-plus'
import { reactive } from 'vue'
import { useProjectManager } from '~/utils'

const projectManager = useProjectManager()
const project = projectManager.get()!

const rules: FormRules = reactive({
  heapSize: [
    {
      required: true,
      message: '请输入堆大小',
      trigger: 'blur',
    },
    {
      validator: linkerValidator,
      trigger: 'blur',
    },
  ],
  stackSize: [
    {
      required: true,
      message: '请输入栈大小',
      trigger: 'blur',
    },
    {
      validator: linkerValidator,
      trigger: 'blur',
    },
  ],
})

const formModel = {
  heapSize: project.gen.linker.heapSize,
  stackSize: project.gen.linker.stackSize,

  builder: project.gen.builder,
  builderVersion: project.gen.builderVersion,
  toolchains: project.gen.toolchains,
  useToolchainsPackage: project.gen.useToolchainsPackage,
  toolchainsVersion: project.gen.toolchainsVersion,
  toolchainsPath: project.gen.toolchainsPath,

  copyHalLibrary: project.gen.copyLibrary,
  hal: project.gen.hal,
  halVersion: project.gen.halVersion,
}

function linkerValidator(_rule: any, value: number, callback: (error?: Error) => void) {
  if (value === 0) {
    callback(new Error('请输入有效的十六进制值 (例如: 0x1000)'))
    return
  }

  callback()
}
</script>

<template>
  <div class="g-settings-container">
    <el-form :model="formModel" label-position="left" label-width="auto" :rules="rules">
      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.linker') }}
        </h2>
        <el-form-item class="g-settings-item" :label="$t('label.heapSize')" prop="heapSize">
          <HexDecInput v-model="formModel.heapSize.value" :disabled="formModel.heapSize.value < 0" />
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.stackSize')" prop="stackSize">
          <HexDecInput v-model="formModel.stackSize.value" :disabled="formModel.stackSize.value < 0" />
        </el-form-item>
      </div>

      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.builder') }}
        </h2>
        <el-form-item class="g-settings-item" :label="$t('label.builderTool')" :required="true">
          <el-select v-model="formModel.builder.value">
            <el-option
              v-for="option in project.gen.builders"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.builderVersion')" :required="true">
          <el-select v-model="formModel.builderVersion.value">
            <el-option
              v-for="option in project.gen.builderVersions"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.toolchains')" :required="true">
          <el-select v-model="formModel.toolchains.value">
            <el-option
              v-for="option in project.gen.toolchainsList"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="g-settings-item">
          <el-switch
            v-model="formModel.useToolchainsPackage.value"
            :active-text="$t('label.useToolchains')"
          />
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.toolchainsVersion')" :required="formModel.useToolchainsPackage.value">
          <el-select v-model="formModel.toolchainsVersion.value" :disabled="!formModel.useToolchainsPackage.value">
            <el-option
              v-for="option in project.gen.toolchainsVersions"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.toolchainsPath')">
          <el-input v-model="formModel.toolchainsPath.value" :disabled="!formModel.useToolchainsPackage.value" :readonly="true" />
        </el-form-item>
      </div>

      <div class="g-settings-section">
        <h2 class="g-settings-title">
          {{ $t('label.hal') }}
        </h2>
        <el-form-item class="g-settings-item">
          <el-switch
            v-model="formModel.copyHalLibrary.value"
            :active-text="$t('label.copyHalLibrary')"
          />
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.hal')" prop="hal" :required="true">
          <el-select v-model="formModel.hal.value">
            <el-option
              v-for="option in project.gen.hals"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.halVersion')" prop="halVersion" :required="true">
          <el-select v-model="formModel.halVersion.value">
            <el-option
              v-for="option in project.gen.halVersions"
              :key="option"
              :label="option"
              :value="option"
            />
          </el-select>
        </el-form-item>
        <el-form-item class="g-settings-item" :label="$t('label.halPath')">
          <el-input v-model="project.gen.halPath.value" :readonly="true" />
        </el-form-item>
      </div>
    </el-form>
  </div>
</template>

<style scoped>
</style>
