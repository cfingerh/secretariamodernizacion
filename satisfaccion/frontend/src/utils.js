import axios from 'axios'
// import _ from 'lodash'
import { stackedBarOptions } from '@/options/stackedBar.js'
import Chart from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'
// import { concat } from 'lodash'

export const utils = {
    components: {},
    data () {
        return {
            stackedBarOptions: stackedBarOptions,
            tipo: null,
            mostrar: true,
            periodo: 'historico'
        }
    },
    created: function () { },
    mounted () {
    },
    methods: {

        sin_info (elementId) {
            const ctx = document.getElementById(elementId)
            console.log(ctx)
            if (ctx.children.length > 0) {
                ctx.removeChild(ctx.children[0])
            }
            var div = document.createElement('div')
            div.innerText = 'Sin Información'
            ctx.appendChild(div)
        },

        cambiar (config) {
            const ctx = document.getElementById(config.elementId)
            if (ctx.children.length > 0) {
                ctx.removeChild(ctx.children[0])
            }
            var div = document.createElement('div')
            div.innerText = 'Cargando'
            ctx.appendChild(div)

            var institucionCodigoDipres = this.$route.params.id || ''

            this.medicion = config.medicion
            config.filtro = config.filtro || {}
            config.filtro.medicion = this.medicion

            if (config.tipo_grafico === 'linea_tipo') {
                config.filtro.dimension = config.grupo
                var chartConfig = {}
                axios.get('/api/data_dimension_anio/' +
                institucionCodigoDipres, { params: config.filtro }).then(res => {
                    if (res.data.labels.length === 1) {
                        chartConfig = {
                            type: 'bar',
                            data: {
                                labels: res.data.labels,
                                datasets: res.data.datasets
                            }
                        }
                        this.draw_barra_tipo(config.elementId, chartConfig)
                    } else {
                        chartConfig = {
                            type: 'line',
                            data: {
                                labels: res.data.labels,
                                datasets: res.data.datasets
                            }
                        }
                        this.draw_linea(config.elementId, chartConfig)
                    }
                })
            }

            if (config.tipo_grafico === 'barra') {
                axios.get('/api/data_grafica/' + institucionCodigoDipres, { params: config.filtro }).then(res => {
                    var chartConfig = {
                        type: 'bar',
                        data: {
                            labels: res.data.labels,
                            datasets:
                                [
                                    {
                                        label: 'Satisfecho',
                                        data: res.data.data.satisfecho,
                                        backgroundColor: '#00d1b2',
                                    },
                                    {
                                        label: 'Neutro',
                                        data: res.data.data.neutro,
                                        backgroundColor: '#FBD561',
                                    },
                                    {
                                        label: 'Insatisfechos',
                                        data: res.data.data.insatisfecho,
                                        backgroundColor: '#ED3945',
                                    },

                                ]
                        }
                    }
                    this.draw_barra(config.elementId, chartConfig)
                })
            }
        },

        draw_barra_horizontal (elementId, chartConfig) {
            var chartOptions = {
                tooltips: {
                    enabled: false
                },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    datalabels: {
                        color: 'white',

                        font: {
                            size: 14,
                            weight: 600
                        },
                        formatter: function (value, context) {
                            return Math.round(value * 10) / 10 + ' %'
                        }
                    }
                },
                scales: {
                    xAxes: [
                        {
                            scaleLabel: {
                                display: true,
                                labelString: '% usuarios'
                            },
                            ticks: {
                                beginAtZero: true,
                                stepSize: 25,
                                min: 0,
                                max: 100,
                                fontFamily: 'Roboto',
                                fontColor: '#272727',
                                fontSize: '12',
                                callback: function (label, index, labels) {
                                    return label + '%'
                                }
                            },
                        }],
                    yAxes: [{
                        ticks: {
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12',
                            callback: function (label, index, labels) {
                                return label
                            }

                        },
                        gridLines: { display: false },
                    }]
                }
            }
            Chart.plugins.register(ChartDataLabels)

            chartConfig.options = chartOptions
            const ctx = document.getElementById(elementId)
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            var canvas = document.createElement('canvas')
            ctx.appendChild(canvas)
            var mychart = new Chart(canvas, chartConfig, {
                responsive: true,
                maintainAspectRatio: false
            })
            mychart.draw()
        },

        get_font_size () {
            return Math.sqrt(window.innerWidth) / 3 + 2
        },

        draw_barra (elementId, chartConfig) {
            var chartOptions = {
                tooltips: { },
                legend: { align: 'start' },
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    datalabels: {
                        color: 'white',
                        font: {
                            size: this.get_font_size(),
                            weight: 600
                        },
                        align: 'center',
                        formatter: function (value, context) {
                            return Math.round(value * 10) / 10 + ' %'
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        stacked: true,
                        scaleLabel: {
                            display: true,
                            labelString: '% usuarios'
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 25,
                            min: 0,
                            max: 100,
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12',
                            callback: function (label, index, labels) {
                                return label + '%'
                            }
                        },

                    }],
                    xAxes: [{
                        stacked: true,
                        ticks: {
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12'
                        },
                        gridLines: { display: false },

                    }]
                },

            }
            Chart.plugins.register(ChartDataLabels)

            chartConfig.options = chartOptions
            const ctx = document.getElementById(elementId)
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            var canvas = document.createElement('canvas')
            canvas.style.height = '300px'
            chartConfig.options.maintainAspectRatio = false
            console.log(chartConfig)
            ctx.appendChild(canvas)
            var mychart = new Chart(canvas, chartConfig, {
                responsive: true,
                maintainAspectRatio: false
            })
            mychart.draw()
        },

        draw_barra_tipo (elementId, chartConfig) {
            var chartOptions = {
                tooltips: {},
                legend: { align: 'start' },
                plugins: {
                    legend: { position: 'top', },
                    datalabels: {
                        // color: 'white',
                        font: { size: 14, weight: 600 },
                        // align: 'center',
                        formatter: function (value, context) {
                            return ''
                            // Math.round(value * 10) / 10 + ' %'
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        stacked: false,
                        scaleLabel: {
                            display: true,
                            labelString: '% usuarios'
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 25,
                            // min: 0,
                            // max: 100,
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12',
                            callback: function (label, index, labels) {
                                return label + '%'
                            }
                        },

                    }],
                    xAxes: [{
                        stacked: false,
                        ticks: {
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12'
                        },
                        gridLines: { display: false },

                    }]
                },

            }
            Chart.plugins.register(ChartDataLabels)

            chartConfig.options = chartOptions
            const ctx = document.getElementById(elementId)
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            var canvas = document.createElement('canvas')
            canvas.style.height = '300px'
            chartConfig.options.maintainAspectRatio = false
            ctx.appendChild(canvas)
            var mychart = new Chart(canvas, chartConfig, {
                responsive: true,
                maintainAspectRatio: false
            })
            mychart.draw()
        },

        draw_linea (elementId, chartConfig) {
            var chartOptions = {
                tooltips: {},
                legend: { align: 'start' },
                plugins: {
                    legend: { position: 'top' },
                    datalabels: {
                        // color: 'white',
                        font: { size: 14, weight: 600 },
                        // align: 'center',
                        formatter: function (value, context) {
                            return ''
                            // Math.round(value * 10) / 10 + ' %'
                        }
                    }
                },
                scales: {
                    yAxes: [{
                        stacked: false,
                        scaleLabel: {
                            display: true,
                            labelString: '% usuarios'
                        },
                        ticks: {
                            beginAtZero: true,
                            stepSize: 25,
                            // min: 0,
                            // max: 100,
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12',
                            callback: function (label, index, labels) {
                                return label + '%'
                            }
                        },

                    }],
                    xAxes: [{
                        stacked: false,
                        ticks: {
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12'
                        },
                        gridLines: { display: false },

                    }]
                },

            }
            Chart.plugins.register(ChartDataLabels)

            chartConfig.options = chartOptions
            const ctx = document.getElementById(elementId)
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            if (ctx.childNodes.length > 0) { ctx.removeChild(ctx.childNodes[0]) }
            var canvas = document.createElement('canvas')
            canvas.style.height = '300px'
            chartConfig.options.maintainAspectRatio = false
            ctx.appendChild(canvas)
            var mychart = new Chart(canvas, chartConfig, {
                responsive: true,
                maintainAspectRatio: false
            })
            mychart.draw()
        },

        label_to_name (label) {
            if (label === 'pi_imagen_confianza') { return 'Confianza' }
            if (label === 'pi_imagen_transp') { return 'Transparente' }
            if (label === 'pi_imagen_preocupa') { return 'Preocupación por usuarios' }
            if (label === 'pi_imagen_actual') { return 'Actualización y modernización' }
            if (label === 'pi_imagen_funcion') { return 'Funcionarios comprometidos' }
            if (label === 'pi_imagen_satisface') { return 'Satisface a usuarios' }

            if (label === 'pev_tram_facil') { return 'Facilidad para realizarlo' }
            if (label === 'pev_tram_tiempo') { return 'Tiempo de respuesta' }
            if (label === 'pev_tram_claridad_pasos') { return 'Claridad de los pasos a seguir' }
            if (label === 'pev_tram_info_compr') { return 'Lo comprensible de la información' }
            if (label === 'pev_tram_info_util') { return 'Utilidad de la información para el trámite' }
            if (label === 'pev_tram_resp_util') { return 'Respuesta útil' }
            if (label === 'pev_tram_resp_compl') { return 'Respuesta completa' }
            if (label === 'pev_tram_resp_clara') { return 'Claridad del resultado' }
            if (label === 'pev_tram_acogido') { return 'Esfuerzo por acogerme' }

            if (label === 'pec_eval_telefono') { return 'Callcenter' }
            if (label === 'pec_eval_web') { return 'Web' }
            if (label === 'pec_eval_presencial') { return 'Oficina' }
            if (label === 'pec_canal_telefono') { return 'Callcenter' }
            if (label === 'pec_canal_web') { return 'Web' }
            if (label === 'pec_canal_presencial') { return 'Oficina' }

            return label
        },

        labels_to_names (arreglo) {
            return arreglo.map(a => { return this.label_to_name(a) })
        },

        /// ////////// OLD ///////////
        // cambiar_tipo (tipo) {
        //     this.tipo = tipo || this.tipo
        //     this.mostrar = false
        //     setTimeout(() => {
        //         this.draw(); this.mostrar = true
        //     }, 500)
        // },

    }
}
