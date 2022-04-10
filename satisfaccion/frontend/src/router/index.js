import Vue from 'vue'
import VueRouter from 'vue-router'

import Layout from '@/Layout.vue'
import CargasLayout from '@/cargas/Layout.vue'
import axios from 'axios'

Vue.use(VueRouter)

const routes = [

    {
        path: '/',
        component: Layout,
        // redirect: '/admin/catalogo',
        children: [
            { path: '/', name: 'Portada', component: () => import('@/views/Home.vue'), meta: { noAuth: true } },
            { path: '/login', name: 'Login', component: () => import('@/views/Login.vue'), meta: { noAuth: true } },
            { path: '/logindev', name: 'Login', component: () => import('@/views/LoginDev.vue'), meta: { noAuth: true } },
            { path: '/portal', name: 'Portal', component: () => import('@/views/Login.vue'), meta: { noAuth: true } },
            { path: '/logout', name: 'Login', component: () => import('@/views/Login.vue'), meta: { noAuth: true } },
            { path: '/callback', name: 'Callback', component: () => import('@/views/Callback.vue'), meta: { noAuth: true } },

            { path: '/resultados', name: 'Resultados', component: () => import('@/views/Resultados.vue'), meta: { noAuth: true } },

            { path: '/generales', name: 'Generales', component: () => import('@/generales/Indice.vue'), meta: { noAuth: true } },
            { path: '/comparar', name: 'Comparar', component: () => import('@/comparar/Indice.vue'), meta: { noAuth: true } },
            { path: '/detalleservicio/:id/:nombre', name: 'DetalleServicio', component: () => import('@/institucion/Indice.vue'), meta: { noAuth: true } },
            { path: '/metodologia', name: 'Metodologia', component: () => import('@/views/Metodologia.vue'), meta: { noAuth: true } },
            { path: '/resumen', name: 'Resumen', component: () => import('@/views/Resumen.vue'), meta: { noAuth: true } },

        ]
    },
    {
        path: '/cargas',
        component: CargasLayout,
        // redirect: '/admin/catalogo',
        children: [
            { path: '/', name: 'cargasListado', component: () => import('@/cargas/Listado.vue'), meta: { noAuth: true } }

        ]
    },

]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes,
    scrollBehavior: function (to, from, savedPosition) {
        if (to.hash) {
            return {
                selector: to.hash
            }
        } else {
            return { x: 0, y: 0 }
        }
    }
    // linkActiveClass: 'nav-link--active',
    // linkExactActiveClass: 'nav-link--active'
})

router.beforeEach(function (to, from, next) {
    if (to.fullPath === '/login?logout') {
        localStorage.removeItem('jwt.access')
        localStorage.removeItem('jwt.refresh')
        next({ path: '/login' })
        return
    }
    if (!to.meta.noAuth) {
        if (localStorage.getItem('jwt.access') === null) {
            next({ path: '/login', params: { nextUrl: to.fullPath } })
            return
        }
    }
    next()
})

axios.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('jwt.access')
        if (config.url.search('http') !== 0 && config.url.search('/api/') === 0) {
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
    const originalRequest = error.config

    if (error.response && error.response.status === 401 && error.response.data && error.response.data.detail === 'Authentication credentials were not provided.') {
        localStorage.removeItem('jwt.access')
        router.push('/login')
        return Promise.reject(error)
    }

    if (error.response.status === 401 && error.response.data && error.response.data.code === 'token_not_valid') {
        // si el url es el refresh, signifia que ya es el segundo request una vez que el primero no fue existos o por tanto debe devolver el error
        if (error.config.url.search('/api/token/refresh/') >= 0) {
            localStorage.removeItem('jwt.access')
            router.push('/login')
            return Promise.reject(error)
        }

        const refreshToken = localStorage.getItem('jwt.refresh')
        return axios.post(process.env.VUE_APP_BASEURL + '/api/token/refresh/', { refresh: refreshToken })
            .then(function (res) {
                if (res.status === 200) {
                    localStorage.setItem('jwt.access', res.data.access)
                    return axios(originalRequest)
                }
            }).catch(function () {
                localStorage.removeItem('jwt.access')
                localStorage.removeItem('jwt.refresh')

                router.push({
                    name: 'login',
                    query: {
                        t: new Date().getTime()
                    }
                })
            })
    }

    return Promise.reject(error)

    // if (error.response.status === 401 && originalRequest.url === 'http://13.232.130.60:8081/v1/auth/token) {
    //   router.push('/login')
    //   return Promise.reject(error)
    // }
})

export default router
