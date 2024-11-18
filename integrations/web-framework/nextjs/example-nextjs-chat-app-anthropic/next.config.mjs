import { ModuleAlias } from '@langtrase/typescript-sdk/dist/webpack/plugins/ModuleAlias.js'
const nextConfig = {
  webpack: (config, { isServer }) => {
    if (isServer) {
        config.resolve.plugins = [
        ...(config.resolve.plugins || []),
        new ModuleAlias(process.cwd())
      ];
      config.module.rules.push({
        loader: "node-loader",
        test: /\.node$/,
      });
      config.ignoreWarnings = [{ module: /opentelemetry/ }];
    }
  return config;
  },
};


export default nextConfig;
