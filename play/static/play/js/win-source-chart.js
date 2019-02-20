var winSourceChartCtx = document.getElementById('winSourceChart').getContext('2d');
var winSourceChart = {};

["Straight flush", "Four of a kind", "Full house", "Flush", "Straight", "Three of a kind", "Two pair", "Pair", "High card"]

function buildWinSourceChart(wins, total_wins) {
    console.log(wins);
    winSourceChart = new Chart(winSourceChartCtx, {
        // The type of chart we want to create
        type: 'horizontalBar',

        // The data for our dataset
        data: {
            labels: ["Wins"],
            datasets: [{
                label: "High card",
                stack: "High card",
                backgroundColor: '#A6BFCC',
                data: [wins[8]],
            },
            {
                label: "Pair",
                stack: "Pair",
                backgroundColor: '#2A3948',
                data: [wins[7]],
            },
            {
                label: "Two pair",
                stack: "Two pair",
                backgroundColor: '#32668F',
                data: [wins[6]],
            },
            {
                label: "Three of a kind",
                stack: "Three of a kind",
                backgroundColor: '#D2C2AB',
                data: [wins[5]],
            },
            {
                label: "Straight",
                stack: "Straight",
                backgroundColor: '#9C9378',
                data: [wins[4]],
            },
            {
                label: "Flush",
                stack: "Flush",
                backgroundColor: '#D78852',
                data: [wins[3]],
            },  
            {
                label: "Full house",
                stack: "Full house",
                backgroundColor: '#736C55',
                data: [wins[2]],
            },
            {
                label: "Four of a kind",
                stack: "Four of a kind",
                backgroundColor: '#D5BD6F',
                data: [wins[1]],
            },
            {
                label: "Straight flush",
                stack: "Straight flush",
                backgroundColor: '#F3D199',
                data: [wins[0]],
            }]
        },

        // Configuration options go here
        options: {
            legend: {
                display: false
            },
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
                    },
                    afterFit: function(scaleInstance) {
                        scaleInstance.width = 100; // sets the width to 100px
                    }
                }]
            }
        }
    })
    winChart.update();
    }