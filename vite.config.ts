/**
 * ****************************************************************************
 *  @author      xqyjlj
 *  @file        vite.config.ts
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
 *  2025-04-26     xqyjlj       initial version
 */

import fs from 'node:fs'
import path from 'node:path'
import vue from '@vitejs/plugin-vue'
import unocss from 'unocss/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import components from 'unplugin-vue-components/vite'
import vueRouter from 'unplugin-vue-router/vite'
import { defineConfig } from 'vite'
import electron from 'vite-plugin-electron/simple'
import { prismjsPlugin } from 'vite-plugin-prismjs'
import svgLoader from 'vite-svg-loader'

const optimizeDepsElementPlusIncludes = ['element-plus', 'element-plus/es']
const elementPlusComponents = fs.readdirSync('node_modules/element-plus/es/components')
elementPlusComponents.forEach((dirname) => {
  ['css', 'index'].forEach((name) => {
    const stylePath = `node_modules/element-plus/es/components/${dirname}/style/${name}.mjs`
    if (fs.existsSync(stylePath)) {
      optimizeDepsElementPlusIncludes.push(`element-plus/es/components/${dirname}/style/${name}`)
    }
  })
})

let electronArgs: string[] = []
const sepIndex = process.argv.indexOf('--')
if (sepIndex !== -1) {
  electronArgs = process.argv.slice(sepIndex + 1)
}

export default defineConfig({
  optimizeDeps: {
    include: optimizeDepsElementPlusIncludes,
  },
  resolve: {
    alias: {
      '~/': `${path.resolve(__dirname, 'src')}/`,
      '@/electron': `${path.resolve(__dirname, 'electron')}/`,
    },
  },
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: `@use "~/styles/themes/index.scss" as *;`,
        api: 'modern-compiler',
      },
    },
  },
  plugins: [
    vue(),
    vueRouter({
      extensions: ['.vue', '.md'],
      dts: 'src/typed-router.d.ts',
    }),
    electron({
      main: {
        entry: 'electron/main.ts',
        onstart(options) {
          options.startup(['.', '--no-sandbox', '--', ...electronArgs])
        },
      },
      preload: {
        input: path.join(__dirname, 'electron/preload.ts'),
      },
      renderer: process.env.NODE_ENV === 'test'
        ? undefined
        : {},
    }),
    components({
      extensions: ['vue', 'md'],
      include: [/\.vue$/, /\.vue\?vue/, /\.md$/],
      resolvers: [
        ElementPlusResolver({
          importStyle: 'sass',
        }),
      ],
      dts: 'src/components.d.ts',
    }),
    prismjsPlugin({
      languages: [
        'c',
        'cpp',
        'cmake',
        'python',
        'armasm',
        'linker-script',
        'json',
        'yaml',
        'xml',
        'markdown',
        'lua',
        'gitignore',
      ],
      plugins: ['line-numbers', 'inline-color', 'match-braces', 'diff-highlight'],
      theme: 'default',
      css: true,
    }),
    unocss(),
    svgLoader(),
  ],
})
