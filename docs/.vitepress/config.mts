import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'lavoix',
  description: 'Speech infrastructure library and service documentation',
  lastUpdated: true,
  cleanUrls: true,
  markdown: {
    codeTransformers: []
  },
  themeConfig: {
    search: {
      provider: 'local'
    },
    outline: {
      level: [2, 3],
      label: 'On this page'
    },
    editLink: {
      pattern: 'https://github.com/Unchained-Labs/lavoix/edit/main/docs/:path',
      text: 'Edit this page on GitHub'
    },
    docFooter: {
      prev: 'Previous',
      next: 'Next'
    },
    footer: {
      message: 'lavoix docs',
      copyright: 'Unchained Labs'
    },
    nav: [
      { text: 'Home', link: '/' },
      { text: 'Getting Started', link: '/tutorials/getting-started' },
      { text: 'Architecture', link: '/architecture' },
      { text: 'Concepts', link: '/concepts' },
      { text: 'API', link: '/api/index' },
      { text: 'Tutorials', link: '/tutorials/getting-started' },
      { text: 'References', link: '/related-documents' }
    ],
    sidebar: [
      {
        text: 'Overview',
        collapsed: false,
        items: [
          { text: 'Product Landing', link: '/' },
          { text: 'Architecture', link: '/architecture' },
          { text: 'Concepts', link: '/concepts' }
        ]
      },
      {
        text: 'Tutorials',
        collapsed: false,
        items: [
          { text: 'Getting Started', link: '/tutorials/getting-started' },
          { text: 'Building a Provider', link: '/tutorials/building-a-provider' }
        ]
      },
      {
        text: 'API Documentation',
        collapsed: false,
        items: [
          { text: 'API Overview', link: '/api/index' },
          { text: 'REST API', link: '/api/rest-api' },
          { text: 'Library API', link: '/api/library-api' }
        ]
      },
      {
        text: 'References',
        collapsed: false,
        items: [{ text: 'Related Documents', link: '/related-documents' }]
      }
    ],
    socialLinks: [{ icon: 'github', link: 'https://github.com/Unchained-Labs/lavoix' }]
  }
})
