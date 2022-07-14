import Vue from 'vue'
import App from './App'
import router from './router'
import 'bootstrap'

import 'bootstrap/dist/css/bootstrap.min.css'
// import 'bootstrap/dist/css/bootstrap.css'
import './custom.scss'
// import './app.css'
import '@trevoreyre/autocomplete-vue/dist/style.css'

import VueCarousel from 'vue-carousel'
import Multiselect from 'vue-multiselect'
import axios from 'axios'

import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import {
    faHome, faCaretUp, faCaretDown, faInfoCircle, faCircle, faSearch, faAdjust, faChevronRight, faChevronDown, faPlus, faBars, faEnvelope, faFilePdf, faFileWord, faFileImage, faChartBar, faComments
} from '@fortawesome/free-solid-svg-icons'

import { faSmile, faFrown } from '@fortawesome/free-regular-svg-icons'

import { faLinkedin } from '@fortawesome/free-brands-svg-icons'
// import Vuex from 'vuex'

// window.$ = window.jQuery = require('jquery')

// Vue.use(BootstrapVue)
Vue.use(VueCarousel)
Vue.component('multiselect', Multiselect)
// Vue.use(Vuex)

Vue.filter('formatDateTime', function (value) {
    if (value) {
        console.log(value)
        return new Date(value).toLocaleDateString(
            'es-cl',
            {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric'
            }
        )

        // moment(String(value)).format('DD MMM YYYY HH:mm:ss')
    }
})

Vue.component('font-awesome-icon', FontAwesomeIcon)
library.add(
    faHome, faLinkedin, faCaretUp, faCaretDown, faSmile, faFrown, faInfoCircle, faCircle, faSearch, faAdjust, faChevronRight, faChevronDown, faPlus, faBars, faEnvelope, faFilePdf, faFileWord, faFileImage, faChartBar, faComments
)
Vue.config.productionTip = false

function getJWTExpireDate (jwtToken) {
    if (jwtToken) {
        try {
            const [, payload] = jwtToken.split('.')
            const { exp: expires } = JSON.parse(window.atob(payload))
            if (typeof expires === 'number') {
                return new Date(expires * 1000)
            }
        } catch {
        }
    }
    return null
}

axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('jwt.access')

        if (config.url.search('/api/token/refresh/') < 0) {
            if ((getJWTExpireDate(token) - (new Date())) / 1000 < 50) {
                const refreshToken = localStorage.getItem('jwt.refresh')
                if (!refreshToken) {
                    localStorage.removeItem('jwt.access')
                    localStorage.removeItem('jwt.refresh')
                }

                if (refreshToken && refreshToken !== '') {
                    axios.post(process.env.VUE_APP_BASEURL + '/api/token/refresh/', { refresh: refreshToken })
                        .then(function (res) {
                            if (res.status === 200) {
                                localStorage.setItem('jwt.access', res.data.access)
                            }
                        }).catch(function () {
                            localStorage.removeItem('jwt.access')
                            localStorage.removeItem('jwt.refresh')
                            this.$router.push({ name: 'Login', query: { t: new Date().getTime() } })
                        })
                }
            }
        }

        if (config.url.search('http') !== 0) {
            config.url = process.env.VUE_APP_BASEURL + config.url
        }
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config
    },

    (error) => {
        return Promise.reject(error)
    }
)

axios.interceptors.response.use((response) => {
    return response
}, function (error) {
    if (error.response && error.response.status === 401 &&
        error.response.data &&
        (error.response.data.code === 'token_not_valid' || error.response.data.detail === 'Authentication credentials were not provided.')
    ) {
        localStorage.removeItem('jwt.access')
        router.push('/public/login')
        return Promise.reject(error)
    }
    return Promise.reject(error)

    // if (error.response.status === 401 && originalRequest.url === 'http://13.232.130.60:8081/v1/auth/token) {
    //   router.push('/login')
    //   return Promise.reject(error)
    // }
})

new Vue({
    router,
    // store: store,
    render: h => h(App)
}).$mount('#app')
