<template>
<div>
    <div id="myCarousel" class="carousel slide" data-bs-ride="carousel">
        <div class="carousel-indicators">
            <button type="button" data-bs-target="#myCarousel" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
            <button type="button" data-bs-target="#myCarousel" data-bs-slide-to="1" aria-label="Slide 2"></button>
            <button type="button" data-bs-target="#myCarousel" data-bs-slide-to="2" aria-label="Slide 3"></button>
        </div>
        <div class="carousel-inner">
            <div class="carousel-item active">
                <svg class="bd-placeholder-img" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice" focusable="false"><rect width="100%" height="100%" fill="#777"/></svg>
                <div class="container">
                    <div class="carousel-caption text-start">
                        <h1>Example headline.</h1>
                        <p>Some representative placeholder content for the first slide of the carousel.</p>
                        <p><a class="btn btn-lg btn-primary" href="#">Sign up today</a></p>
                    </div>
                </div>
            </div>
            <div class="carousel-item">
                <svg class="bd-placeholder-img" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice" focusable="false"><rect width="100%" height="100%" fill="#777"/></svg>
    <div class="container">
      <div class="carousel-caption">
        <h1>Another example headline.</h1>
        <p>Some representative placeholder content for the second slide of the carousel.</p>
        <p><a class="btn btn-lg btn-primary" href="#">Learn more</a></p>
    </div>
</div>
</div>
<div class="carousel-item">
<svg class="bd-placeholder-img" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" preserveAspectRatio="xMidYMid slice" focusable="false"><rect width="100%" height="100%" fill="#777"/></svg>

<div class="container">
  <div class="carousel-caption text-end">
    <h1>One more for good measure.</h1>
    <p>Some representative placeholder content for the third slide of this carousel.</p>
    <p><a class="btn btn-lg btn-primary" href="#">Browse gallery</a></p>
    </div>
    </div>
    </div>
    </div>
    <button class="carousel-control-prev" type="button" data-bs-target="#myCarousel" data-bs-slide="prev">
    <span class="carousel-control-prev-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Previous</span>
    </button>
    <button class="carousel-control-next" type="button" data-bs-target="#myCarousel" data-bs-slide="next">
    <span class="carousel-control-next-icon" aria-hidden="true"></span>
    <span class="visually-hidden">Next</span>
    </button>
</div>
    <section>
        <div class="container">
            <div class="row">
                <div class="col-md-5">
                    <div class="card card-info">
                        <header>
                            <h3>¿Qué medimos?</h3>
                        </header>
                        <section>
                            <ul class="content-home__list">
                                <li class="content-home__item">Estudiamos la satisfacción de los usuarios en relación con instituciones y servicios públicos</li>
                                <li class="content-home__item">Los trámites e interacciones medidas representan más del 80% de la demanda anual de servicios del Estado (sin contar salud y educación)</li>
                                <li class="content-home__item">Aplicamos encuestas telefónicas a usuarios acerca de su última experiencia con la institución</li>
                                <li class="content-home__item">Así se obtiene información sobre los factores que afectan la satisfacción</li>
                                <li class="content-home__item">Con el objetivo de entregar este insumo para gestión de las instituciones</li>
                            </ul>
                        </section>
                        <div class="card-footer">
                            <button class="btn btn-primary">
                            Quiero conocer más
                            </button>
                        </div>
                    </div>
                    <ul class="link__list">
                        <li class="link__item">
                            <a href="">Descarga la metodología usada en el proceso de encuestas y resultados</a>
                        </li>
                        <li class="link__item">
                            <a href="">Descarga los datos obtenidos en el proceso</a>
                        </li>
                    </ul>
                </div>
                <div class="col-md-7">
                    <carousel :per-page="1" :mouse-drag="false" :navigationEnabled="true"
                    :paginationEnabled="false"
                     navigation-next-label=">" navigation-prev-label="<" :loop="true" :speed="300">
                        <slide v-for="institucion in instituciones" v-bind:key="institucion.nombre">
                            <box-instituciones :institucion="institucion"></box-instituciones>
                        </slide>
                    </carousel>
                </div>
                <historic-chart/>
            </div>
        </div>
    </section>
</div>
</template>

<script>
import BoxInstituciones from '@/components/BoxInstituciones.vue'
import { Carousel, Slide } from 'vue-carousel'
import axios from 'axios'
export default {
    name: 'Home',
    components: { Carousel, Slide, BoxInstituciones },
    async beforeCreate () {},
    mixins: [],
    data () {
        return { instituciones: null }
    },
    methods: {},
    mounted () {
        axios.get('/api/instituciones').then(res => { this.instituciones = res.data })
    }
}
</script>
