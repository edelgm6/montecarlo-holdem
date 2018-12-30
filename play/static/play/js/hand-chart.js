var ctx = document.getElementById('myChart').getContext('2d');

var handsChart = {};


function buildHandsChart(wins, losses, ties) {
    handsChart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'horizontalBar',

        // The data for our dataset
        data: {
            labels: ["Straight flush", "Four of a kind", "Full house", "Flush", "Straight", "Three of a kind", "Two pair", "Pair", "High card"],
            datasets: [{
                label: "wins",
                stack: "wins",
                backgroundColor: '#A6BFCC',
                data: wins,
            },
            {
                label: "losses",
                stack: "losses",
                backgroundColor: '#2A3948',
                data: losses,
            },
            {
                label: "ties",
                stack: "ties",
                backgroundColor: '#32668F',
                data: ties,
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
    handsChart.update();
    }