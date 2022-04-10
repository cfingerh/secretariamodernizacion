<template>

    <div class="ficha">
        <div class="chart__header">
            <h2>Satisfacción última experiencia</h2>
            <h4>{{institucion.nombre}}</h4>
        </div>
        <div class="chart__body">
            <div class="row">
                <div class="col-12 col-md-4 ajustado">
                    <div class="group-links">
                        <a class="ficha-selector-medicion"  v-bind:class="{ active: config.medicion==='experiencia' }" @click="cambiar_medicion('experiencia')">
                            Satisfacción última experiencia
                            <span title="Satisfacción última experiencia" class="tooltip-info">
                                <font-awesome-icon icon="info-circle" />
                            </span>
                            <span style="float:right">
                                <font-awesome-icon icon="chevron-right"/>
                                </span>
                        </a>
                        <a class="ficha-selector-medicion"  v-bind:class="{ active: config.medicion==='eval_inst' }" @click="cambiar_medicion('eval_inst')">
                            Evaluación Institución
                            <span title="Evaluación Institución" class="tooltip-info">
                                <font-awesome-icon icon="info-circle" />
                            </span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right" /></span>
                        </a>
                    </div>
                </div>
                <div class="col-12 col-md-8 ajustado derecha p-4">
                    <h5>{{subtitle()}}</h5>
                    <!-- <div class="row">
                        <div class="col">
                            <label class="form-check-label" style="float:right" for="radioSatisfaccion">Año 2020</label>
                            <input @input="cambiar_tipo()" value="ultimo" v-model="periodo"  class="form-check-input" style="float:right; margin-right:10px" type="radio" name="radioSatisfaccion" id="radioSatisfaccionUltimo">
                        </div>
                        <div class="col">
                            <input @input="cambiar_tipo()" value="historico" v-model="periodo" class="form-check-input" style="float:left;margin-right:10px" type="radio">
                            <label  class="form-check-label" style="float:left"  for="radioSatisfaccion">Histórico</label>
                        </div>
                    </div> -->
                    <div id="institucion-historic-chart">
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { utils } from '@/utils.js'

export default {
    name: 'HistoricChart',
    props: ['institucion'],
    mixins: [utils],
    data () {
        return {
            config: {
                elementId: 'institucion-historic-chart',
                tipo_grafico: 'barra',
                medicion: 'experiencia',
                periodo: 'historico',
                filtro: null
            }

        }
    },
    methods: {
        subtitle () {
            if (this.config.medicion === 'experiencia') {
                return 'Satisfacción última experiencia'
            }
            if (this.config.medicion === 'eval_inst') {
                return 'Evaluación de las instituciones'
            }
            if (this.config.medicion === 'tipo_tramite') {
                return 'Satisfacción por tipo de trámite'
            }
        },
        cambiar_medicion (medicion) {
            this.config.medicion = medicion
            this.cambiar(this.config)
        }
    },

    mounted () {
        this.cambiar(this.config)
    }
}
</script>
yarn
