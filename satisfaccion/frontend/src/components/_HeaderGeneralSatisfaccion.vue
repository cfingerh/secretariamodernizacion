<template>
    <div>
        <!-- <canvas id="header-general-satisfaccion"></canvas> -->
        <img src="img/ultima-experiencia.svg" alt="trimestres" class="metodologia_2--img">
    </div>
</template>

<script>
import Chart from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

export default {
    name: 'HeaderGeneralSatisfaccion',
    props: ['institucion'],
    data () {
        return {
            data: null,
            datos: null
        }
    },
    mounted () {
        this.data = {
            type: 'bar',
            data: {
                labels: ['Insatisfechos', 'Neutros', 'Satisfechos'],
                datasets: [
                    {
                        label: '2019',
                        data: [22, 16, 62],
                        backgroundColor: [
                            '#f14668',
                            '#ffe08a',
                            '#00d1b2',

                        ]
                    },
                    {
                        label: '2020',
                        data: [29, 15, 57],
                        backgroundColor: [
                            '#f14668',
                            '#ffe08a',
                            '#00d1b2',
                        ],
                    },

                ]
            }
        }

        var chartOptions = {
            tooltips: {
                enabled: false
            },
            legend: {
                display: false
            },
            plugins: {
                datalabels: {
                    color: 'white',
                    align: 'bottom',
                    anchor: 'end',
                    font: {
                        size: 14,
                        weight: 600
                    },
                    offset: 10,
                    formatter: function (value, context) {
                        return Math.round(value * 10) / 10 + ' %'
                    }
                }
            },
            scales: {
                yAxes: [
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
                xAxes: [{

                    ticks: {
                        padding: 15,
                        fontFamily: 'Roboto',
                        fontColor: '#272727',
                        fontSize: '12',
                        callback: function (label, index, labels) {
                            return label + '%'
                        }

                    },
                    gridLines: { display: false },
                }]
            },
            animation: {
                onComplete: function () {
                    var chartInstance = this.chart
                    var ctx = chartInstance.ctx

                    ctx.font = Chart.helpers.fontString(Chart.defaults.global.defaultFontSize, Chart.defaults.global.defaultFontStyle, Chart.defaults.global.defaultFontFamily)

                    ctx.fillStyle = '#757575'

                    ctx.textAlign = 'center'
                    ctx.textBaseline = 'top'
                    this.data.datasets.forEach(function (dataset, i) {
                        var meta = chartInstance.controller.getDatasetMeta(i)
                        meta.data.forEach(function (bar, index) {
                            console.log(dataset)
                            // var data = dataset.data[index]
                            // ctx.fillText(data, bar._model.x, bar._model.y - 5)
                            // console.log(bar._model.y + 55)
                            // console.log(bar._chart.chartArea.bottom)
                            ctx.fillText(dataset.label, bar._model.x, bar._chart.chartArea.bottom + 3)
                        })
                    })
                }
            }
        }
        Chart.plugins.register(ChartDataLabels)

        this.data.options = chartOptions
        const ctx = document.getElementById('header-general-satisfaccion')
        var mychart = new Chart(ctx, this.data, {
            responsive: true,
            maintainAspectRatio: false
        })

        mychart.draw()
    }
}
</script>
