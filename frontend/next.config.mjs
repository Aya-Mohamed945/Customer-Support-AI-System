// frontend/next.config.mjs

/** @type {import('next').NextConfig} */

const nextConfig = {
  reactStrictMode: true,

  // Generate a minimal standalone production bundle
  output: 'standalone',

  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
