<template>
    <div>
        <section class="proyecto-single">
            <div class="container" v-if="proceso">
                <div class="row">
                    <div class="col">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
                                <li class="breadcrumb-item"><router-link to="/procesos">Procesos</router-link></li>
                                <li class="breadcrumb-item active" aria-current="page">{{proceso.titulo}}</li>
                            </ol>
                        </nav>
                        <!-- <span class="proyecto-single__category" v-if="proceso.categoria" :class="getBgClass(proceso.categoria)">{{proceso.categoria | uppercase}}</span> -->
                    </div>
                </div>
                <div class="proyecto-single__content">
                    <div class="row align-items-center">
                        <div class="col-md-7">
                            <h3 class="proyecto-single__title">{{proceso.titulo}}</h3>
                            <div v-html="proceso.descripcion_larga" class="proyecto-single__descripcion"></div>
                        </div>
                        <div class="col-md-5">
                            <img :src="proceso.cover" class="proyecto-single__img">
                        </div>
                    </div>
                </div>
<!--                 <div class="row" v-if="proceso.logros.length > 0">
                    <div class="col">
                        <div class="logros">
                            <div class="row align-items-center">
                                <div class="col-md-auto">
                                    <img src="/img/icon_logros.png" class="logros__img">
                                </div>
                                <div class="col">
                                    <h3 class="logros__title">Logros</h3>
                                    <ul class="logros__list">
                                        <li class="logros__item" v-for="logro in proceso.logros" v-bind:key="logro" v-html="logro"></li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                    </div>
                </div> -->
            </div>
        </section>
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'ProcesoSingle',
    components: {
    },
    data () {
        return {
            proceso: [],
            categorias: [],
            params: ''
        }
    },
    mounted () {
        var self = this
        var procesos = []
        self.params = Number(self.$route.query.proceso)
        var todo = []
        axios
            .get('./json/categorias_proyecto.json')
            .then(response => {
                response.data.data.categorias.filter(function (item) {
                    if (item.proceso) {
                        todo.push(item)
                    }
                })
                self.categorias = todo
            })
            .catch(error => console.log(error))
        axios
            .get('./json/procesos.json')
            .then(response => {
                response.data.data.procesos.filter(function (item) {
                    if (item.id === self.params) {
                        procesos.push(item)
                    }
                })
                self.proceso = procesos[0]
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
