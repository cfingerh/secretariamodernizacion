<template>
  <div>
    <canvas :id="'canal-chart'+institucion.id"></canvas>
  </div>
</template>

<script>
import Chart from 'chart.js'

export default {
    name: 'CanalChart',
    props: ['institucion'],
    data () {
        return {
            data: null,
            datos: this.institucion.datos
        }
    },
    mounted () {
        var labels = []
        var data = []
        if (this.datos.satisfactioncall_positive) {
            labels.push('Call Center')
            data.push(this.datos.satisfactioncall_positive)
        }
        if (this.datos.satisfactionweb_positive) {
            labels.push('Web')
            data.push(this.datos.satisfactionweb_positive)
        }
        if (this.datos.satisfactionpres_positive) {
            labels.push('Oficina')
            data.push(this.datos.satisfactionpres_positive)
        }

        this.data = {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [
                    {
                        data: data,
                        backgroundColor: 'rgba(54,73,93,.5)',
                        borderColor: '#36495d',
                        borderWidth: 3
                    },
                ]
            },
            options: {
                responsive: true,
                lineTension: 1,
                scales: {
                    yAxes: [
                        {
                            ticks: {
                                beginAtZero: true,
                                padding: 25
                            }
                        }
                    ]
                }
            }
        }
        var chartOptions = {
            legend: {
                display: false
            },
            // tooltips: {
            //     enabled: true
            // },
            // steppedLine: false,
            scales: {
                yAxes: [
                    {
                        // display: false,
                        ticks: {
                            beginAtZero: true,
                            stepSize: 50,
                            // min: 0,
                            max: 100,
                            // fontFamily: 'Roboto',
                            //     fontColor: 'blue',
                            // fontSize: '16'
                        },
                        // gridLines: { display: true, drawBorder: true, drawOnChartArea: false, color: 'blue' }
                    }],
                xAxes: [{
                    // ticks: {
                    //     fontFamily: ' Roboto',
                    //     fontColor: 'black',
                    //     fontSize: '16'
                    // },
                    gridLines: { display: true },
                    // scaleLabel: {
                    //     fontColor: 'white'
                    // }
                }]
            },
            // responsive: true,
            // maintainAspectRatio: true,
            title: {
                display: false,
                fontColor: 'black',
                fontFamily: ' Roboto',
                fontSize: '16'
            }
        }

        this.data.options = chartOptions
        const ctx = document.getElementById('canal-chart' + this.institucion.id)
        var mychart = new Chart(ctx, this.data)
        console.log(mychart)
    }
}
</script>
