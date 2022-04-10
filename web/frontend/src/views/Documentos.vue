<template>
    <div>
        <section>
            <div class="container">
                <div class="row align-items-center justify-content-between mb-3">
                    <div class="col">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
                                <li class="breadcrumb-item active" aria-current="page">Documentos</li>
                            </ol>
                        </nav>
                    </div>
                    <div class="col-md-4 align-self-center">
                        <div class="input-group input-group--search" v-on:keyup.enter="search()">
                            <input class="form-control" type="text" placeholder="Buscar Documento" aria-label="Buscar Documento" v-model="busqueda">
                            <div class="input-group-append">
                                <span class="input-group-text">
                                    <a @click="search()"><font-awesome-icon :icon="['fas', 'search']" /></a>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col mb-3">
                        <p>La Secretaría de Modernización del Estado realiza estudios en diversas materias de gestión pública y modernización del Estado. Los estudios se dividen en dos grandes áreas: los que se orientan a diagnosticar la situación actual de las instituciones públicas y formular proyectos de modernización en conjunto con dichas instituciones; y aquellos orientados a proponer mejoras transversales en la gestión pública y/o la formulación, implementación y evaluación de políticas públicas. En esta sección se presentan los estudios que lleva a cabo la Secretaría de Modernización del Estado y otros documentos de interés.</p>
                        <p>Los antecedentes de la medición de satisfacción usuaria se encuentran disponibles en el sitio <a href="https://www.satisfaccion.gob.cl/" target="_blank"> www.satisfaccion.gob.cl</a>.</p>
                    </div>
                </div>
            </div>
        </section>
        <section class="documentos__categorias">
            <div class="container">
                <div class="row justify-content-center">
                    <div class="col-lg-4 col-md-4 col-sm-6 mb-3" v-for="documento in documentos" v-bind:key="documento.id">
                        <div class="card card--proyecto h-100">
                            <img :src="documento.cover" class="card-img-top--proyecto" alt="">
                            <div class="card-body">
                                <h5 class="card-title card-title--documentos">{{documento.titulo}}</h5>
                                <!-- <p class="card-text" v-html="proyecto.descripcion_corta"></p> -->
                                <router-link :to="'/documentos-category?categoria=' + documento.id" class="proyecto__more">Revisar</router-link>
                            </div>
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
    name: 'Documentos',
    components: {
    },
    data () {
        return {
            documentos: [],
            busqueda: null
        }
    },
    mounted () {
        var self = this
        axios
            .get('./json/documentos_categorias.json')
            .then(response => (self.documentos = response.data.data.documentos))
            .catch(error => console.log(error))
    },
    methods: {
        search: function () {
            window.location.href = '/resultados?busqueda=' + this.busqueda
        }
    }
}
</script>
