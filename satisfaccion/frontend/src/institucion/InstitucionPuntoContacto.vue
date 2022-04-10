<template>
    <div style="padding-top:40px">
        <canvas id="institucion-punto-contacto"></canvas>
        <p class="text-center mt-4">Evaluación canales de atención utilizados<br>Porcentaje de personas satisfechas <span title="Evaluación positiva (nota 6 y 7)" class="tooltip-info">
            <font-awesome-icon icon="info-circle" />
        </span></p>
    </div>

</template>

<script>
import Chart from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

export default {
    name: 'HistoricChart',
    props: ['institucion'],
    data () {
        return {
            indicador: 'satisfaccion'
        }
    },
    methods: {
        cambiar_tipo (tipo) {
            this.draw(9)
        },
        draw () {
            this.data = {
                type: 'bar',
                data: {
                    labels: ['Web', 'Callcenter', 'Oficinas'],
                    datasets: [
                        {
                            data: [
                                this.institucion.resumen.canales.Web.positivo,
                                this.institucion.resumen.canales.Callcenter.positivo,
                                this.institucion.resumen.canales.Oficinas.positivo],
                            backgroundColor: ['#485FC7', '#F96854', '#ED3945'],
                        }
                    ]
                }
            }
            var chartOptions = {
                tooltips: {
                    // enabled: false
                },
                legend: {
                    display: false
                },
                plugins: {
                    datalabels: {
                        color: 'white',
                        font: {
                            size: 14,
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

                    // gridLines: { display: true, drawBorder: true, drawOnChartArea: false, color: 'blue' }
                    }],
                    // yAxes: [
                    //     {
                    //         // display: false,
                    //         ticks: {
                    //             beginAtZero: true,
                    //             stepSize: 25,
                    //             min: 0,
                    //             max: 100,
                    //             fontFamily: 'Roboto',
                    //             fontColor: '#272727',
                    //             fontSize: '12',
                    //             callback: function (label, index, labels) {
                    //                 return label + '%'
                    //             }
                    //         },

                    //     // gridLines: { display: true, drawBorder: true, drawOnChartArea: false, color: 'blue' }
                    //     }],
                    xAxes: [{
                        stacked: true,
                        ticks: {
                            fontFamily: 'Roboto',
                            fontColor: '#272727',
                            fontSize: '12'
                        },
                        gridLines: { display: false },

                    }]
                    // xAxes: [{
                    //     ticks: {
                    //         fontFamily: 'Roboto',
                    //         fontColor: '#272727',
                    //         fontSize: '12'
                    //     },
                    //     gridLines: { display: false },
                    // // scaleLabel: {
                    // //     fontColor: 'white'
                    // // }
                    // }]
                },
            // responsive: true,
            // maintainAspectRatio: true,
            // title: {
            //     display: false,
            //     fontColor: 'black',
            //     fontFamily: ' Roboto',
            //     fontSize: '12'
            // }
            }
            Chart.plugins.register(ChartDataLabels)

            this.data.options = chartOptions
            const ctx = document.getElementById('institucion-punto-contacto')
            var mychart = new Chart(ctx, this.data, {
                responsive: true,
                maintainAspectRatio: false
            })
            mychart.draw()
        }
    },

    mounted () {
        this.draw()
    }
}
</script>
