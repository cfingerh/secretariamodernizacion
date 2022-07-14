<template>
    <div v-if="institucion">
        <section>
            <div class="container">
                <ol class="breadcrumb">
                    <li><a href="/">Portada</a></li>
                    <li><a href="/resultados">Resultados por Institución</a></li>
                    <li>{{institucion.nombre_a_mostrar}}</li>
                </ol>
                <div class="row">
                    <div class="col-md-8">
                        <img src="/img/gob-line.svg" class="mb-4">
                        <div class="titulo" style="float:left">
                            <h1>{{institucion.nombre_a_mostrar}}</h1>
                            <div class="updated-nombre_a_mostrar">Años evaluados: {{institucion.datos.anios_string}}</div>

                        </div>

                    </div>
                    <div class="col-md-4">
                        <!-- <a style="float:right" @click="informe()" type="button" class="btn button-more btn-secondary">Descargar informe año {{institucion.ultimo_anio}}</a> -->
                    </div>
                </div>
            </div>
        </section>
        <section v-if="institucion.datos.nota_metodologica">
            <div class="container">
                Nota: {{institucion.datos.nota_metodologica}}
            </div>
        </section>

        <section class="bg-light">
            <div class="container">
                <div class="row">
                    <div class="col-md-12">
                        <h2>Resultados de la última medición: año {{ultimo_anio()}}</h2>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6 box-detalle-arriba-around">
                        <div class="box-detalle-arriba pt-4">
                            <div class="neto bad mt-4">
                                 {{institucion.resumen.ultimo.experiencia.neta}}%
                            </div>
                            <p class="text-center mt-4">Índice de satisfacción neta última experiencia <span title="La satisfacción neta es la diferencia entre la evaluación positiva (nota 6 y 7) y la evaluación negativa (nota menor o igual a 4)" class="tooltip-info"><font-awesome-icon icon="info-circle" /></span></p>
                            <div class="row">
                                <div class="col good">
                                    {{institucion.resumen.ultimo.experiencia.positivo}}% <font-awesome-icon :icon="['far', 'smile']" />
                                </div>
                                <div class="col bad">
                                    {{institucion.resumen.ultimo.experiencia.negativo}}% <font-awesome-icon :icon="['far', 'frown']" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6 box-detalle-arriba-around">
                        <div class="box-detalle-arriba pt-4">
                            <div class="neto good mt-4">
                                {{institucion.resumen.ultimo.eval_inst.neta}}%
                            </div>
                            <p class="text-center mt-4">Evaluación general neta de la Institución <span title="La evaluación general neta es la diferencia entre la evaluación positiva (nota 6 y 7) y la evaluación negativa (nota menor o igual a 4)" class="tooltip-info"><font-awesome-icon icon="info-circle" /></span></p>
                            <div class="row">
                                <div class="col good">
                                    {{institucion.resumen.ultimo.eval_inst.positivo}}% <font-awesome-icon :icon="['far', 'smile']" />
                                </div>
                                <div class="col bad">
                                    {{institucion.resumen.ultimo.eval_inst.negativo}}% <font-awesome-icon :icon="['far', 'frown']" />
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- <div class="col-md-4 box-detalle-arriba-around">
                        <div class="box-detalle-arriba">
                            <institucion-punto-contacto :institucion='institucion'></institucion-punto-contacto>
                        </div>
                    </div> -->
                </div>
            </div>
        </section>
        <section class="bg-light">
            <div class="container">
                <div class="box-ficha card">
                    <institucion-experiencia></institucion-experiencia>
                </div>
                <div class="box-ficha card">
                    <institucion-tipo-usuario :anios="institucion.datos.anios"></institucion-tipo-usuario>
                </div>

                <!-- <div class="box-ficha card">
                    <institucion-historic-chart :institucion='institucion'></institucion-historic-chart>
                </div>

                <div class="box-ficha card">
                    <institucion-tipo-usuario :institucion='institucion'></institucion-tipo-usuario>
                </div>

                <div class="box-ficha card">
                    <institucion-canal :institucion='institucion'></institucion-canal>
                </div>

                <div class="box-ficha card">
                    <institucion-dimension :institucion='institucion'></institucion-dimension>
                </div> -->

            </div>
        </section>
    </div>
</template>

<script>
import axios from 'axios'
// import InstitucionHistoricChart from '@/institucion/InstitucionHistoricChart.vue'
// import InstitucionTipoUsuario from '@/institucion/InstitucionTipoUsuario.vue'
// import InstitucionCanal from '@/institucion/InstitucionCanal.vue'
// import InstitucionDimension from '@/institucion/InstitucionDimension.vue'
// import InstitucionPuntoContacto from '@/institucion/InstitucionPuntoContacto.vue'
import InstitucionExperiencia from '@/institucion/InstitucionExperiencia.vue'
import InstitucionTipoUsuario from '@/institucion/InstitucionTipoUsuario.vue'

export default {
    name: 'DetalleServicio',
    components: {
        // InstitucionHistoricChart,
        // InstitucionTipoUsuario,
        // InstitucionCanal,
        // InstitucionDimension,
        //  InstitucionPuntoContacto,
        InstitucionExperiencia,
        InstitucionTipoUsuario
    },
    async beforeCreate () {},
    mixins: [],
    data () {
        return { institucion: null }
    },
    methods: {
        informe () {
            axios.get('/api/instituciones/' + this.$route.params.id + '/ultimo_informe').then(res => { window.open(res.data.url) })
        },
        ultimo_anio () {
            if (!this.institucion) { return null }

            return this.institucion.datos.anios[this.institucion.datos.anios.length - 1]
        }

    },
    mounted () {
        axios.get('/api/instituciones/' + this.$route.params.id).then(res => {
            res.data.ultimo_anio = res.data.datos.anios[res.data.datos.anios.length - 1]
            this.institucion = res.data
        })
    }
}
</script>
