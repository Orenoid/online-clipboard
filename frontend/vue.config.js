module.exports = {
    configureWebpack: config => {
        config.externals = {
            'vue': 'Vue'
        }
    }
}