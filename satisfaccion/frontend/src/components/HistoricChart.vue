<template>
    <div style="padding:10px">
        <canvas :id="'historic-chart'+institucion.id"></canvas>
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
            data: null,
            datos: null
        }
    },
    mounted () {
        var datos = this.institucion.datos
        var satisfacciones = this.institucion.resumen.satisfaciones
        var valores = [null, null, null, null]
        var years = ['', '', '', '']
        datos.anios.forEach(function (y, b) {
            if (y === 2017) { valores[0] = satisfacciones[b] }
            if (y === 2018) { valores[1] = satisfacciones[b] }
            if (y === 2019) { valores[2] = satisfacciones[b] }
            if (y === 2020) { valores[3] = satisfacciones[b] }
            if (y === 2021) { valores[4] = satisfacciones[b] }

            if (y === 2017) { years[0] = 2017 }
            if (y === 2018) { years[1] = 2018 }
            if (y === 2019) { years[2] = 2019 }
            if (y === 2020) { years[3] = 2020 }
            if (y === 2020) { years[4] = 2021 }
        })
        this.data = {
            type: 'bar',
            data: {
                labels: years,
                datasets: [
                    {
                        data: valores,
                        backgroundColor: '#0F69C4',
                        borderColor: '#0F69C4',
                        borderWidth: 3
                    },
                ]
            },
            options: {

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
                    font: {
                        size: 10,
                        weight: 600
                    },
                    align: 'bottom',
                    anchor: 'end',
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
                            fontSize: '10',
                            callback: function (label, index, labels) {
                                return label + '%'
                            }
                        },

                        // gridLines: { display: true, drawBorder: true, drawOnChartArea: false, color: 'blue' }
                    }],
                xAxes: [{
                    ticks: {
                        fontFamily: 'Roboto',
                        fontColor: '#272727',
                        fontSize: '12'
                    },
                    gridLines: { display: false },
                    // scaleLabel: {
                    //     fontColor: 'white'
                    // }
                }]
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
        const ctx = document.getElementById('historic-chart' + this.institucion.id)
        var mychart = new Chart(ctx, this.data, {
            responsive: true,
            maintainAspectRatio: false
        })
        mychart.draw()
    }
}
</script>
