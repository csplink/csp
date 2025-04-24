/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        zh-cn.ts
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
 *  2025-04-29     xqyjlj       initial version
 */

import zhLocale from 'element-plus/es/locale/lang/zh-cn'

export default {
  ...zhLocale,
  startup: {
    command: '我需要：',
    contributors: '贡献者',
    recentProjects: '最近打开的工程',
    more: '更多',
    newSocProject: '新建 SOC 工程',
    openProject: '打开工程',
  },
  mainNavigation: {
    clock: '时钟',
    code: '代码',
    generate: '生成',
    sponsor: '赞助',
    packages: '软件包',
    settings: '设置',
  },
  settings: {
    systemSetting: '系统设置',
    personalization: '个性化',
    applicationTheme: '应用主题',
    themeColor: '主题色',
    system: '系统',
    softwareUpdate: '软件更新',
    update: '自动更新',
    language: '语言',
    about: '关于',
    help: '帮助',
    feedback: '反馈',
    light: '浅色',
    dark: '深色',
    autoTheme: '跟随系统设置',
    generateSetting: '生成设置',
  },
  titleHeader: {
    file: '文件',
    fileNew: '新建',
    fileOpen: '打开',
    fileOpenRecent: '打开最近的工程',
    fileSave: '保存',
    fileSaveAs: '另存为',
    fileGenerate: '生成',
    fileExit: '退出',
  },
  moduleTree: {
    peripherals: '外设',
    middlewares: '中间件',
    highlight: '高亮引脚',
  },
  chipPackage: {
    resetState: '重置状态',
    labelMessageBoxMessage: '请输入标签',
    labelMessageBoxTitle: '设置标签',
    labelMessageBoxInputPlaceholder: '标签',
    labelMessageBoxInputErrorMessage: '无效标签',
  },
  chipConfigure: {
    overview: '概览',
    modes: '模式',
    configurations: '配置',
  },
  codeFileTree: {
    diff: '差异',
  },
  ipConfigurator: {
    name: '名称',
    value: '值',
    select: '请选择',
    functionPin: '功能',
    lockedPin: '锁定',
    modePin: '模式',
    labelPin: '标签',
  },
  base: {
    ok: '确定',
    cancel: '取消',
  },
}
