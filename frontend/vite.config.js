import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'node:path'

export default defineConfig({
  plugins: [react()],
  build: {
    rollupOptions: {
      input: {
        app: resolve(__dirname, 'index.html'),
        landing: resolve(__dirname, 'landing.html'),
      },
    },
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': { target: 'http://localhost:8100', changeOrigin: true },
      '/health': { target: 'http://localhost:8100', changeOrigin: true },
    },
  },
})
