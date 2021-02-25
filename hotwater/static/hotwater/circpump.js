

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
            },]
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
                label: 'RUN',
                borderColor: 'orange',
                fill: false,
                pointRadius: 0,
                data: [],
            },]
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
                        suggestedMin: 0,
                        suggestedMax: 1,
                        stepSize: 1
                    },
                    scaleLabel: {
                        display: true,
                        labelString: 'on/off'
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

    this.pumpTarget = document.getElementById(pump_div);
    this.pumpVal = false;

    var ctx = document.getElementById(temp_chart_div).getContext('2d');
    this.tempChart = new Chart(ctx, this.tempChartConfig);
    ctx = document.getElementById(pump_chart_div).getContext('2d');
    this.pumpChart = new Chart(ctx, this.pumpChartConfig);

    this.updateData = function(adata, shift) {
        let sindata = adata['data']['sensor']['data']
        let spumpdata = adata['data']['relay']['data']
        const scount = adata['data']['sensor']['count'];
        const pcount = adata['data']['relay']['count'];
        if (scount > 0) {
            this.gaugeIn.value = sindata[0]['attributes']['value'];
        }
        if (pcount > 0) {
            this.pumpVal = spumpdata[0]['attributes']['value'];
        }

        // reverse load
        for (let i = scount - 1; i >= 0; i--) {
            this.tempChart.data.datasets[0].data.push({
                t: sindata[i]['attributes']['timestamp'] - offset,
                y: sindata[i]['attributes']['value']
            });
        }
        for (let i = pcount - 1; i >= 0; i--) {
            this.pumpChart.data.datasets[0].data.push({
                    t: spumpdata[i]['attributes']['timestamp'] - offset,
                    y: spumpdata[i]['attributes']['value']
            });
        }
        if (shift) {
            // remove extras
            for (let i = 0; i < this.tempChart.data.datasets[0].data.length - 9000; i++) {
                this.tempChart.data.datasets[0].data.shift();
            }
            for (let i = 0; i < this.pumpChart.data.datasets[0].data.length - 9000; i++) {
                this.pumpChart.data.datasets[0].data.shift();
            }
        }
    };

    this.draw = function () {
        this.gaugeIn.draw();
        let newcls = 'circpump-stop';;
        // if pumpVal = true spin
        if (this.pumpVal) {
            // change class to circpump-run
            newcls = 'circpump-run';
        }
        this.pumpTarget.className = newcls;
        this.tempChart.update();
        this.pumpChart.update();
    };
}


