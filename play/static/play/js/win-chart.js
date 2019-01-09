var winChartCtx = document.getElementById('winChart').getContext('2d');

var winChart = {};

function buildWinChart(wins, losses, ties) {
    winChart = new Chart(winChartCtx, {
        // The type of chart we want to create
        type: 'horizontalBar',

        // The data for our dataset
        data: {
            labels: ["Outcomes"],
            datasets: [{
                label: "wins",
                stack: "wins",
                backgroundColor: '#A6BFCC',
                data: [wins],
            },
            {
                label: "losses",
                stack: "losses",
                backgroundColor: '#2A3948',
                data: [losses],
            },
            {
                label: "ties",
                stack: "ties",
                backgroundColor: '#32668F',
                data: [ties],
            }]
        },

        // Configuration options go here
        options: {
            scales: {
                xAxes: [{
                    stacked: true,
                    gridLines: {
                        display: false
                    }
                }],
                yAxes: [{
                    stacked: true,
                    gridLines: {
                        display: false
                    }
                }]
            }
        }
    })
    winChart.update();
    }