<template>
    <div v-if="resultados">
        <section>
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <img src="/img/gob-line.svg" class="mb-4">
                        <div class="titulo">
                            <h1>Resultados generales 2021 y su evolución</h1>
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
                                <li>Considerando el volumen de encuestas, este estudio es uno de los más grandes que se realiza a nivel nacional. Este año 2022 se superarán las 110.000 encuestas.</li>
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
                <!-- <div class="box-ficha card">
                    <general-canal></general-canal>
                </div>
                <div class="box-ficha card">
                    <general-dimension></general-dimension>
                </div> -->

            </div>
        </section>

    </div>
</template>

<script>
import axios from 'axios'
import GeneralesParticipacion from './GeneralesParticipacion.vue'
import GeneralesExperiencia from './GeneralesExperiencia.vue'
import GeneralesTipoUsuario from './GeneralesTipoUsuario.vue'
// import GeneralCanal from './GeneralCanal.vue'
// import GeneralDimension from './GeneralDimension.vue'

export default {
    name: 'DetalleServicio',
    components: {
        GeneralesParticipacion,
        GeneralesExperiencia,
        GeneralesTipoUsuario,
        // GeneralCanal,
        // GeneralDimension,
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
