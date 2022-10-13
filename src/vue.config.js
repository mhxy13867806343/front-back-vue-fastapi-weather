// vue.configs.js
const ScriptSetup = require('unplugin-vue2-script-setup/webpack').default

module.exports = {
  transpileDependencies: ['@sadais/piui-tool', 'sadais-piui'],
  parallel: false,  // disable thread-loader, which is not compactible with this plugin
  configureWebpack: {
    plugins: [
      ScriptSetup({ /* options */ }),
    ],
  },
}
