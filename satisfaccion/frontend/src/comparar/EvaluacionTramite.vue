<template>

    <div class="ficha">
        <div class="chart__header">
            <h2>Evaluación de la experiencia</h2>
        </div>
        <div class="chart__body">
            <div class="row">
                <div class="col col-5 ajustado">
                    <div class="group-links">
                        <a  class="ficha-selector-tipo"  v-bind:class="{ active: tipo==='tramite' }" @click="cambiar_tipo('tramite')">
                            Satisfacción por tipo de trámite
                            <span title="Tooltip" class="tooltip-info"><font-awesome-icon icon="info-circle" /></span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right"/></span>
                        </a>
                        <div v-if="tipo==='tramite'">
                            <div class="form-check" v-for="opcion in filtros[tipo]" v-bind:key="opcion.id">
                            <input @input="cambiar_tipo()" class="form-check-input" type="radio" :name="`tipoUsuario${tipo}`" :id="`tipoUsuario${tipo}`">
                            <label class="form-check-label" for="flexRadioDefault1">
                                {{opcion.nombre}}
                            </label>
                            </div>
                        </div>
                        <a class="ficha-selector-tipo"  v-bind:class="{ active: tipo==='geografica' }" @click="cambiar_tipo('geografica')">
                            Satisfacción por tipo de trámite por zona geográfica
                            <span title="Tooltip" class="tooltip-info"><font-awesome-icon icon="info-circle" /></span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right" /></span></a>
                        <div v-if="tipo==='geografica'">
                            <div class="form-check" v-for="opcion in filtros[tipo]" v-bind:key="opcion.id">
                            <input @input="cambiar_tipo()" class="form-check-input" type="radio" :name="`tipoUsuario${tipo}`" :id="`tipoUsuario${tipo}`">
                            <label class="form-check-label" for="flexRadioDefault1">
                                {{opcion.nombre}}
                            </label>
                            </div>
                        </div>
                        <a class="ficha-selector-tipo"  v-bind:class="{ active: tipo==='comparacion' }" @click="cambiar_tipo('comparacion')">
                            Satisfacción por nacionalidad
                            <span title="Tooltip" class="tooltip-info"><font-awesome-icon icon="info-circle" /></span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right" /></span></a>
                        <a class="ficha-selector-tipo"  v-bind:class="{ active: tipo==='tipo_institucion' }" @click="cambiar_tipo('tipo_institucion')">
                            Problema al realizar el trámite
                            <span title="Tooltip" class="tooltip-info"><font-awesome-icon icon="info-circle" /></span>
                            <span style="float:right"><font-awesome-icon icon="chevron-right" /></span></a>
                    </div>

                </div>
                <div class="col col-7 ajustado derecha">
                    <h5>Satisfacción por tipo de trámite</h5>
                    <canvas v-show="mostrar" id="comparar-evaluacion-tramite"></canvas>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import Chart from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'
import { utils } from '@/utils.js'

export default {
    name: 'HistoricChart',
    props: ['institucion'],
    mixins: [utils],
    data () {
        return {
            tipo: 'tramite',
            mostrar: true,
            myChart: null,
            periodo: 'historico',
            filtros:
                {
                    tramite: [
                        { id: 'beneficio', nombre: 'Beneficio/Apoyo' },
                        { id: 'consulta', nombre: 'Consulta/Solicitud de información' },
                        { id: 'obligacion_lega', nombre: 'Cumplimiento de obligaciones legales' },
                        { id: 'inscripcion', nombre: 'Inscripción/Certificado/Documentos' },
                    ],
                    geografica: [
                        { id: 'norte', nombre: 'Zona Norte' },
                        { id: 'centro', nombre: 'Zona Centro' },
                        { id: 'sur', nombre: 'Zona Sur' },
                        { id: 'metropolitana', nombre: 'Región Metropolitana' },

                    ]
                }
        }
    },
    methods: {
        subtitle () {
            if (this.tipo === 'satisfaccion') {
                return 'Evaluación atributos de experiencia'
            }
            if (this.tipo === 'evaluacion') {
                return 'Evaluación de la institución'
            }
            if (this.tipo === 'comparacion') {
                return 'Última experiencia versus evaluación de la institución'
            }
            if (this.tipo === 'tipo_institucion') {
                return 'Satisfacción por tipo de institución'
            }
            if (this.tipo === 'tipo_tramite') {
                return 'Satisfacción por tipo de trámite'
            }
        },

        draw () {
            this.data = this.get_fake_data()

            if (this.tipo === 'tipo_institucion') {
                this.data = this.get_fake_institucion()
            }
            if (this.tipo === 'tipo_tramite') {
                this.data = this.get_fake_tramite()
            }
            if (this.periodo === 'ultimo') {
                this.data = this.get_fake_data_last()
            }

            Chart.plugins.register(ChartDataLabels)
            console.log(this.stackedBarOptions)
            this.data.options = this.stackedBarOptions
            const ctx = document.getElementById('comparar-evaluacion-tramite')
            if (this.myChart) {
                this.myChart.data = this.data.data
                this.myChart.update()
            } else {
                this.mychart = new Chart(ctx, this.data, {
                    responsive: true,
                    maintainAspectRatio: false
                })
                this.mychart.draw()
            }
        }
    },

    mounted () {
        this.draw()
    }
}
</script>
