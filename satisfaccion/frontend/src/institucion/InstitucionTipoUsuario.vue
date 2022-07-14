<template>

    <div class="ficha">
        <div class="row">
            <div class="col-12 col-md-12" style="text-align:center">
                <h1>Satisfacción Última Experiencia</h1>
            </div>
            <br><hr><br>
        </div>
        <div class="row">
            <div class="col-12 col-md-12">
                <div class="chart__header">
                    <h2>Satisfacción neta por rango edad</h2>
                </div>
            </div>
            <div class="col-12 col-md-12">
                <div class="chart__body">
                    <div id="generales-edad" ></div>
                </div>
            </div>
            <div class="col-12 col-md-12">
                <div class="chart__header">
                    <h2>Satisfacción neta por género</h2>
                </div>
            </div>
            <div class="col-12 col-md-12">
                <div class="chart__body">
                    <div id="generales-sexo"></div>
                </div>
            </div>
            <!-- <div class="col-12 col-md-12">
                <br>
                <br>
                <div class="chart__header">
                    <h2>Satisfacción neta por nivel educacional</h2>
                </div>
            </div>
            <div class="col-12 col-md-12">
                <div class="chart__body">
                    <div id="generales-educacion"></div>
                </div>
            </div> -->
            <div class="col-12 col-md-12">
                <br>
                <br>
                <div class="chart__header">
                    <h2>Satisfacción neta por habilitación</h2>
                </div>
            </div>
            <div class="col-12 col-md-12">
                <div class="chart__body">
                    <div id="generales-habilitado"></div>
                </div>
            </div>
            <div class="col-12 col-md-12">
                <br><br>
                <small class="comentario_tooltip" >
                La satisfacción neta es la diferencia entre la evaluación positiva (nota 6 y 7) y la evaluación negativa (nota menor o igual a 4)
                </small>
            </div>

        </div>
    </div>
</template>

<script>
import { utils } from '@/utils.js'

export default {
    name: 'HistoricChart',
    props: ['anios'],
    mixins: [utils],
    data () {
        return {
            ultimoAnio: this.anios[this.anios.length - 1],
            configA: {
                elementId: 'generales-edad',
                tipo_grafico: 'linea_tipo',
                medicion: 'experiencia',
                periodo: 'ultimo',
                grupo: 'edad',
                anio: this.anios[this.anios.length - 1]
            },
            configB: {
                elementId: 'generales-sexo',
                tipo_grafico: 'linea_tipo',
                medicion: 'experiencia',
                periodo: 'ultimo',
                grupo: 'sexo',
                anio: this.anios[this.anios.length - 1]
            },
            // configC: {
            //     elementId: 'generales-educacion',
            //     tipo_grafico: 'linea_tipo',
            //     medicion: 'experiencia',
            //     periodo: 'ultimo',
            //     grupo: 'educacion',
            //     anio: this.anios[this.anios.length - 1]
            // },
            configD: {
                elementId: 'generales-habilitado',
                tipo_grafico: 'linea_tipo',
                medicion: 'experiencia',
                periodo: 'ultimo',
                grupo: 'habilitado',
                anio: this.anios[this.anios.length - 1]
            },

        }
    },
    methods: {

    },
    mounted () {
        this.cambiar(this.configA)
        this.cambiar(this.configB)
        // this.cambiar(this.configC)
        this.cambiar(this.configD)
    }
}
</script>

<style scoped>
.chart__header{
    text-align: center;
}
.chart__body div
{
    max-width:600px;
    margin:auto;
}
</style>
