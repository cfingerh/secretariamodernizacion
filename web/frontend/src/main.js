import Vue from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap'
import { BootstrapVue } from 'bootstrap-vue'
import vuejquery from 'vue-jquery'
import moment from 'moment'
import VueAnalytics from 'vue-analytics'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faHome, faBars, faSearch, faAngleDown, faAngleUp, faDownload } from '@fortawesome/free-solid-svg-icons'
import { faLinkedin, faTwitter } from '@fortawesome/free-brands-svg-icons'

import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
// import '../src/assets/css/style.css'
import './app.css'

window.$ = window.jQuery = require('jquery')
Vue.component('font-awesome-icon', FontAwesomeIcon)

Vue.use(vuejquery)
Vue.use(BootstrapVue)
Vue.use(VueAnalytics, {
    id: 'UA-158836531-1',
    router
})

Vue.config.productionTip = false

library.add(faHome, faBars, faLinkedin, faTwitter, faSearch, faDownload, faAngleDown, faAngleUp)

Vue.filter('dateFormat', function (value) {
    if (!value) return ''
    value = value.toString()
    return moment(value).format('DD/MM/YYYY')
})

Vue.filter('uppercase', function (value) {
    return value.toUpperCase()
})
new Vue({
    router,
    render: h => h(App)
}).$mount('#app')
