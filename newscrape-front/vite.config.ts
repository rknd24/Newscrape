import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // Newscrape 専用ポート。他アプリと取り合わないよう固定。
    // strictPort: 埋まっていたら別ポートに逃げず、エラーで気づけるようにする
    port: 5180,
    strictPort: true,
    proxy: {
      '/news': 'http://localhost:8000',
      '/analyze': 'http://localhost:8000',
      '/chat': 'http://localhost:8000',
    },
  },
})
