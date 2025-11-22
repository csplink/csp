<!--
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        index.vue
 *  @brief       Sponsor page for CSP project
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
 *  2025-11-22     xqyjlj       initial version
-->

<script setup lang="ts">
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const sponsorWays = computed(() => [
  {
    name: t('sponsor.alipay'),
    description: t('sponsor.alipayDescription'),
    src: './images/sponsor/alipay.png',
  },
  {
    name: t('sponsor.wechatPay'),
    description: t('sponsor.wechatPayDescription'),
    src: './images/sponsor/wechat.png',
  },
])

const projectGoals = computed(() => [
  {
    title: t('sponsor.featureImprovement'),
    description: t('sponsor.featureImprovementDesc'),
  },
  {
    title: t('sponsor.newFeatures'),
    description: t('sponsor.newFeaturesDesc'),
  },
  {
    title: t('sponsor.communityBuilding'),
    description: t('sponsor.communityBuildingDesc'),
  },
  {
    title: t('sponsor.internationalization'),
    description: t('sponsor.internationalizationDesc'),
  },
])
</script>

<template>
  <el-scrollbar class="sponsor-scrollbar">
    <div class="sponsor-container">
      <div class="header-section">
        <h1 class="page-title">
          {{ t('sponsor.pageTitle') }}
        </h1>
        <p class="page-subtitle">
          {{ t('sponsor.pageSubtitle') }}
        </p>
      </div>

      <!-- 项目介绍 -->
      <el-card class="intro-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>{{ t('sponsor.aboutProject') }}</span>
          </div>
        </template>
        <div class="intro-content">
          <p>
            {{ t('sponsor.projectIntro1') }}
          </p>
          <p>
            {{ t('sponsor.projectIntro2') }}
          </p>
        </div>
      </el-card>

      <div class="section">
        <h2 class="section-title">
          {{ t('sponsor.sponsorWays') }}
        </h2>
        <el-row :gutter="20" justify="center">
          <el-col
            v-for="(way, index) in sponsorWays"
            :key="index"
            :xs="24"
            :sm="12"
          >
            <el-card class="sponsor-way-card" shadow="hover">
              <div class="qr-code-container">
                <el-image :src="way.src" :alt="way.name" class="qr-code" />
              </div>
              <h3>{{ way.name }}</h3>
              <p>{{ way.description }}</p>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 项目目标 -->
      <div class="section">
        <h2 class="section-title">
          {{ t('sponsor.fundUsage') }}
        </h2>
        <div class="goals-grid">
          <el-card
            v-for="(goal, index) in projectGoals"
            :key="index"
            class="goal-card"
            shadow="never"
          >
            <h4>{{ goal.title }}</h4>
            <p>{{ goal.description }}</p>
          </el-card>
        </div>
      </div>

      <!-- 感谢信息 -->
      <el-card class="thanks-card" shadow="never">
        <template #header>
          <div class="card-header">
            <span>{{ t('sponsor.specialThanks') }}</span>
          </div>
        </template>
        <div class="thanks-content">
          <p>
            {{ t('sponsor.thanksMessage') }}
          </p>
        </div>
        <el-divider />
        <SponsorsList />
      </el-card>
    </div>
  </el-scrollbar>
</template>

<style scoped>
.sponsor-scrollbar {
  flex: 1;
}

.sponsor-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.header-section {
  text-align: center;
  padding: 40px 0;
}

.page-title {
  font-size: 36px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0 0 16px 0;
}

.page-subtitle {
  font-size: 16px;
  color: #7f8c8d;
  line-height: 1.6;
  max-width: 800px;
  margin: 0 auto;
}

.intro-card,
.thanks-card {
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.intro-card :deep(.ep-card__header),
.thanks-card :deep(.ep-card__header) {
  background: rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 18px;
}

.intro-content,
.thanks-content {
  line-height: 1.8;
}

.intro-content p,
.thanks-content p {
  margin-bottom: 12px;
}

.highlight {
  background: rgba(255, 255, 255, 0.2);
  padding: 12px;
  border-radius: 8px;
  font-weight: 500;
}

.highlight a {
  color: #ffe66d;
  text-decoration: none;
}

.highlight a:hover {
  text-decoration: underline;
}

/* 章节样式 */
.section {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: #2c3e50;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 赞助方式卡片 */
.sponsor-way-card {
  text-align: center;
  height: 100%;
  transition: all 0.3s ease;
}

.sponsor-way-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.qr-code-container {
  margin-bottom: 16px;
  padding: 16px;
  background: #fff;
  border-radius: 8px;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.qr-code {
  max-width: 180px;
  max-height: 180px;
  width: 100%;
  height: auto;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: transform 0.3s ease;
}

.qr-code:hover {
  transform: scale(1.05);
}

.sponsor-way-card h3 {
  margin: 0 0 12px 0;
  font-size: 18px;
  color: #2c3e50;
  font-weight: 600;
}

.sponsor-way-card p {
  color: #7f8c8d;
  margin-bottom: 16px;
}

/* 项目目标网格 */
.goals-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.goal-card {
  background: #f8f9fa;
  border-left: 4px solid #3498db;
}

.goal-card h4 {
  margin: 0 0 8px 0;
  color: #2c3e50;
  font-size: 16px;
  font-weight: 600;
}

.goal-card p {
  margin: 0;
  color: #7f8c8d;
  line-height: 1.6;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .sponsor-container {
    padding: 16px;
  }

  .page-title {
    font-size: 28px;
  }

  .section-title {
    font-size: 24px;
  }

  .goals-grid {
    grid-template-columns: 1fr;
  }
}
</style>
