/** @type {import('next').NextConfig} */

function apiImagePattern() {
  const raw = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000/api";
  try {
    const u = new URL(raw);
    return {
      protocol: u.protocol.replace(":", ""),
      hostname: u.hostname,
      ...(u.port ? { port: u.port } : {}),
      pathname: "/media/**",
    };
  } catch {
    return { protocol: "http", hostname: "127.0.0.1", port: "8000", pathname: "/media/**" };
  }
}

const nextConfig = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: [
          { key: "X-Content-Type-Options", value: "nosniff" },
          { key: "X-Frame-Options", value: "DENY" },
          { key: "Referrer-Policy", value: "strict-origin-when-cross-origin" },
          { key: "Permissions-Policy", value: "camera=(), microphone=(), geolocation=()" },
        ],
      },
    ];
  },
  images: {
    remotePatterns: [apiImagePattern()],
    dangerouslyAllowLocalIP: process.env.NODE_ENV !== "production",
  },
};

module.exports = nextConfig;
