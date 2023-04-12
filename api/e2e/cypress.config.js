const { defineConfig } = require('cypress')

module.exports = defineConfig({
    e2e: {
        baseUrl: 'http://0.0.0.0:8000',
        supportFile: false,
        setupNodeEvents(on, config) {
            on('task', {
                log(message) {
                    console.log(message)
                    return null
                },
                table(message) {
                    console.table(message)
                    return null
                }
            })
        },
    }
})