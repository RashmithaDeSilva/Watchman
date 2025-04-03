import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: "/api/:path*", // Any request to /api/... will be redirected
        destination: "http://localhost:5001/:path*", // Your Flask backend
      },
    ];
  },
};

export default nextConfig;
