/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        routes.ts
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
 *  2025-05-19     xqyjlj       initial version
 */

import type { RouteRecordRaw } from 'vue-router'

const routes: Readonly<RouteRecordRaw[]> = [
  {
    path: '/',
    component: () => import('~/pages/welcome/index.vue'),
  },
  {
    path: '/chipConfigure',
    component: () => import('~/pages/chipConfigure/index.vue'),
  },
  {
    path: '/clockConfigure',
    component: () => import('~/pages/clockConfigure/index.vue'),
  },
  {
    path: '/codeView',
    component: () => import('~/pages/codeView/index.vue'),
  },
  {
    path: '/createProject',
    component: () => import('~/pages/createProject/index.vue'),
  },
  {
    path: '/welcome',
    component: () => import('~/pages/welcome/index.vue'),
  },
  {
    path: '/packageManager',
    component: () => import('~/pages/packageManager/index.vue'),
  },
  {
    path: '/sponsor',
    component: () => import('~/pages/sponsor/index.vue'),
  },
  {
    path: '/settings',
    component: () => import('~/pages/settings/index.vue'),
    children: [
      {
        path: 'system',
        component: () => import('~/pages/settings/system.vue'),
      },
      {
        path: 'generate',
        component: () => import('~/pages/settings/generate.vue'),
      },
    ],
  },
  {
    path: '/startup',
    component: () => import('~/pages/startup/index.vue'),
  },
]

export default routes

function collectImports(rs: Readonly<RouteRecordRaw[]>): Promise<unknown>[] {
  const imports: Promise<unknown>[] = []

  for (const r of rs) {
    if (typeof r.component === 'function') {
      const result = (r.component as () => Promise<unknown>)()
      if (result instanceof Promise) {
        imports.push(result)
      }
    }

    if (r.children) {
      imports.push(...collectImports(r.children))
    }
  }

  return imports
}

export function loadAllRoutes() {
  return Promise.all(collectImports(routes))
}
