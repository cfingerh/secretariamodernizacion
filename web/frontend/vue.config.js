const CompressionPlugin = require('compression-webpack-plugin')

module.exports = {
  chainWebpack (config) {
    config.plugins.delete('prefetch')

    // and this line
    config.plugin('CompressionPlugin').use(CompressionPlugin)
  },

  configureWebpack: {
    optimization: {
      splitChunks: {
        minSize: 100000,
        maxSize: 500000
      }
    }
  }
}
