
function CircPump(name, in_div, pump_div, temp_chart_div, pump_chart_div) {
    this.name = name;
    this.tempChartConfig = {
        type: 'line',
        data: {
            datasets: [{
                label: 'IN',
                borderColor: 'orange',
                fill: false,
                pointRadius: 0,
                data: [],
            }, {
                label: 'OUT',
                borderColor: 'skyblue',
                fill: false,
                pointRadius: 0,
                data: [],
            }, {
                label: 'BURN',
                borderColor: 'red',
                fill: false,
                pointRadius: 0,
                data: [],
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    type: 'time',
                    ticks: {
                        stepSize: 10
                    },
                    time: {
                        unit: 'minute',
                        displayFormats: {minute: 'MM-DD HH:mm'}
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    ticks: {
                        suggestedMin: 30,
                        suggestedMax: 180,
                        stepSize: 30
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'temp'
                    }
                }]
            },
        }
    };
    this.pumpChartConfig = {
        type: 'line',
        data: {
            datasets: [{
                label: 'IN',
                borderColor: 'orange',
                fill: false,
                pointRadius: 0,
                data: [],
            }, {
                label: 'OUT',
                borderColor: 'skyblue',
                fill: false,
                pointRadius: 0,
                data: [],
            }, {
                label: 'BURN',
                borderColor: 'red',
                fill: false,
                pointRadius: 0,
                data: [],
            }]
        },
        options: {
            maintainAspectRatio: false,
            scales: {
                xAxes: [{
                    type: 'time',
                    ticks: {
                        stepSize: 10
                    },
                    time: {
                        unit: 'minute',
                        displayFormats: {minute: 'MM-DD HH:mm'}
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
                yAxes: [{
                    ticks: {
                        suggestedMin: 30,
                        suggestedMax: 180,
                        stepSize: 30
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'temp'
                    }
                }]
            },
        }
    };

    this.gaugeIn = new RadialGauge({
        renderTo: in_div,
        title: 'IN',
        width: 200, height: 200,
        units: 'F', minValue: 30, maxValue: 180,
        majorTicks: ['30', '60', '90', '120', '150', '180'],
        minorTicks: 6,
        highlights: [{from: 30, to: 60, color: 'skyblue'},
            {from: 60, to: 90, color: 'aliceblue'},
            {from: 90, to: 120, color: 'yellow'},
            {from: 120, to: 150, color: 'orange'},
            {from: 150, to: 180, color: 'red'}
        ],
        valueBox: true,
        value: 30
    });

    this.spinnerPump = pump_div;

    var ctx = document.getElementById(temp_chart_div).getContext('2d');
    this.tempChart = new Chart(ctx, this.chartConfig);
    ctx = document.getElementById(pump_chart_div).getContext('2d');
    this.pumpChart = new Chart(ctx, this.chartConfig);

    this.updateData = function(adata, shift) {
        let sindata = adata['data']['sensor']['data']
        let spumpdata = adata['data']['relay']['data']
        let numpts = adata['data']['sensor_in']['count'];
        if (numpts > 0) {
            this.gaugeIn.value = sindata[0]['attributes']['value'];
            this.gaugeOut.value = soutdata[0]['attributes']['value'];
            this.gaugeBurn.value = sburndata[0]['attributes']['value'];
            // reverse load
            for (let i = numpts - 1; i >= 0; i--) {
                this.lineChart.data.datasets[0].data.push({
                    t: sindata[i]['attributes']['timestamp'] - offset,
                    y: sindata[i]['attributes']['value']
                });
                this.lineChart.data.datasets[1].data.push({
                    t: soutdata[i]['attributes']['timestamp'] - offset,
                    y: soutdata[i]['attributes']['value']
                });
                this.lineChart.data.datasets[2].data.push({
                    t: sburndata[i]['attributes']['timestamp'] - offset,
                    y: sburndata[i]['attributes']['value']
                });
            }
            if (shift) {
                // remove extras
                for (let i = 0; i < this.lineChart.data.datasets[0].data.length - 9000; i++) {
                    this.lineChart.data.datasets[0].data.shift();
                    this.lineChart.data.datasets[1].data.shift();
                    this.lineChart.data.datasets[2].data.shift();
                }
            }
        }
    };
    this.draw = function () {
        this.gaugeIn.draw();
        this.gaugeOut.draw();
        this.gaugeBurn.draw();
        this.lineChart.update();
    };
}

