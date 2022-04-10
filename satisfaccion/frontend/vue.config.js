const CompressionPlugin = require('compression-webpack-plugin')

module.exports = {
    chainWebpack (config) {
        config.plugins.delete('prefetch')

        // and this line
        config.plugin('CompressionPlugin').use(CompressionPlugin)

        config
            .plugin('html')
            .tap(args => {
                args[0].title = 'Observatorio'
                return args
            })
    },
    // lintOnSave: false,

    configureWebpack: {
        devtool: 'source-map',
        optimization: {
            splitChunks: {
                minSize: 100000,
                maxSize: 500000
            }
        }
    }
}
