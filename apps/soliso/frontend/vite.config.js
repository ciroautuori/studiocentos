import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    tailwindcss({
      apply: true,
      config: {
        content: [
          './index.html',
          './src/**/*.{vue,js,ts,jsx,tsx}',
        ],
        theme: {
          extend: {
            colors: {
              'red': {
                DEFAULT: '#c9000a',
              },
              'blue': {
                DEFAULT: '#005490',
              },
              'orange': {
                DEFAULT: '#ff6b00',
              },
            },
            boxShadow: {
              'card': '0 10px 25px rgba(0, 0, 0, 0.1)',
            },
          },
        },
        plugins: [],
      },
    }),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
})
