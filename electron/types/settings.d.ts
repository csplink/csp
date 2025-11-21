/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        settings.d.ts
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
 *  2025-08-12     xqyjlj       initial version
 */

import type { I18nModeType } from './i18n'
import type { ThemeModeType } from './theme'

export interface SettingsRecentProjectItemType {
  path: string /* !< 项目路径 */
  lastModified: string /* !< 上一次修改时间 (ISO 8601 格式) */
  projectName: string /* !< 工程名 */
  targetChip: string /* !< 芯片名 */
}

export interface AppSettingsType {
  system: SystemSettingsType
  recentProjects: Record<string, SettingsRecentProjectItemType> /* !< key 为项目路径 */
}

export interface SystemSettingsType {
  theme: ThemeModeType
  themeColor: string
  language: I18nModeType
  autoUpdate: boolean
  telemetry: boolean
  crashReports: boolean
  autoSave: boolean
}
