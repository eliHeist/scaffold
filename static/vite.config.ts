import { defineConfig } from 'vite'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
    plugins: [
        tailwindcss(),
    ],
    server: {
        watch: {
            ignored: ['!../../**/*'], // Ensure Vite watches parent folder
        }
    },
    build: {
        outDir: 'dist', // Output directory
        sourcemap: true,
        rollupOptions: {
            output: {
                entryFileNames: '[name].js',
                chunkFileNames: '[name].js',
                assetFileNames: '[name][extname]'
            }
        }
    }
})