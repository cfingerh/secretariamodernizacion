export const stackedBarOptions = {
    tooltips: {
        // enabled: false
    },
    legend: {
        // display: false
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
            align: 'center',
            formatter: function (value, context) {
                return Math.round(value * 10) / 10 + ' %'
            }
        }
    },
    scales: {
        yAxes: [
            {
                stacked: true,
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
            }
        ],

        xAxes: [
            {
                stacked: true,
                ticks: {
                    fontFamily: 'Roboto',
                    fontColor: '#272727',
                    fontSize: '12'
                },
                gridLines: { display: false },
            }
        ]
    },
}
