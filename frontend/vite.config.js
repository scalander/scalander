import { sveltekit } from '@sveltejs/kit/vite';

const config = {
  plugins: [sveltekit()],
  server: {
    host: "0.0.0.0",
    port: 8080,
  },
  optimizeDeps: { exclude: ['layercake'] }
};

export default config;
