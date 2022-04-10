<template>
    <div>
        <section class="proyectos">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <nav aria-label="breadcrumb">
                            <ol class="breadcrumb">
                                <li class="breadcrumb-item"><router-link to="/">Inicio</router-link></li>
                                <li class="breadcrumb-item active" aria-current="page">Proyectos</li>
                            </ol>
                        </nav>
                    </div>
                </div>
                <div class="row">
                    <div class="col">
                        <h3 class="proyectos__title">Proyectos</h3>
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
                <div class="row" v-if="proyectos.length == 0">
                    No hay resultados
                </div> -->
                <div class="row">
                    <div class="col-lg-4 col-md-6 mb-4" v-for="proyecto in proyectos" v-bind:key="proyecto.id">
                        <div class="card card--proyecto h-100">
                            <img :src="proyecto.cover" class="card-img-top--proyecto" alt="">
                            <div class="card-body">
                                <h5 class="card-title">{{proyecto.titulo}}</h5>
                                <!-- <p class="card-text" v-html="proyecto.descripcion_corta"></p> -->
                                <router-link :to="'/proyecto-single?proyecto=' + proyecto.id" class="proyecto__more">Conoce más</router-link>
                                <!-- <span :class="getBorderClass(proyecto.categoria)">{{proyecto.categoria}}</span> -->
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
    name: 'Proyectos',
    components: {
    },
    data () {
        return {
            proyectos: [],
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
                        if (item.proyecto) {
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
                .get('./json/proyectos.json')
                .then(response => {
                    self.proyectos = response.data.data.proyectos
                    if (self.categoria.length > 0) {
                        self.proyectos.filter(function (item) {
                            if (self.categoria.includes(item.categoria)) {
                                filtrado.push(item)
                            }
                        })
                        self.proyectos = filtrado
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
