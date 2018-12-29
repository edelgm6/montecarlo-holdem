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
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: wins,
            },
            {
                label: "losses",
                stack: "losses",
                backgroundColor: 'rgb(0, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: losses,
            },
            {
                label: "ties",
                stack: "ties",
                backgroundColor: 'rgb(0, 0, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: ties,
            }]
        },

        // Configuration options go here
        options: {
            scales: {
                xAxes: [{
                    stacked: true
                }],
                yAxes: [{
                    stacked: true
                }]
            }
        }
    })
    handsChart.update();
    }