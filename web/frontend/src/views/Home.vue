<template>
    <div v-if="datos">
        <section class="intro-home">
            <div class="container">
                <div class="row align-items-center" v-if="datos.panel_1">
                    <div class="col-md-5">
                        <!-- <h2 class="intro">
                            <strong class="text--light-blue intro__110">{{datos.panel_1['110_1']}}</strong>
                            <strong>
                                <span class="text--light-blue intro__28">{{datos.panel_1['28']}}</span>
                                <span class="text--light-blue intro__35">{{datos.panel_1['35']}}</span>
                                <span class="text--red intro__40">{{datos.panel_1['40']}}</span>
                            </strong>
                            <strong class="text--red intro__110">{{datos.panel_1['110_2']}}</strong>
                        </h2> -->
                        <img src="/img/que-es-modernizacion.svg" class="intro-home__img">
                    </div>
                    <div class="col-md-7" v-html="datos.panel_1['texto']">
                    </div>
                </div>
            </div>
        </section>
        <section class="home__items">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-12" v-if="datos.panel_2">
                        <h2 class="home__title"><span>{{datos.panel_2['titulo']}}</span></h2>
                    </div>
                </div>
            </div>
            <div class="container" v-if="datos.panel_2">
                <div class="row text-center" v-if="datos.panel_2['items'].length > 0">
                    <div class="col-md-3" v-for="item in datos.panel_2['items']" v-bind:key="item.titulo">
                        <img :src="item.cover" class="home__item-img">
                        <h3 class="home__item-title">{{item.titulo}}</h3>
                        <p class="home__item-description">{{item.descripcion}}</p>
                        <a :href="item.boton_ruta_externo" target="_blank" class="btn btn-primary d-block home__item-btn" v-if="item.boton_ruta_externo">{{item.boton_titulo}}</a>
                        <router-link :to="item.boton_ruta" class="btn btn-primary d-block home__item-btn" v-if="item.boton_ruta">{{item.boton_titulo}}</router-link>
                    </div>
                </div>
            </div>
        </section>
<!--         <section class="novedades">
            <div class="container-fluid">
                <div class="row">
                    <div class="col-12" v-if="datos.panel_2">
                        <h2 class="novedades__title"><span>{{datos.panel_2['titulo']}}</span></h2>
                    </div>
                </div>
            </div>
            <div class="container">
                <b-carousel id="carousel-1" v-model="slide" :interval="4000" controls indicators img-width="1024" img-height="480">
                    <b-carousel-slide img-src="/img/slide-home.png">
                        <h3 class="news__title">Recomendaciones OCDE #Transformación Digital en Chile</h3>
                        <p class="news__description">La Secretaría de Modernización del Estado del Ministerio de Hacienda junto con la División de Gobierno Digital del Ministerio Secretaría General de la Presidencia tiene el agrado de invitar a usted, al seminario:  Transformación Digital en Chile, Reportes OECD.</p>
                        <a href="" class="news__link">Descargar documentos</a>
                    </b-carousel-slide>

                    <b-carousel-slide img-src="/img/slide-home.png">
                        <h3 class="news__title">Recomendaciones OCDE #Transformación Digital en Chile</h3>
                        <p class="news__description">La Secretaría de Modernización del Estado del Ministerio de Hacienda junto con la División de Gobierno Digital del Ministerio Secretaría General de la Presidencia tiene el agrado de invitar a usted, al seminario:  Transformación Digital en Chile, Reportes OECD.</p>
                        <a href="" class="news__link">Descargar documentos</a>
                    </b-carousel-slide>
                </b-carousel>
            </div>
        </section> -->
    </div>
</template>
<script>
import axios from 'axios'
export default {
    name: 'Home',
    components: {
    },
    data () {
        return {
            datos: [],
            slide: null
        }
    },
    mounted () {
        axios
            .get('./json/home.json')
            .then(response => (this.datos = response.data.data))
            .catch(error => console.log(error))
    }
}
</script>
