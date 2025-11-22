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
    newChipProject: '新建芯片工程',
    openProject: '打开工程',
  },
  moduleTree: {
    peripherals: '外设',
    middlewares: '中间件',
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
  command: {
    file: '文件',
    new: '新建',
    open: '打开',
    openRecent: '打开最近的工程',
    save: '保存',
    saveAs: '另存为',
    generate: '生成',
    exit: '退出',
    export: '导出',
    alignLeft: '左对齐',
    alignRight: '右对齐',
    alignTop: '顶端对齐',
    alignBottom: '低端对齐',
    alignHorizontalCenter: '水平居中',
    alignVerticalCenter: '垂直居中',
    distributeHorizontally: '水平分布',
    distributeVertically: '垂直分布',
    ok: '确定',
    cancel: '取消',
    zoomIn: '放大',
    zoomOut: '缩小',
    fullScreen: '全屏',
    diff: '差异',
    highlight: '高亮',
    clear: '清除',
    help: '帮助',
    welcome: '欢迎',
    library: '库',
    install: '安装',
    devTools: '开发者工具',
    uninstall: '卸载',
  },
  packageInfo: {
    type: '类型',
    license: '许可证',
    vendor: '供应商',
    description: '描述',
    support: '支持',
    authorInfo: '作者信息',
    author: '作者',
    email: '邮箱',
    blog: '博客',
    visitBlog: '访问博客',
    visitGitHub: '访问 GitHub',
    relatedLinks: '相关链接',
    visitProjectHomepage: '访问项目主页',
  },
  message: {
    openCspProject: '打开 CSP 工程',
    generateFailed: '生成失败，请检查日志',
    generateSuccess: '生成成功',
    dumpFailed: '导出失败，请检查日志',
    dumpSuccess: '导出成功',
    installPackage: '安装软件包',
    installSuccess: '安装成功',
    installFailed: '安装失败，请检查日志',
    uninstallSuccess: '卸载成功',
    uninstallFailed: '卸载失败，请检查日志',
  },
  pin: {
    function: '功能',
    locked: '锁定',
    label: '标签',
  },
  label: {
    problems: '问题',
    logs: '日志',
    error: '错误',
    success: '成功',
    name: '名称',
    pleaseSelect: '请选择',
    systemSetting: '系统设置',
    personalization: '个性化',
    applicationTheme: '应用主题',
    themeColor: '主题色',
    system: '系统',
    language: '语言',
    softwareUpdate: '软件更新',
    autoUpdate: '自动更新',
    checkForUpdates: '检查更新',
    privacy: '隐私',
    telemetry: '数据统计',
    crashReports: '崩溃报告',
    version: '版本',
    license: '许可证',
    author: '作者',
    light: '浅色',
    dark: '深色',
    autoTheme: '跟随系统设置',
    about: '关于',
    generateSetting: '生成设置',
    linker: '链接器',
    heapSize: '堆大小',
    stackSize: '栈大小',
    builder: '构建器',
    builderTool: '构建工具',
    builderVersion: '构建版本',
    toolchains: '工具链',
    useToolchains: '使用工具链',
    toolchainsVersion: '工具链版本',
    toolchainsPath: '工具链路径',
    hal: 'HAL库',
    copyHalLibrary: '复制HAL库',
    halVersion: 'HAL版本',
    halPath: 'HAL路径',
    today: '今天',
    yesterday: '昨天',
    daysAgo: '{days} 天前',
    clock: '时钟',
    code: '代码',
    sponsor: '赞助',
    packages: '软件包',
    settings: '设置',
    dumping: '加载中...',
    generating: '生成中...',
    installing: '安装中...',
    progress: '进度',
    currentFile: '当前文件',
  },
  fileType: {
    csp: 'CSP 工程文件',
    csppack: 'CSP 软件包',
  },
}
