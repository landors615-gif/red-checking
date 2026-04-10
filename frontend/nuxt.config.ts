export default defineNuxtConfig({
  devtools: { enabled: false },
  compatibilityDate: '2024-11-01',
  app: {
    baseURL: '/red-checking/',
    buildAssetsDir: '/_nuxt/',
    head: {
      title: 'Red Checking - 小红书账号/内容 AI 检测',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no' },
        { name: 'description', content: '输入一个小红书链接，快速生成专业分析报告' },
      ],
      link: [
        { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
        { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
        {
          rel: 'stylesheet',
          href: 'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
        },
      ],
    },
  },
  css: ['~/assets/css/main.css'],
  runtimeConfig: {
    public: {
      // Backend API — override via NUXT_PUBLIC_API_BASE env var
      // For production: set to your deployed backend URL
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000',
    },
  },
  // Generate static site for GitHub Pages
  nitro: {
    preset: 'static',
  },
  // SPA fallback for GitHub Pages (all routes serve index.html)
  routeRules: {
    '/**': { ssr: false },
  },
})
