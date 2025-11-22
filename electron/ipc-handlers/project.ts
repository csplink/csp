/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        project.ts
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

import type { ProjectType, SystemBrowserWindow } from '@/electron/types'
import type { IpcMainEvent, IpcMainInvokeEvent } from 'electron'
import { BrowserWindow, ipcMain } from 'electron'
import { closeAllSubWindow, createWindow } from '../src/window'
import {
  addRecentProjects,
  checkProjectByPath,
  createProject,
  getProject,
  saveProject,
} from '../utils'

export function registerProjectHandler() {
  ipcMain.handle('project:get', async (event: IpcMainInvokeEvent) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    const data = win.userData!
    addRecentProjects(data.projectPath!)
    return getProject(data.projectPath!)
  })
  ipcMain.handle('project:getPath', async (event: IpcMainInvokeEvent) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    const data = win.userData!
    return data.projectPath!
  })
  ipcMain.on('project:setPath', (event: IpcMainEvent, path: string) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    const data = win.userData!
    if (!checkProjectByPath(path)) {
      return
    }
    createWindow({ runMode: 'main', projectPath: path, backendUrl: data.backendUrl })
    win.close()
  })
  ipcMain.handle('project:save', async (event: IpcMainInvokeEvent, project: ProjectType) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    const data = win.userData!
    await saveProject(data.projectPath!, project)
  })
  ipcMain.handle('project:saveAs', async (event: IpcMainInvokeEvent, newPath: string, project: ProjectType) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    const data = win.userData!
    const projectPath = await createProject(newPath, project)/* !< 创建新项目文件 */
    createWindow({ runMode: 'main', projectPath, backendUrl: data.backendUrl })/* !< 打开新窗口 */
    win.close()/* !< 关闭当前窗口 */
  })
  ipcMain.on('project:create', async (event: IpcMainEvent, path: string, project: ProjectType) => {
    const win = BrowserWindow.fromWebContents(event.sender) as SystemBrowserWindow
    const data = win.userData!
    const projectPath = await createProject(path, project)
    closeAllSubWindow()
    createWindow({ runMode: 'main', projectPath, backendUrl: data.backendUrl })
  })
}
