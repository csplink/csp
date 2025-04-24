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

import * as ElIcons from '@element-plus/icons-vue'
import ContextMenu from '@imengyu/vue3-context-menu'
import { createApp } from 'vue'
import VueKonva from 'vue-konva'
import {
  createClockTreeManagerPlugin,
  createContributorManagerPlugin,
  createIpManagerPlugin,
  createProjectManagerPlugin,
  createSummaryManagerPlugin,
} from '~/database'
import { createValueHubPlugin } from '~/events'
import App from './App.vue'
import I18n from './i18n'
import Router from './router'
import Pinia from './store'

import '~/styles/index.scss'
import 'uno.css'
import 'element-plus/theme-chalk/src/message.scss'
import 'element-plus/theme-chalk/src/message-box.scss'
import '@imengyu/vue3-context-menu/lib/vue3-context-menu.css'

const modules = import.meta.glob('~/assets/images/icons/*.svg', { eager: true })

async function main() {
  const app = createApp(App)
  for (const name in ElIcons) {
    app.component(name, (ElIcons as any)[name])
  }

  for (const path in modules) {
    function toComponentName(file: string): string {
      const name = file.replace('.svg', '')
      const parts = name.split(/[-_]/g) // 支持 folder-src / folder_src
      const pascalCase = parts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join('')
      return `Material${pascalCase}`
    }

    const fileName = path.split('/').pop()!
    const componentName = toComponentName(fileName)
    const component = modules[path] as any
    app.component(componentName, component)
  }

  app.use(Router)
  app.use(I18n)
  app.use(Pinia)
  app.use(VueKonva)
  app.use(ContextMenu)

  const valueHubPlugin = createValueHubPlugin()

  const clockTreeManagerPlugin = createClockTreeManagerPlugin()
  const contributorManagerPlugin = createContributorManagerPlugin()
  const ipManagerPlugin = createIpManagerPlugin(valueHubPlugin.value)
  const summaryManagerPlugin = createSummaryManagerPlugin(ipManagerPlugin.value)
  const projectManagerPlugin = await createProjectManagerPlugin(
    valueHubPlugin.value,
    summaryManagerPlugin.value,
    clockTreeManagerPlugin.value,
    ipManagerPlugin.value,
  )

  app.use(valueHubPlugin.plugin)

  app.use(clockTreeManagerPlugin.plugin)
  app.use(contributorManagerPlugin.plugin)
  app.use(ipManagerPlugin.plugin)
  app.use(projectManagerPlugin.plugin)
  app.use(summaryManagerPlugin.plugin)

  app.mount('#app')
}

main()
