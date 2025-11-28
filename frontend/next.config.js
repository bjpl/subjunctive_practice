/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  poweredByHeader: false,

  // Ignore ESLint warnings during production builds
  eslint: {
    ignoreDuringBuilds: true,
  },

  // Ignore TypeScript errors during production builds (temporary for legacy code)
  typescript: {
    ignoreBuildErrors: true,
  },

  // API configuration
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: process.env.NEXT_PUBLIC_API_URL + '/:path*',
      },
    ];
  },

  // Image configuration
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**',
      },
    ],
  },

  // Environment variables
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
};

module.exports = nextConfig;
