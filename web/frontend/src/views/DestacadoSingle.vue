<template>
    <div>
        <section class="noticia-single">
            <div class="container">
                <div class="row">
                    <div class="col">
                        <h3 class="noticia-single__title">{{destacado.title}}</h3>
                        <img :src="destacado.cover" class="noticia-single__cover">
                        <div class="noticia-single__info">
                            <h4 class="noticia-single__author">{{destacado.autor}}</h4>
                            <h4 class="noticia-single__date">{{destacado.fecha | formatDate}}</h4>
                        </div>
                        <div class="noticia-single__content">
                            <span v-html="destacado.descripcion"></span>
                            <br>
                            <span v-if="destacado.url_relacionadas.length > 0"> Noticias Relevantes:
                                <span v-for="relacionada in destacado.url_relacionadas" v-bind:key="relacionada.titulo">
                                    <a :href="relacionada.url" target="_blank">{{relacionada.titulo}}</a><br>
                                </span>
                            </span>
                            <br>
                            <span v-if="destacado.url_fuente">Fuente: <a :href="destacado.url_fuente.url" target="_blank">
                            {{destacado.url_fuente.titulo}}</a></span>
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
  name: 'DestacadoSingle',
  components: {
  },
  data () {
    return {
        destacado: [],
        params: ''
    }
  },
    mounted () {
        var self = this
        var destacados = []
        self.params = Number(self.$route.query.destacados)
        axios
            .get('./json/destacados.json')
            .then(response => {
                response.data.data.destacados.filter(function (item) {
                    if (item.id === self.params) {
                        destacados.push(item)
                    }
                })
                self.destacado = destacados[0]
            })
            .catch(error => console.log(error))
    },
  methods: {
  }
}
</script>