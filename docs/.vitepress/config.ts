import { defineConfig } from 'vitepress'

// https://vitepress.dev/reference/site-config
export default defineConfig({
  title: 'CSP 文档',
  description: '芯片灵活配置工具',
  base: '/',
  themeConfig: {
    logo: '/images/logo.svg',
    nav: [
      { text: '首页', link: '/' },
      { text: '环境搭建', link: '/installation' },
      { text: '软件包', link: '/packages' },
    ],
    sidebar: {
      '/': [
        { text: '介绍', link: '/' },
        { text: '环境搭建', link: '/installation' },
        {
          text: '软件包',
          items: [
            { text: '软件包总览', link: '/packages/' },
            { text: '工具链', link: '/packages/toolchains' },
            { text: 'HAL库', link: '/packages/hal' },
          ],
        },
      ],
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/csplink/csp' },
    ],
    search: {
      provider: 'local',
    },
  },
})
