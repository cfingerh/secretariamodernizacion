<template>
<div>
    <section>
        <div class="container">
            <div class="row">
                <div class="col-md-12">
                    <!-- <ol class="breadcrumb">
                        <li><a href="">Inicio </a></li>
                        <li>Resultados por institución</li>
                    </ol> -->
                    <img src="/img/gob-line.svg" class="mb-4">
                    <div class="titulo">
                        <h1>Instituciones participantes</h1>
                    </div>
                    <div class="row">
                        <div class="col-md-8" >

                            <autocomplete :search="search"  :get-result-value="getResultValue" autoselect="true" placeholder="Escribe la institución que quieres consultar">
                                <template #result="{ result, props }">
                                    <div v-bind="props" class="autocomplete-result">
                                    <a :href="`/detalleservicio/${result.codigo_dipres}/${result.codigo}`">{{ result.nombre }}

                                    </a>

                                    </div>
                                </template>
                            </autocomplete>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="container mt-5">
            <p>Mostrar por:</p>
            <ul class="nav nav-tabs mb-4">
                <li class="nav-item">
                    <a class="nav-link"  v-bind:class="{ 'active': vista==='porTipo' }" aria-current="page" href="#" @click="vista='porTipo'">Tipo de institución</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link"  v-bind:class="{ 'active': vista==='porOrden' }" href="#" @click="vista='porOrden'">Orden alfabético</a>
                </li>
            </ul>
        </div>
        <div class="container ">
            <div class="row" v-show="vista==='porTipo'" v-if="grupos">
                <div class="col-md-6">
                    <grupo-instituciones :grupos="grupos" grupo='Fiscalización'></grupo-instituciones>
                    <grupo-instituciones :grupos="grupos" grupo='Economía'></grupo-instituciones>
                    <grupo-instituciones :grupos="grupos" grupo='Ciudadanía /T. Generales'></grupo-instituciones>
                </div>
                <div class="col-md-6">
                    <grupo-instituciones :grupos="grupos" grupo='Salud/Previsión'></grupo-instituciones>
                    <grupo-instituciones :grupos="grupos" grupo='Social'></grupo-instituciones>
                </div>

            </div>
            <div class="row" v-show="vista==='porOrden'">
                <div class="col-md-6">
                    <div class="card card--link">
                        <div v-for="institucion in instituciones_mitad_1" v-bind:key="institucion.id" class="group-instituciones__item">
                            <a :href="`/detalleservicio/${institucion.codigo_dipres}/${institucion.codigo}`" >{{institucion.nombre}}</a><br>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card card--link">
                        <div v-for="institucion in instituciones_mitad_2" v-bind:key="institucion.id" class="group-instituciones__item">
                            <a :href="`/detalleservicio/${institucion.codigo_dipres}/${institucion.codigo}`" >{{institucion.nombre}}</a><br>
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
import GrupoInstituciones from '../components/GrupoInstituciones.vue'
import Autocomplete from '@trevoreyre/autocomplete-vue'
import _ from 'lodash'

export default {
    name: 'DetalleServicio',
    components: { GrupoInstituciones, Autocomplete },
    async beforeCreate () {},
    mixins: [],
    data () {
        return {
            form: { buscar: null },
            vista: 'porTipo',
            grupos: null,
            instituciones: [],
            isLoading: false,
            instituciones_mitad_1: [],
            instituciones_mitad_2: []
        }
    },
    methods: {
        getResultValue (result) {
            return result.nombre
        },
        handleSubmit (result) {
            window.open()
        },
        search (input) {
            var instituciones = []
            this.grupos.forEach(g => { g.instituciones.forEach(i => { if (i.nombre) { instituciones.push(i) } }) })

            if (input.length < 1) { return [] }
            return instituciones.filter(institucion => {
                return institucion.nombre.toLowerCase()
                    .search(input.toLowerCase()) >= 0
            })
        },
        asyncFind (query) {
            this.isLoading = true
            console.log(query)
            var instituciones = []
            this.grupos.forEach(g => { g.instituciones.forEach(i => { instituciones.push(i) }) })
            this.instituciones = instituciones
            this.isLoading = false
        },
    },
    mounted () {
        var instituciones = []
        axios.get('/api/instituciones/por_grupo').then(res => {
            this.grupos = res.data

            this.grupos.forEach(g => { g.instituciones.forEach(i => { if (i.nombre) { instituciones.push(i) } }) })
            instituciones = _.orderBy(instituciones, 'nombre')
            this.instituciones_mitad_1 = instituciones.slice(0, 24)
            this.instituciones_mitad_2 = instituciones.slice(24, 54)
        })
    }
}
</script>

<style scoped>
.wiki-result {
  border-top: 1px solid #eee;
  padding: 16px;
  background: transparent;
}

.wiki-title {
  font-size: 20px;
  margin-bottom: 8px;
}

.wiki-snippet {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.54);
}
</style>
