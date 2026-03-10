import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: '0.0.0.0',
    port: 5000,
    strictPort: true,
    allowedHosts: ['.replit.dev', '.repl.co', '.picard.replit.dev'],
    hmr: {
      clientPort: 443,
    },
    watch: {
      ignored: ['**/node_modules/**', '**/.cache/**', '**/data/**', '**/frontend/**', '**/__pycache__/**', '**/app/**'],
    },
    proxy: {
      '/api': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
      '/health': {
        target: 'http://localhost:8001',
        changeOrigin: true,
      },
    },
  },
})
