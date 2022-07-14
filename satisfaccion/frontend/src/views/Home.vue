<template>
<div>
   <div class="content--home">
        <div class="col-md-10 offset-md-1"> <!--row-->
            <div class="col-12 col-lg-6 col-md-6 content--home--text" >
                    <h1 class="color-white">¡Tu experiencia cuenta para el Estado!</h1>
                    <p class="color-white">Las instituciones públicas, junto a la Secretaría de Modernización del Estado, miden anualmente la satisfacción de sus usuarios/as para identificar oportunidades de mejora a la entrega de servicios.
                    La información del sentir ciudadano permite orientar las iniciativas de modernización y evaluar continuamente los avances.</p>
                    <div><a type="button" href="/metodologia" class="btn btn-info">Ver más</a></div>
                </div>
                <div class="col-12 col-lg-6 col-md-6 content--home--img">
                    <img src="img/usuarios_2.svg" alt="" class="home--img" style="max-height:260px">
                </div>
        </div>
    <br>
    </div>
    <section class="featured--home bg-light">
        <div class="container">
            <div class="col-md-12">
                <h1 class="carousel__title">Resultados generales 2021</h1>
                <!-- <p class="mb-4">A nivel agregado o general, el estudio 2021 arroja los siguientes resultados:</p> -->

                <div id="carouselHeader" class="carousel carousel-dark slide" data-bs-ride="carousel" v-if="sliders">
                        <div class="carousel-indicators">
                            <button type="button" data-bs-target="#carouselHeader" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                            <button type="button" data-bs-target="#carouselHeader" data-bs-slide-to="1" aria-label="Slide 1"></button>
                            <button type="button" data-bs-target="#carouselHeader" data-bs-slide-to="2" aria-label="Slide 2"></button>
                        </div>
                        <div class="carousel-inner">
                            <div class="carousel-item active">
                                <div class="carousel-item-detalle">
                                    <h2 class="carousel__subtitle">Satisfacción última experiencia 2021</h2>
                                    <img src="img/ultima-experiencia.svg" alt="trimestres" class="metodologia_2--img" style="height:400px">
                                    <span>Revisa en detalle la <a href="/metodologia">Metodología, datos y documentación</a></span>
                                </div>
                            </div>
                            <div class="carousel-item">
                                <div class="carousel-item-detalle">
                                    <h2 class="carousel__subtitle">Cómo ha evolucionado la evaluación de satisfacción: número de instituciones</h2>
                                    <img src="img/hemos-crecido-2021.svg" alt="trimestres" class="metodologia_2--img esconder-chico" style="height:400px;">
                                    <img src="img/hemos-crecido-sm-14.svg" alt="trimestres" class="metodologia_2--img esconder-grande" style="height:400px">
                                    <span>Este año 2022 se superarán las 110.000 encuestas.</span>
                                </div>
                            </div>
                            <!-- <div class="carousel-item">
                                <div class="carousel-item-detalle">
                                    <h2 class="carousel__subtitle">Preferencia de uso por canal</h2>
                                    <img src="img/infografia_por_canal.png" alt="trimestres" class="metodologia_2--img esconder-chico" style="max-height:400px">
                                    <img src="img/Preferencia canal-sm_Mesa de trabajo.svg" alt="trimestres" class="metodologia_2--img esconder-grande" style="max-height:400px">

                                </div>
                            </div> -->
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#carouselHeader" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#carouselHeader" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                    </div>

            </div>
        </div>
    </section>

    <section class="bg-light">
        <div class="container">

            <div class="row">
                <div class="col-md-12">
                    <img src="/img/gob-line.svg" class="mb-4">
                    <div class="titulo">
                        <h1>Resultados por Institución:</h1>
                    </div>
                    <p class="text-center">Revisa todas las <a href="/resultados">instituciones que participan</a> del año 2021 y anteriores</p>

                    <div id="carouselExampleControl" class="carousel carousel-dark slide" data-bs-ride="carousel" v-if="sliders">
                        <div class="carousel-indicators">
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="0" class="active" aria-current="true" aria-label="Slide 1"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="1" aria-label="Slide 1"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="2" aria-label="Slide 2"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="3" aria-label="Slide 3"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="4" aria-label="Slide 4"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="5" aria-label="Slide 5"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="6" aria-label="Slide 6"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="7" aria-label="Slide 7"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="8" aria-label="Slide 8"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="9" aria-label="Slide 9"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="10" aria-label="Slide 10"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="11" aria-label="Slide 11"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="12" aria-label="Slide 12"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="13" aria-label="Slide 13"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="14" aria-label="Slide 14"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="15" aria-label="Slide 15"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="16" aria-label="Slide 16"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="17" aria-label="Slide 17"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="18" aria-label="Slide 18"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="19" aria-label="Slide 19"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="20" aria-label="Slide 20"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="21" aria-label="Slide 21"></button>
                            <button type="button" data-bs-target="#carouselExampleControl" data-bs-slide-to="22" aria-label="Slide 22"></button>

                        </div>
                        <div class="carousel-inner">
                            <div class="carousel-item carousel-item-md" v-for="slide in sliders" v-bind:key="slide" v-bind:class="{ active: slide===0}">
                                <div class="row" >
                                    <div class="col-12 col-md-6">
                                        <div class="box-institucion-left">
                                            <box-instituciones :institucion="instituciones[slide*2]"></box-instituciones>
                                        </div>
                                    </div>
                                    <div class="col-12 col-md-6" >
                                        <div class="box-institucion-right">
                                            <box-instituciones :institucion="instituciones[slide*2+1]"></box-instituciones>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControl" data-bs-slide="prev">
                            <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Previous</span>
                        </button>
                        <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControl" data-bs-slide="next">
                            <span class="carousel-control-next-icon" aria-hidden="true"></span>
                            <span class="visually-hidden">Next</span>
                        </button>
                    </div>
                </div>

            </div>
        </div>
    </section>
    <section class="info--home">
        <div class="container">
            <div class="row">
                <div class="col-12 col-lg-6">
                    <div class="card card-info">
                        <header>
                            <h3><font-awesome-icon :icon="['fas', 'chart-bar']" /> ¿Qué medimos?</h3>
                        </header>
                        <section>
                            <ul class="content-home__list">
                                <li class="content-home__item">Medimos la satisfacción de las personas que han interactuado con el Estado, preguntándoles directamente por su experiencia con las instituciones públicas en evaluación.</li>
                                <li class="content-home__item">Las instituciones que son evaluadas en esta medición realizan más del 88% de la demanda de trámites y servicios del Estado central.</li>
                            </ul>
                        </section>
                    </div>
                </div>
                <div class="col-12 col-lg-6">
                    <div class="card card-info">
                        <header>
                            <h3><font-awesome-icon :icon="['fas', 'comments']" /> ¿Cómo medimos?</h3>
                        </header>
                        <section>
                            <ul class="content-home__list">
                                <li class="content-home__item">Nos contactamos a través de encuestas telefónicas o web con personas que han interactuado con las instituciones en evaluación en los últimos 3 meses</li>
                                <li class="content-home__item">Las encuestas son aplicadas por empresas con reconocida experiencia y adjudicadas a través de licitación pública.</li>
                                <li class="content-home__item">Toda la información que se genera en esta medición es entregada y analizada con cada una de las instituciones participantes para implementar acciones para mejorar la experiencia de los usuarios.</li>
                            </ul>
                        </section>
                        <div class="card-footer">
                            <a class="btn btn-secondary" href="/metodologia">
                            Conocer más
                            </a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</div>
