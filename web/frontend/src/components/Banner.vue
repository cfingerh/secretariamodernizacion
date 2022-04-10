<template>
    <section class="featured-home" v-if="datos">
        <div class="container">
        <div class="row">
            <div class="col-lg-7">
                <!-- <img :src="datos.cover1" class="featured-home__img--1"> -->
                <h1 class="featured-home__title">
                    <span class="featured-home__title--1">Diseñamos, gestionamos y apoyamos el</span>
                    <span class="featured-home__title--2">desarrollo de proyectos transversales</span>
                    <span class="featured-home__title--3">de modernización del estado buscando</span>
                    <span class="featured-home__title--4">mejorar la satisfacción del ciudadano</span>
                </h1>
            </div>
            <div class="col-md-5">
                <img :src="datos.cover" class="featured-home__img--2 d-none d-lg-block">
            </div>
        </div>
    </div>
    </section>
</template>
<script>
import axios from 'axios'
export default {
    name: 'Banner',
    components: {
    },
    data () {
        return {
            datos: []
        }
    },
    mounted () {
        axios
            .get('./json/banner.json')
            .then(response => (this.datos = response.data.data))
            .catch(error => console.log(error))
    }
}
</script>
