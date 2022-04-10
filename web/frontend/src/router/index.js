/* eslint-disable */
import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import Nosotros from '../views/Nosotros.vue'
import Proyectos from '../views/Proyectos.vue'
import ProyectoSingle from '../views/ProyectoSingle.vue'
import Procesos from '../views/Procesos.vue'
import ProcesoSingle from '../views/ProcesoSingle.vue'
import Documentos from '../views/Documentos.vue'
import DocumentosCategory from '../views/DocumentosCategory.vue'
import DocumentoSingle from '../views/DocumentoSingle.vue'
import Resultados from '../views/Resultados.vue'
// import Destacados from '../views/Destacados.vue'
// import DestacadoSingle from '../views/DestacadoSingle.vue'
Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/nosotros',
    name: 'Nosotros',
    component: Nosotros
  },
  {
    path: '/proyectos',
    name: 'Proyectos',
    component: Proyectos
  },
  {
    path: '/proyecto-single',
    name: 'ProyectoSingle',
    component: ProyectoSingle
  },
  {
    path: '/procesos',
    name: 'Procesos',
    component: Procesos
  },
  {
    path: '/proceso-single',
    name: 'ProcesoSingle',
    component: ProcesoSingle
  },
  {
    path: '/documentos',
    name: 'Documentos',
    component: Documentos
  },
  {
    path: '/documentos-category',
    name: 'DocumentosCategory',
    component: DocumentosCategory
  },
  {
    path: '/resultados',
    name: 'Resultados',
    component: Resultados
  },
  {
    path: '/documento-single',
    name: 'DocumentoSingle',
    component: DocumentoSingle
  }
  // {
  //   path: '/destacados',
  //   name: 'Destacados',
  //   component: Destacados
  // },
  // {
  //   path: '/destacado-single',
  //   name: 'DestacadoSingle',
  //   component: DestacadoSingle
  // }
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
  },
  // linkActiveClass: 'nav-link--active',
  // linkExactActiveClass: 'nav-link--active'
})

export default router
