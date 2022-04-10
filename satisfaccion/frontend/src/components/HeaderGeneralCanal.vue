<template>
    <div>
        <canvas id="header-general-canal"></canvas>
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
    methods: {
        draw () {
            // var colors = ['#485FC7', '#00D1B2']
            this.data = {
                type: 'bar',
                data: {
                    labels: ['Teléfono', 'Digital', 'Presencial'],
                    datasets: [
                        {
                            label: '2019',
                            data: [24, 44, 44],
                            backgroundColor: '#485FC7'
                        },
                        {
                            label: '2020',
                            data: [61, 60, 29],
                            backgroundColor: '#00D1B2'
                        },

                    ]
                }
            }

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
                                return label
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
            const ctx = document.getElementById('header-general-canal')
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
