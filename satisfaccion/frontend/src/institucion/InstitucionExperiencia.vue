<template>

    <div class="ficha">
        <div class="row">
            <div class="col-12 col-md-6">
                <div class="chart__header">
                    <h2>Satisfacción última experiencia</h2>
                </div>
                <div class="chart__body">
                    <div id="generales-experiencia"></div>
                </div>
            </div>
            <div class="col-12 col-md-6">
                <div class="chart__header">
                    <h2>Evaluación de la institución</h2>
                </div>
                <div class="chart__body">
                    <div id="generales-eval_inst"></div>
                </div>
            </div>

        </div>
        <small class="comentario_tooltip" >Valores se presentan redondeados, por lo que suma puede ser distinta a 100%</small>
    </div>
</template>

<script>
import { utils } from '@/utils.js'

export default {
    name: 'HistoricChart',
    mixins: [utils],
    data () {
        return {
            config: {
                elementId: 'generales-experiencia',
                tipo_grafico: 'barra',
                medicion: 'experiencia',
                periodo: 'historico',
                // filtro: { institucion__codigo_dipres: this.$route.params.id }
            },
            configB: {
                elementId: 'generales-eval_inst',
                tipo_grafico: 'barra',
                medicion: 'eval_inst',
                periodo: 'historico',
                // filtro: { institucion__codigo_dipres: this.$route.params.id }
            }
        }
    },
    methods: {

    },

    mounted () {
        this.cambiar(this.config)
        this.cambiar(this.configB)
        // this.cambiar(this.config)
    }
}
</script>
