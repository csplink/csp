<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        RecentProjectsCard.vue
 *  @brief       最近项目卡片组件
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
 *  2025-11-21     xqyjlj       initial version
-->

<script setup lang="ts">
import type { SettingsRecentProjectItemType } from '@/electron/types'
import { computed, shallowRef } from 'vue'
import { useI18n } from 'vue-i18n'
import { setProjectPath, useSettingsManager } from '~/utils'

const { t } = useI18n()
const settings = useSettingsManager()

const refreshTrigger = shallowRef(0)

const recentProjects = computed((): SettingsRecentProjectItemType[] => {
  // eslint-disable-next-line ts/no-unused-expressions
  refreshTrigger.value
  const projects = Object.values(settings.settings.recentProjects) as SettingsRecentProjectItemType[]
  return projects.sort((a, b) => new Date(b.lastModified).getTime() - new Date(a.lastModified).getTime())
})

function formatDate(dateString: string) {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))

  if (diffDays === 0) {
    return t('label.today')
  }
  else if (diffDays === 1) {
    return t('label.yesterday')
  }
  else if (diffDays < 7) {
    return t('label.daysAgo', { days: diffDays })
  }
  else {
    return date.toLocaleDateString()
  }
}

function handleProjectClick(project: SettingsRecentProjectItemType) {
  setProjectPath(project.path)
}

function handleProjectRemove(event: Event, project: SettingsRecentProjectItemType) {
  event.stopPropagation()

  settings.settings.removeRecentProject(project.path)
  refreshTrigger.value++
}
</script>

<template>
  <el-scrollbar class="panel-scrollbar">
    <div class="recent-projects-card">
      <div v-if="recentProjects.length !== 0" class="projects-list">
        <template v-for="project in recentProjects" :key="project.path">
          <el-tooltip :content="project.path" placement="right">
            <div
              class="project-item"
              @click="handleProjectClick(project)"
            >
              <div class="project-icon">
                <i class="ri-cpu-line" />
              </div>
              <div class="project-name">
                {{ project.projectName }}
              </div>
              <div class="project-chip">
                {{ project.targetChip }}
              </div>
              <div class="project-time">
                {{ formatDate(project.lastModified) }}
              </div>
              <div
                class="project-remove"
                @click="handleProjectRemove($event, project)"
              >
                <i class="ri-close-line" />
              </div>
            </div>
          </el-tooltip>
        </template>
      </div>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.recent-projects-card {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.panel-scrollbar {
  flex: 1;
}

.projects-list {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px;
}

.project-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.project-item:hover {
  background-color: var(--ep-fill-color-light);
}

.project-item:hover .project-remove {
  opacity: 1;
}

.project-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--ep-color-primary);
  font-size: 16px;
  flex-shrink: 0;
}

.project-name {
  flex: 1;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  min-width: 0;
}

.project-chip {
  color: var(--ep-text-color-regular);
  font-size: 13px;
  white-space: nowrap;
  opacity: 0.9;
}

.project-time {
  color: var(--ep-text-color-secondary);
  font-size: 12px;
  white-space: nowrap;
  opacity: 0.7;
}

.project-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  border-radius: 4px;
  color: var(--ep-text-color-placeholder);
  cursor: pointer;
  transition: all 0.2s ease;
  opacity: 0;
  font-size: 12px;
  flex-shrink: 0;
}

.project-remove:hover {
  background-color: var(--ep-color-danger-light-9);
  color: var(--ep-color-danger);
}
</style>
