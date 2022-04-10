<template>
    <div v-if="resultados">
        <section>
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <img src="/img/gob-line.svg" class="mb-4">
                        <div class="titulo">
                            <h1>Resultados generales 2020 y su evolución</h1>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <section class="bg-light">
            <div class="container">
                <div class="box-ficha card">
                    <h4>Cómo ha evolucionado la evaluación de satisfacción</h4>
                    <div class="row">
                        <div class="col-md-8">
                            <generales-participacion></generales-participacion>
                        </div>
                        <div class="col-md-4">
                            <ul>
                                <li>Esta medición de satisfacción de usuarios basada en el enfoque de evaluación de experiencia se aplicó por primera vez el año 2015.</li>
                                <li>El número de instituciones se ha ido incrementando con los años y el año 2019 se triplicó, incluyendo a la mayoría de las instituciones con mayor demanda de trámites y servicios del nivel central.</li>
                                <li>El año 2021 han comprometido su participación en la medición 62 instituciones</li>
                                <li>Considerando el volumen de encuestas, este estudio es uno de los más grandes que se realiza a nivel nacional. Este año 2021 se superarán las 100.000 encuestas.</li>
                            </ul>
                        </div>
                    </div>
                </div>

                <div class="box-ficha card">
                    <generales-experiencia></generales-experiencia>
                </div>
                <div class="box-ficha card">
                    <generales-tipo-usuario></generales-tipo-usuario>
                </div>
                <div class="box-ficha card">
                    <general-canal></general-canal>
                </div>
                <div class="box-ficha card">
                    <general-dimension></general-dimension>
                </div>

            </div>
        </section>

    </div>
</template>

<script>
import axios from 'axios'
import GeneralesParticipacion from './GeneralesParticipacion.vue'
import GeneralesExperiencia from './GeneralesExperiencia.vue'
import GeneralesTipoUsuario from './GeneralesTipoUsuario.vue'
import GeneralCanal from './GeneralCanal.vue'
import GeneralDimension from './GeneralDimension.vue'

export default {
    name: 'DetalleServicio',
    components: {
        GeneralesParticipacion,
        GeneralesExperiencia,
        GeneralesTipoUsuario,
        GeneralCanal,
        GeneralDimension,
    },
    async beforeCreate () {},
    mixins: [],
    data () {
        return { resultados: {} }
    },
    methods: {},
    mounted () {
        axios.get('/api/instituciones/' + this.$route.params.id).then(res => { this.institucion = res.data })
    }
}
</script>