</template>

<script>
import ChevronRight from '@/../public/img/right-slider.png'
import ChevronLeft from '@/../public/img/left-slider.png'
import BoxInstituciones from '@/components/BoxInstituciones.vue'
import axios from 'axios'
export default {
    name: 'Home',
    components: {
        BoxInstituciones,
    },
    async beforeCreate () {},
    mixins: [],
    data () {
        return {
            instituciones: null,
            sliders: null
        }
    },
    methods: {
        shuffle: function (array) {
            var currentIndex = array.length; var temporaryValue; var randomIndex
            while (currentIndex !== 0) {
                randomIndex = Math.floor(Math.random() * currentIndex)
                currentIndex -= 1
                temporaryValue = array[currentIndex]
                array[currentIndex] = array[randomIndex]
                array[randomIndex] = temporaryValue
            }
            var conDatos = array.filter(a => { return a.datos.anios.length > 1 })
            return conDatos
        },
        range: function (start, end) {
            if (start > end) return [start]
            return [start, ...this.range(start + 1, end)]
        }
    },
    mounted () {
        axios.get('/api/instituciones').then(res => {
            this.instituciones = this.shuffle(res.data)
            this.sliders = this.range(0, (this.instituciones.length / 2) - 2)
            console.log(this.instituciones)
            console.log(this.sliders)
        }).catch(err => {
            console.log(err)
        })
    },
    computed: {
        navigationNext () {
            const chevronRight = ChevronRight
            return `<img src="${chevronRight}"/>`
        },
        navigationPrev () {
            const chevronLeft = ChevronLeft
            return `<img src="${chevronLeft}"/>`
        },
    }
}
</script>

<style scoped>
.box-institucion-left
{
margin-left:40px;
}

.box-institucion-right
{
margin-right:40px;
}

.carousel-item-md {
    height: 550px;
}

.carousel-item-detalle{
        margin-left:120px;
        margin-right:120px;
        text-align:center
    }

@media (max-width: 720px){
    .carousel-item-md {
        height: 1024px;
            }
    .carousel-item-detalle{
        margin-left:20px;
        margin-right:20px;
        text-align:center
    }
    .box-institucion-left
    {
    margin-left:0px;
    }

    .box-institucion-right
    {
    margin-right:0px;
    }
    .carousel-indicators
    {
        display: none;
    }

}

#carouselsHeader {
  margin-left: 50px;
  margin-right: 50px;
}
.carousel-control-left {
  margin-left: -25px;
}

.carousel-control.right {
  margin-right: -25px;
}

</style>
