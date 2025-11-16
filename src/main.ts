/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        main.ts
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

import ContextMenu from '@imengyu/vue3-context-menu'
import Prism from 'prismjs'
import { createApp } from 'vue'
import VueKonva from 'vue-konva'
import {
  createClockTreeManagerPlugin,
  createIpManagerPlugin,
  createRepositoryManagerPlugin,
  createSummaryManagerPlugin,
} from '~/database'
import {
  createContributorManagerPlugin,
  createPackageManagerPlugin,
  createPinsManagerPlugin,
  createProjectManagerPlugin,
  createServerManagerPlugin,
  createSettingsManagerPlugin,
  getSystemArgs,
  useSystemStore,
} from '~/utils'

import App from './App.vue'
import I18n from './i18n'
import Router from './router'
import { loadAllRoutes } from './router/routes'
import Pinia from './store'

import '~/styles/index.scss'
import 'uno.css'
import 'element-plus/theme-chalk/src/message.scss'
import 'element-plus/theme-chalk/src/message-box.scss'
import 'element-plus/theme-chalk/src/notification.scss'
import 'element-plus/theme-chalk/src/loading.scss'
import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'
import 'remixicon/fonts/remixicon.css'

const materialModules = import.meta.glob('~/../resources/images/icons/material/*.svg', { eager: true })

async function main() {
  const app = createApp(App)

  Prism.languages.xmake = Prism.languages.lua

  for (const path in materialModules) {
    function toComponentName(file: string): string {
      const name = file.replace('.svg', '')
      const parts = name.split(/[-_]/g) /* !< folder-src / folder_src */
      const pascalCase = parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('')
      return `Material${pascalCase}`
    }

    const fileName = path.split('/').pop()!
    const componentName = toComponentName(fileName)
    const component = materialModules[path] as any
    app.component(componentName, component)
  }

  app.use(Router)
  app.use(I18n)
  app.use(Pinia)
  app.use(VueKonva)
  app.use(ContextMenu)

  const args = await getSystemArgs()
  useSystemStore().args = args

  const settingsManagerPlugin = createSettingsManagerPlugin()
  const serverManagerPlugin = createServerManagerPlugin()
  const contributorManagerPlugin = createContributorManagerPlugin()

  await settingsManagerPlugin.init(I18n)
  await serverManagerPlugin.init()

  app.use(settingsManagerPlugin.plugin)
  app.use(serverManagerPlugin.plugin)
  app.use(contributorManagerPlugin.plugin)

  if (args.runMode === 'startup') {
    app.mount('#app')
    window.electron.send('app:mounted')
    return
  }

  const packageManagerPlugin = createPackageManagerPlugin(serverManagerPlugin.manager)
  const clockTreeManagerPlugin = createClockTreeManagerPlugin()
  const summaryManagerPlugin = createSummaryManagerPlugin()
  const projectManagerPlugin = createProjectManagerPlugin(I18n)
  const ipManagerPlugin = createIpManagerPlugin()
  const repositoryManagerPlugin = createRepositoryManagerPlugin()
  const pinsManagerPlugin = createPinsManagerPlugin()

  await projectManagerPlugin.load()
  const project = projectManagerPlugin.project()

  summaryManagerPlugin.setIpManager(ipManagerPlugin.manager)
  summaryManagerPlugin.setClockTreeManager(clockTreeManagerPlugin.manager)
  ipManagerPlugin.setProject(project)
  ipManagerPlugin.setI18n(I18n)
  clockTreeManagerPlugin.setIpManager(ipManagerPlugin.manager)

  await packageManagerPlugin.init()
  await projectManagerPlugin.init(
    summaryManagerPlugin.manager,
    packageManagerPlugin.manager,
  )
  pinsManagerPlugin.init(projectManagerPlugin.manager, summaryManagerPlugin.manager, ipManagerPlugin.manager)

  app.use(packageManagerPlugin.plugin)
  app.use(clockTreeManagerPlugin.plugin)
  app.use(summaryManagerPlugin.plugin)
  app.use(projectManagerPlugin.plugin)
  app.use(ipManagerPlugin.plugin)
  app.use(repositoryManagerPlugin.plugin)
  app.use(pinsManagerPlugin.plugin)

  if (args.runMode === 'main') {
    await loadAllRoutes()
  }

  app.mount('#app')
  window.electron.send('app:mounted')
}

main()
