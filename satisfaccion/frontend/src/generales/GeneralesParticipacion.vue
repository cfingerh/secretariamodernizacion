<template>

    <div class="ficha">
        <div class="chart__body">
            <!-- <canvas id="generales-canal"></canvas> -->
            <img src="img/hemos-crecido-2021.svg" alt="trimestres" class="metodologia_2--img" >
        </div>
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
            this.draw()
        },

        draw () {
            // var colors = ['#485FC7', '#00D1B2']
            var factor = 1.3
            this.data = {
                type: 'bubble',
                data: {
                    datasets: [
                        {
                            label: 'First Dataset',
                            data: [{ x: 2021, y: 62 / 2, r: 62 * factor }],
                            backgroundColor: 'rgb(255, 99, 132,1)'
                        },
                        {
                            label: 'First Dataset',
                            data: [{ x: 2020, y: 49 / 2, r: 49 * factor }],
                            backgroundColor: 'rgb(255, 99, 132,0.9)'
                        },
                        {
                            label: 'First Dataset',
                            data: [{ x: 2019, y: 33 / 2, r: 33 * factor }],
                            backgroundColor: 'rgb(255, 99, 132,0.8)'
                        },
                        {
                            label: 'First Dataset',
                            data: [{ x: 2018, y: 9 / 2, r: 9 * factor }],
                            backgroundColor: 'rgb(255, 99, 132,0.7)'
                        },
                        {
                            label: 'First Dataset',
                            data: [{ x: 2017, y: 5 / 2, r: 5 * factor }],
                            backgroundColor: 'rgb(255, 99, 132,0.6)'
                        }
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
                        anchor: 'center',
                        font: {
                            size: 14,
                            weight: 600
                        },
                        offset: -10,
                        formatter: function (value, context) {
                            return Math.round(value.y * 2)
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
                                max: 75,
                                fontFamily: 'Roboto',
                                fontColor: '#272727',
                                fontSize: '12'

                            },

                        }],
                    xAxes: [{
                        ticks: {
                            min: 2017,
                            max: 2022,
                            stepSize: 1,
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

            }
            Chart.plugins.register(ChartDataLabels)

            this.data.options = chartOptions
            const ctx = document.getElementById('generales-canal')
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
