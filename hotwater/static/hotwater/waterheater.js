

function __heaterDataCallback(adata, heater, func) {
    func.call(heater, adata);
}

function __heaterCallback(heater, func) {
    func.call(heater);
}


function WaterHeater(name, in_div, out_div, burn_div, chart_div, url, period) {
    this.name = name;
    this.url = url;
    this.period = period;

    this.chartConfig = {
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
    this.gaugeOut = new RadialGauge({
        renderTo: out_div,
        title: 'OUT',
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
    this.gaugeBurn = new RadialGauge({
        renderTo: burn_div,
        title: 'BURN',
        width: 200, height: 200,
        units: 'F', minValue: 30, maxValue: 270,
        majorTicks: ['30', '60', '90', '120', '150', '180', '210', '240', '270'],
        minorTicks: 6,
        highlights: [{from: 30, to: 60, color: 'skyblue'},
            {from: 60, to: 90, color: 'aliceblue'},
            {from: 90, to: 120, color: 'yellow'},
            {from: 120, to: 150, color: 'orange'},
            {from: 150, to: 270, color: 'red'}
        ],
        valueBox: true,
        value: 30
    });
    var ctx = document.getElementById(chart_div).getContext('2d');
    this.lineChart = new Chart(ctx, this.chartConfig);

    this.offset = new Date().getTimezoneOffset() * 60 * 1000;

    // max data points to display in chart
    this.maxPoints = 9000;

    // dataset indices
    this.inIndex = 0;
    this.outIndex = 1;
    this.burnIndex = 2;

    // last ts loaded
    this.lastLoaded;

    this.updateData = function(adata) {
        let sincount = adata['data']['sensor_in']['count'];
        let sindata = adata['data']['sensor_in']['data']
        if (sincount > 0) {
            // data comes in latest first
            this.gaugeIn.value = sindata[0]['attributes']['value'];
            let sinLen = 0;
            if (this.lineChart.data.datasets[this.inIndex].data.length > 0) {
                // already have data
                for (let i = sincount - 1; i >= 0; i--) {
                    sinLen = this.lineChart.data.datasets[this.inIndex].data.push({
                        t: sindata[i]['attributes']['timestamp'] - this.offset,
                        y: sindata[i]['attributes']['value']
                    });
                    if (sinLen > this.maxPoints) {
                        // remove extra
                        this.lineChart.data.datasets[this.inIndex].data.shift();
                    }
                }
            } else {
                // no data
                let sinLen = 0;
                for (let i = 0; i < sincount; i++) {
                    sinLen = this.lineChart.data.datasets[this.inIndex].data.unshift({
                        t: sindata[i]['attributes']['timestamp'] - this.offset,
                        y: sindata[i]['attributes']['value']
                    });
                }
                // guaranteed not to have more than maxPoints in the incoming data\
                // so no need to remove extras
            }
        }

        let soutcount = adata['data']['sensor_out']['count']
        let soutdata = adata['data']['sensor_out']['data']
        if (soutcount > 0) {
            // data comes in latest first
            this.gaugeOut.value = soutdata[0]['attributes']['value'];
            let soutLen = 0;
            if (this.lineChart.data.datasets[this.outIndex].data.length > 0) {
                // already have data
                for (let i = soutcount - 1; i >= 0; i--) {
                    soutLen = this.lineChart.data.datasets[this.outIndex].data.push({
                        t: soutdata[i]['attributes']['timestamp'] - this.offset,
                        y: soutdata[i]['attributes']['value']
                    });
                    if (soutLen > this.maxPoints) {
                        // remove extra
                        this.lineChart.data.datasets[this.outIndex].data.shift();
                    }
                }
            } else {
                // no data
                let soutLen = 0;
                for (let i = 0; i < soutcount; i++) {
                    soutLen = this.lineChart.data.datasets[this.outIndex].data.unshift({
                        t: soutdata[i]['attributes']['timestamp'] - this.offset,
                        y: soutdata[i]['attributes']['value']
                    });
                }
                // guaranteed not to have more than maxPoints in the incoming data\
                // so no need to remove extras
            }
        }

        let sburncount = adata['data']['sensor_burn']['count']
        let sburndata = adata['data']['sensor_burn']['data']
        if (sburncount > 0) {
            // data comes in latest first
            this.gaugeBurn.value = sburndata[0]['attributes']['value'];
            let sburnLen = 0;
            if (this.lineChart.data.datasets[this.burnIndex].data.length > 0) {
                // already have data
                for (let i = sburncount - 1; i >= 0; i--) {
                    sburnLen = this.lineChart.data.datasets[this.burnIndex].data.push({
                        t: sburndata[i]['attributes']['timestamp'] - this.offset,
                        y: sburndata[i]['attributes']['value']
                    });
                    if (sburnLen > this.maxPoints) {
                        // remove extra
                        this.lineChart.data.datasets[this.burnIndex].data.shift();
                    }
                }
            } else {
                // no data
                let sburnLen = 0;
                for (let i = 0; i < sburncount; i++) {
                    sburnLen = this.lineChart.data.datasets[this.burnIndex].data.unshift({
                        t: sburndata[i]['attributes']['timestamp'] - this.offset,
                        y: sburndata[i]['attributes']['value']
                    });
                }
                // guaranteed not to have more than maxPoints in the incoming data\
                // so no need to remove extras
            }
        }
    };


    this.updateHeater = function (adata) {
        this.updateData(adata);
        this.draw();
        setTimeout(() => __heaterCallback(this, this.startUpdateHeater), this.period);
    };

    this.startUpdateHeater = function () {
        let sts = new Date(this.lastLoaded);
        let ts = new Date();
        this.lastLoaded = ts;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString(), 'datapts': this.maxPoints},
            data => __heaterDataCallback(data, this, this.updateHeater)
        );
    };

    this.setupHeater = function () {
        let sts = new Date();
        let ts = new Date(sts);
        sts.setHours(sts.getHours() - 24);
        this.lastLoaded = ts;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString(), 'datapts': this.maxPoints },
            data => __heaterDataCallback(data, this, this.updateHeater)
            );
    };

    this.draw = function () {
        this.gaugeIn.draw();
        this.gaugeOut.draw();
        this.gaugeBurn.draw();
        this.lineChart.update();
    };
}
