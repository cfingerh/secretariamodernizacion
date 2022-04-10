<template>
    <header class="fixed-top">
    <div class="bg-light pt-2 pb-2">
        <div class="container">
            <div class="row">
                <div class="col-12 col-lg-4 ">
                    <a class="navbar-brand" href="/">
                        <img src="/img/logos/logo_hacienda.png" class="navbar__img--hacienda">
                        <img src="/img/logo.svg" class="navbar__img--secretaria">
                    </a>
                </div>
                <div class="col-12 col-lg-8 ">
                    <h1 class="header__title">Satisfacción de Usuarios</h1>
                    <h4 class="header__bajada">Mejores servicios del Estado para las personas</h4>
                </div>
            </div>
        </div>
    </div>
    <nav class="navbar navbar-expand-md bg-dark">
        <div class="container">
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarCollapse" aria-controls="navbarCollapse" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon">
            <font-awesome-icon :icon="['fa', 'bars']" :style="{ color: 'white' }"/>

            </span>
        </button>
        <div class="collapse navbar-collapse" id="navbarCollapse">
            <ul class="navbar-nav me-auto mb-2 mb-md-0">
                <li class="nav-item">
                    <a class="nav-link" v-bind:class="{ active: $route.name==='Portada' }" aria-current="page" href="/cargas">Carga datos</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" v-bind:class="{ active: $route.name==='Portada' }" aria-current="page" href="/logout">Salir</a>
                </li>
            </ul>
        </div>
        </div>
    </nav>
    </header>
</template>
<script>

import axios from 'axios'

export default {
    name: 'Header',
    mixins: [],
    data () {
        return {
        }
    },
    computed: {},
    methods: {
        getUser () {
            axios.get('/usuarios/info').then(res => {
                this.$store.commit('putUser', res.data)
                this.user = res.data
            })
        }
    },
    mounted () {
        this.getUser()
    }
}
</script>
