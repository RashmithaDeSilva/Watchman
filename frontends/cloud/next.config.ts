import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*", // Any request to /api/... will be redirected
        destination: "http://127.0.0.1:5001/api/v1/:path*", // Your Flask backend
      },
    ];
  },
};

export default nextConfig;
