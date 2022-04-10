<template>

    <div class="ficha">
        <div class="chart__header">
            <h2>Canales evaluados</h2>
        </div>
        <div class="chart__body">
            <div class="row">
                <div class="col-12 col-md-4 ajustado">
                    <div class="group-links">
                        <a class="ficha-selector-medicion"  v-bind:class="{ active: config.medicion==='evaluacion' }"  @click="cambiar_medicion('evaluacion')">
                            Evaluación global por tipo de canal
                            <span title="Tooltip" class="tooltip">
                                <font-awesome-icon icon="info-circle" />
                            </span>
                            <span style="float:right">
                                <font-awesome-icon icon="chevron-right"/>
                                </span>
                        </a>
                        <a class="ficha-selector-medicion"  v-bind:class="{ active: config.medicion==='preferencia' }" @click="cambiar_medicion('preferencia')">
                            Preferencia de uso de canal
                            <span title="Tooltip" class="tooltip">
                                <font-awesome-icon icon="info-circle" />
                            </span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right" /></span>
                        </a>
                        <!-- <a class="ficha-selector-medicion"  v-bind:class="{ active: config.medicion==='internet' }" @click="cambiar_medicion('internet')">
                            Frecuencia en el uso de internet
                            <span title="Tooltip" class="tooltip">
                                <font-awesome-icon icon="info-circle" />
                            </span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right" /></span>
                        </a> -->
                    </div>
                </div>
                <div class="col-12 col-md-8 ajustado derecha">
                    <h5>{{subtitle()}}</h5>
                    <h6>Año 2020</h6>
                    <div id="general-canal"></div>
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
                elementId: 'general-canal',
                tipo_grafico: 'canal_evaluacion',
                medicion: 'evaluacion',
                periodo: 'ultimo',

            },
        }
    },
    methods: {
        subtitle () {
            if (this.config.medicion === 'evaluacion') {
                return 'Evaluación global por tipo de canal'
            }
            if (this.config.medicion === 'preferencia') {
                return 'Preferencia de uso de canal'
            }
        },
        cambiar_medicion (medicion) {
            this.config.medicion = medicion
            if (this.config.medicion === 'evaluacion') {
                this.config.tipo_grafico = 'canal_evaluacion'
            }
            if (this.config.medicion === 'preferencia') {
                this.config.tipo_grafico = 'canal_preferencia'
            }
            this.cambiar(this.config)
        },
    },

    mounted () {
        this.cambiar(this.config)
    }
}
</script>
