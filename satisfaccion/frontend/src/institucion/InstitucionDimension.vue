<template>

    <div class="ficha">
        <div class="chart__header">
            <h2>Dimensiones de la experiencia</h2>
            <h4>{{institucion.nombre}}</h4>
        </div>
        <div class="chart__body">
            <div class="row">
                <div class="col-12 col-md-4 ajustado">
                    <div class="group-links">
                        <a class="ficha-selector-medicion"  v-bind:class="{ active: config.medicion==='atributos' }" @click="cambiar_medicion('atributos')">
                            Evaluación atributos de Experiencia
                            <span title="Tooltip" class="tooltip">
                                <font-awesome-icon icon="info-circle" />
                            </span>
                            <span style="float:right">
                                <font-awesome-icon icon="chevron-right"/>
                            </span>
                        </a>
                        <a class="ficha-selector-medicion"  v-bind:class="{ active: config.medicion==='imagen' }" @click="cambiar_medicion('imagen')">
                            Dimensiones de la imagen de la Institución
                            <span title="Tooltip" class="tooltip">
                                <font-awesome-icon icon="info-circle" />
                            </span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right" /></span>
                        </a>
                    </div>
                </div>
                <div class="col-12 col-md-8 ajustado derecha p-4">
                    <h5>{{subtitle()}}</h5>
                    <div class="row" style="display:none">
                        <div class="col">
                            <label class="form-check-label" style="float:right" for="radioSatisfaccion">Año {{config.ultimo_anio}}</label>
                            <input @input="cambiar_tipo()" value="ultimo" v-model="periodo"  class="form-check-input" style="float:right; margin-right:10px" type="radio" name="radioSatisfaccion" id="radioSatisfaccionUltimo">
                        </div>
                        <div class="col">
                            <input @input="cambiar_tipo()" value="historico" v-model="periodo" class="form-check-input" style="float:left;margin-right:10px" type="radio">
                            <label  class="form-check-label" style="float:left"  for="radioSatisfaccion">Histórico</label>
                        </div>
                    </div>
                    <div id="institucion-dimension">

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
                elementId: 'institucion-dimension',
                tipo_grafico: 'barra_horizontal',
                medicion: 'atributos',
                periodo: 'historico',
                ultimo_anio: this.institucion.datos.anios[this.institucion.datos.anios.length - 1]
            },

        }
    },
    methods: {
        subtitle () {
            if (this.config.medicion === 'atributos') {
                return 'Evaluación atributos de experiencia'
            }
            if (this.config.medicion === 'imagen') {
                return 'Dimensiones de la imagen de la Institución'
            }
        },

        cambiar_medicion (medicion) {
            this.config.medicion = medicion
            this.cambiar_local()
        },
        cambiar_local () {
            this.cambiar(this.config)
        }

    },

    mounted () {
        this.cambiar_local()
    }
}
</script>
