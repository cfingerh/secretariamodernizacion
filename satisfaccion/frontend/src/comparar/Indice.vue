<template>
    <div>
        <section >
            <div class="container">
                <div class="row">
                    <div class="col-md-2">
                        <img src="/img/pc.png" width="150px">
                    </div>
                    <div class="col-md-10">
                        <img src="/img/gob-line.svg" class="mb-4">
                        <div class="titulo">
                            <h1>Comparar</h1>
                            En esta sección podrás conocer los cruces y contrastes más recurrentes en el análisis del estudio de Satisfacción, comparando una institución contra el promedio de todas las instituciones.
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-3" >
                         <label style="float:right">Selecciona una institución</label>
                    </div>
                    <div class="col-md-3">
                        <select v-model="form.version__encuesta_1" class="form-select">
                            <option v-for='encuesta in encuestas' v-bind:key="encuesta.id" :value="encuesta.id">{{encuesta.nombre}}</option>
                        </select>
                    </div>
                </div>
            </div>
        </section>
        <section>
            <div class="container">
                <img src="/img/gob-line.svg" class="mb-4">
                <div class="titulo">
                    <h1>Dirección del Trabajo</h1>
                </div>
            </div>
        </section>
        <section class="bg-light">
            <div class="container">
                <div class="box-ficha card">
                    <evaluacion-tramite></evaluacion-tramite>
                </div>
            </div>
        </section>

    </div>
</template>

<script>

import axios from 'axios'
import EvaluacionTramite from './EvaluacionTramite.vue'

export default {
    name: 'Home',
    components: { EvaluacionTramite },
    data () {
        return {
            encuesta: null,
            encuestas: null,
            form: {
                dimension1: null
            }
        }
    },
    mounted () {
        this.url = process.env.VUE_APP_BASEURL_OLD
        axios.get(this.url + '/api/encuestas').then(res => { this.encuestas = res.data })
    },

    computed: {
    },

    methods: {

    }
}
</script>
