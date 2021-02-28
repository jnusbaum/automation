

function CircPump(name, in_div, pump_div, temp_chart_div, pump_chart_div, url, period) {
    this.name = name;
    this.url = url;
    this.period = period;

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

    this.offset = new Date().getTimezoneOffset() * 60 * 1000;

    // max data points to display in chart
    this.maxPoints = 9000;

    // dataset indices
    this.inIndex = 0;
    this.pumpIndex = 0;

    // last ts loaded
    this.lastLoaded;

    this.updateData = function(adata) {
        let sincount = adata['data']['sensor']['count'];
        let sindata = adata['data']['sensor']['data']
        if (sincount > 0) {
            // data comes in latest first
            this.gaugeIn.value = sindata[0]['attributes']['value'];
            let sinLen = 0;
            if (this.tempChart.data.datasets[this.inIndex].data.length > 0) {
                // already have data
                for (let i = sincount - 1; i >= 0; i--) {
                    sinLen = this.tempChart.data.datasets[this.inIndex].data.push({
                        t: sindata[i]['attributes']['timestamp'] - this.offset,
                        y: sindata[i]['attributes']['value']
                    });
                    if (sinLen > this.maxPoints) {
                        // remove extra
                        this.tempChart.data.datasets[this.inIndex].data.shift();
                    }
                }
            } else {
                // no data
                let sinLen = 0;
                for (let i = 0; i < sincount; i++) {
                    sinLen = this.tempChart.data.datasets[this.inIndex].data.unshift({
                        t: sindata[i]['attributes']['timestamp'] - this.offset,
                        y: sindata[i]['attributes']['value']
                    });
                }
                // guaranteed not to have more than maxPoints in the incoming data\
                // so no need to remove extras
            }
        }

        let pumpcount = adata['data']['relay']['count']
        let pumpdata = adata['data']['relay']['data']
        if (pumpcount > 0) {
            // data comes in latest first
            this.pumpVal = pumpdata[0]['attributes']['value'];
            let pumpLen = 0;
            if (this.pumpChart.data.datasets[this.pumpIndex].data.length > 0) {
                // already have data
                for (let i = pumpcount - 1; i >= 0; i--) {
                    pumpLen = this.pumpChart.data.datasets[this.pumpIndex].data.push({
                        t: pumpdata[i]['attributes']['timestamp'] - this.offset,
                        y: pumpdata[i]['attributes']['value']
                    });
                    if (pumpLen > this.maxPoints) {
                        // remove extra
                        this.pumpChart.data.datasets[this.pumpIndex].data.shift();
                    }
                }
            } else {
                // no data
                let pumpLen = 0;
                for (let i = 0; i < pumpcount; i++) {
                    pumpLen = this.pumpChart.data.datasets[this.pumpIndex].data.unshift({
                        t: pumpdata[i]['attributes']['timestamp'] - this.offset,
                        y: pumpdata[i]['attributes']['value']
                    });
                }
                // guaranteed not to have more than maxPoints in the incoming data\
                // so no need to remove extras
            }
        }
    };


    this.updatePump = function (adata) {
        this.updateData(adata);
        this.draw();
        let pump = this;
        setTimeout(function () {
                        pump.startUpdatePump();
                    }, this.period);
    };

    this.startUpdatePump = function () {
        let sts = new Date(this.lastLoaded);
        let ts = new Date();
        this.lastLoaded = ts;
        let pump = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString(), 'datapts': this.maxPoints},
            function (data) {
                // can't use this here as it is set at runtime
                pump.updatePump(data);
            });
    };

    this.setupPump = function () {
        let sts = new Date();
        let ts = new Date(sts);
        sts.setHours(sts.getHours() - 24);
        this.lastLoaded = ts;
        let pump = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString(), 'datapts': this.maxPoints },
            function (data) {
            // can't use this here as it is set at runtime
                pump.updatePump(data);
            });
    };


    this.draw = function () {
        this.gaugeIn.draw();
        let newcls = 'circpump-stop';
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


