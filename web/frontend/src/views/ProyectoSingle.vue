<template>
    <div>
        <section class="proyecto-single">
            <div class="container" v-if="proyecto">
                <div class="row">
                    <div class="col">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
                                <li class="breadcrumb-item"><router-link to="/proyectos">Proyectos</router-link></li>
                                <li class="breadcrumb-item active" aria-current="page">{{proyecto.titulo}}</li>
                            </ol>
                        </nav>
                        <!-- <span class="proyecto-single__category" :class="getBgClass(proyecto.categoria)" v-if="proyecto.categoria">{{proyecto.categoria | uppercase}}</span> -->
                    </div>
                </div>
                <div class="proyecto-single__content">
                    <div class="row align-items-center justify-content-between">
                        <div class="col-md-7">
                            <h3 class="proyecto-single__title">{{proyecto.titulo}}</h3>
                            <div v-if="proyecto.estado">
                                <h3 class="proyecto-single__subtitle">Estado</h3>
                                <p>{{proyecto.estado}}</p>
                            </div>
                            <div v-if="proyecto.instituciones_asociadas">
                                <h3 class="proyecto-single__subtitle">Instituciones Asociadas</h3>
                                <p>{{proyecto.instituciones_asociadas}}</p>
                            </div>
                            <div v-if="proyecto.descripcion_larga">
                                <h3 class="proyecto-single__subtitle">Descripción</h3>
                                <div v-html="proyecto.descripcion_larga" class="proyecto-single__descripcion"></div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <img :src="proyecto.cover" class="proyecto-single__img">
                        </div>
                    </div>
                    <!-- <div class="row align-items-center justify-content-between" v-if="proyecto.descripcion_larga">
                        <div class="col-md-7">
                            <h3 class="proyecto-single__subtitle">Descripción</h3>
                            <div v-html="proyecto.descripcion_larga" class="proyecto-single__descripcion"></div>
                        </div>
                        <div class="col-md-4">
                            <img :src="proyecto.cover" class="proyecto-single__img">
                        </div>
                    </div> -->
                    <div class="row" v-if="proyecto.logros && proyecto.logros.length">
                        <div class="col">
                            <div class="logros">
                                <div class="row align-items-center">
                                    <div class="col-md-auto">
                                        <img src="/img/icon_logros.svg" class="logros__img">
                                    </div>
                                    <div class="col">
                                        <h3 class="logros__title">Logros</h3>
                                        <ul class="logros__list">
                                            <li class="logros__item" v-for="logro in proyecto.logros" v-bind:key="logro" v-html="logro"></li>
                                        </ul>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row" v-if="proyecto.contacto">
                        <div class="col-md-12">
                            <h3 class="proyecto-single__subtitle">Contacto</h3>
                            <p v-html="proyecto.contacto"></p>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'ProyectoSingle',
    components: {
    },
    data () {
        return {
            proyecto: [],
            categorias: [],
            params: ''
        }
    },
    mounted () {
        var self = this
        var proyectos = []
        self.params = Number(self.$route.query.proyecto)
        var todo = []
        axios
            .get('./json/categorias_proyecto.json')
            .then(response => {
                response.data.data.categorias.filter(function (item) {
                    if (item.proyecto) {
                        todo.push(item)
                    }
                })
                self.categorias = todo
            })
            .catch(error => console.log(error))
        axios
            .get('./json/proyectos.json')
            .then(response => {
                response.data.data.proyectos.filter(function (item) {
                    if (item.id === self.params) {
                        proyectos.push(item)
                    }
                })
                self.proyecto = proyectos[0]
            })
            .catch(error => console.log(error))
    },
    methods: {
        getBgClass: function (category) {
            var item = this.categorias.find(item => item.nombre === category)
            return item.bg_class
        }
    }
}
</script>
