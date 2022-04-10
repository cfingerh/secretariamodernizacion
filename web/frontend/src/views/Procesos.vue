<template>
    <div>
        <section class="proyectos">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
                                <li class="breadcrumb-item active" aria-current="page">Procesos</li>
                            </ol>
                        </nav>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <h3 class="proyectos__title">Procesos</h3>
                        <p class="proyectos__description">Conoce los proyectos en los que la Secretaría de Modernización del Estado ha o está trabajando, para la mejora de los servicios del Estado hacia los ciudadanos.</p>
                    </div>
                </div>
<!--                 <div class="row">
                    <div class="col">
                        <ul class="categorias__filters" v-if="categorias.length > 0">
                            <li class="categorias__filter-item" :class="setActiveClass(categoria)" v-for="categoria in categorias" v-bind:key="categoria.nombre" @click="switchCategory(categoria.nombre)">{{ categoria.nombre }}</li>
                        </ul>
                    </div>
                </div>
                <div class="row" v-if="procesos.length == 0">
                    No hay resultados
                </div> -->
                <div class="row">
                    <div class="col-lg-4 col-md-6 mb-4" v-for="proceso in procesos" v-bind:key="proceso.id">
                        <div class="card card--proceso h-100">
                            <img :src="proceso.cover" class="card-img-top--proyecto" alt="">
                            <div class="card-body">
                                <h5 class="card-title">{{proceso.titulo}}</h5>
                                <!-- <p class="card-text" v-html="proceso.descripcion_corta"></p> -->
                                <router-link :to="'/proceso-single?proceso=' + proceso.id" class="proyecto__more">Conoce más</router-link>
                                <!-- <span :class="getBorderClass(proceso.categoria)">{{proceso.categoria}}</span> <span>{{proceso.estado}}</span> -->
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
    name: 'Procesos',
    components: {
    },
    data () {
        return {
            procesos: [],
            categorias: [],
            categoria: []
        }
    },
    mounted () {
        this.getCategoria()
        this.getData()
        this.$watch('categoria', function () {
            this.getData()
        }, { deep: true })
    },
    methods: {
        getCategoria: function () {
            var self = this
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
        },
        getData: function () {
            var filtrado = []
            var self = this
            axios
                .get('./json/procesos.json')
                .then(response => {
                    self.procesos = response.data.data.procesos
                    if (self.categoria.length > 0) {
                        self.procesos.filter(function (item) {
                            if (self.categoria.includes(item.categoria)) {
                                filtrado.push(item)
                            }
                        })
                        self.procesos = filtrado
                    }
                })
                .catch(error => console.log(error))
        },
        getBorderClass: function (category) {
            var item = this.categorias.find(item => item.nombre === category)
            return item.border_class
        },
        setActiveClass: function (category) {
            if (this.categoria.includes(category.nombre)) {
                return category.bg_class
            } else {
                return category.outline_class
            }
        },
        switchCategory: function (category) {
            var temp = []
            if (this.categoria.includes(category)) {
                this.categoria.filter(function (item) {
                    if (item !== category) {
                        temp.push(item)
                    }
                })
                this.categoria = temp
            } else {
                this.categoria.push(category)
            }
        }
    }
}
</script>
