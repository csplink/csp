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
    component: () => import('~/pages/startup/index.vue'),
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
    path: '/settings',
    component: () => import('~/pages/settings/index.vue'),
    children: [
      {
        path: '',
        redirect: '/settings/system',
      },
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
