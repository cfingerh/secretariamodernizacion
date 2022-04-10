<template>
    <div>
        <section class="noticias">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <ul class="noticias__filters" v-if="categorias.length > 0">
                            <li class="noticias__filter-item" v-for="categoria in categorias" v-bind:key="categoria.nombre" @click="switchCategory(categoria.nombre)">{{ categoria.nombre }}</li>
                        </ul>
                    </div>
                    <div class="col">
                        <div class="form-inline">
                            <input class="form-control mr-sm-2" type="search" placeholder="Buscar Noticias" aria-label="Search" v-model="search">
                        </div>
                    </div>
                </div>
                <div class="row" v-if="destacados.length == 0">
                    No hay resultados
                </div>
                <div class="row" v-if="destacados.length > 0">
                    <div class="col-md-4" v-for="destacado in destacados" v-bind:key="destacado.id">
                        <div class="card">
                            <img :src="destacado.cover" class="card-img-top" alt="">
                            <div class="card-body">
                                <h5 class="card-title">{{destacado.titulo}}</h5>
                                <p class="card-text"><small class="text-muted">{{destacado.fecha | dateFormat}}</small></p>
                                <small>{{destacado.categoria}}</small>
                                <router-link :to="'/destacado-single?destacados=' + destacado.id" class="noticias__more">Leer más</router-link>
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
  name: 'Destacados',
  components: {
  },
  data () {
    return {
        categorias: [],
        destacados: [],
        categoria: null,
        search: ''
    }
  },
    mounted () {
        this.getCategoria()
        this.getData()
        this.$watch('categoria', (newLocale, oldLocale) => {
            if (newLocale !== oldLocale) {
                this.getData()
            }
        }, { immediate: true })
        this.$watch('search', (newLocale, oldLocale) => {
            if (newLocale !== oldLocale) {
                this.getData()
            }
        }, { immediate: true })
    },
    methods: {
        getCategoria: function () {
            var self = this
            axios
                .get('./json/categorias.json')
                .then(response => self.categorias = response.data.data.categorias)
                .catch(error => console.log(error))

        },
        getData: function () {
            var filtrado = []
            var self = this
            axios
                .get('./json/destacados.json')
                .then(response => {
                    self.destacados = response.data.data.destacados
                    if (self.categoria) {
                        self.destacados.filter(function (item) {
                            if (item.categoria === self.categoria) {
                                filtrado.push(item)
                            }
                        })
                        self.destacados = filtrado
                    } else if (self.search) {
                        const searchTerm = new RegExp(self.search, 'i')
                        self.destacados.filter(function (item) {
                            if (item.titulo.match(searchTerm)) {
                                filtrado.push(item)
                            }
                        })
                        self.destacados = filtrado

                    } 
                })
                .catch(error => console.log(error))

        },
        switchCategory: function (category) {
            if (this.categoria === category)
                this.categoria = null
            else
                this.categoria = category
        }
    }
}
</script>