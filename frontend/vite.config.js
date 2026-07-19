import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'node:path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    // The landing page source lives outside this package. Pin its bare imports to
    // the frontend installation so monorepo builds only need `npm ci` here.
    alias: [
      { find: /^react$/, replacement: resolve(__dirname, 'node_modules/react') },
      { find: /^react-dom$/, replacement: resolve(__dirname, 'node_modules/react-dom') },
      { find: /^react-dom\/client$/, replacement: resolve(__dirname, 'node_modules/react-dom/client') },
      { find: /^lucide-react$/, replacement: resolve(__dirname, 'node_modules/lucide-react') },
    ],
  },
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
