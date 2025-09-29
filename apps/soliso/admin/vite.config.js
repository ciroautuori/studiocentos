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
      applyBase: true,
      applyComponents: true,
      applyUtilities: true,
      darkMode: 'class',
      content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
      theme: {
        extend: {
          colors: {
            primary: '#1DA1F2',
            secondary: '#14171A',
          },
        },
      },
    }),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
})
