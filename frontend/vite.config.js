// frontend/vite.config.js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  // Rutas relativas para que el bundle funcione tras copiarse a app/static
  base: './',
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
})
