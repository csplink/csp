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
      { text: '功能介绍', link: '/features' },
    ],
    sidebar: {
      '/': [
        { text: '介绍', link: '/' },
        { text: '环境搭建', link: '/installation' },
        { text: '功能介绍', link: '/features' },
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
