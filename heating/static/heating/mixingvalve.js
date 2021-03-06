

function MixingValve(name, return_div, out_div, boiler_div, chart_div, url, period) {
    this.name = name;
    this.url = url;
    this.period = period;

    this.chartConfig = {
        type: 'line',
        data: {
            datasets: [{
                label: 'RETURN',
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
                label: 'BOILER',
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
    this.gaugeReturn = new RadialGauge({
        renderTo: return_div,
        title: 'RETURN',
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
    this.gaugeBoiler = new RadialGauge({
        renderTo: boiler_div,
        title: 'BOILER',
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
    this.boilerIndex = 2;

    // last ts loaded
    this.lastLoaded;

    this.updateData = function(adata) {
        let sincount = adata['data']['sensor_sys_in']['count'];
        let sindata = adata['data']['sensor_sys_in']['data']
        if (sincount > 0) {
            // data comes in latest first
            this.gaugeReturn.value = sindata[0]['attributes']['value'];
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

        let sboilercount = adata['data']['sensor_boiler_in']['count']
        let sboilerdata = adata['data']['sensor_boiler_in']['data']
        if (sboilercount > 0) {
            // data comes in latest first
            this.gaugeBoiler.value = sboilerdata[0]['attributes']['value'];
            let sboilerLen = 0;
            if (this.lineChart.data.datasets[this.boilerIndex].data.length > 0) {
                // already have data
                for (let i = sboilercount - 1; i >= 0; i--) {
                    sboilerLen = this.lineChart.data.datasets[this.boilerIndex].data.push({
                        t: sboilerdata[i]['attributes']['timestamp'] - this.offset,
                        y: sboilerdata[i]['attributes']['value']
                    });
                    if (sboilerLen > this.maxPoints) {
                        // remove extra
                        this.lineChart.data.datasets[this.boilerIndex].data.shift();
                    }
                }
            } else {
                // no data
                let sboilerLen = 0;
                for (let i = 0; i < sboilercount; i++) {
                    sboilerLen = this.lineChart.data.datasets[this.boilerIndex].data.unshift({
                        t: sboilerdata[i]['attributes']['timestamp'] - this.offset,
                        y: sboilerdata[i]['attributes']['value']
                    });
                }
                // guaranteed not to have more than maxPoints in the incoming data\
                // so no need to remove extras
            }
        }
    };


    this.updateValve = function (adata) {
        this.updateData(adata);
        this.draw();
        let valve = this;
        setTimeout(function () {
                        valve.startUpdateValve();
                    }, this.period);
    };

    this.startUpdateValve = function () {
        let sts = new Date(this.lastLoaded);
        let ts = new Date();
        this.lastLoaded = ts;
        let valve = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString(), 'datapts': this.maxPoints},
            function (data) {
                // can't use this here as it is set at runtime
                valve.updateValve(data);
            });
    };

    this.setupValve = function () {
        let sts = new Date();
        let ts = new Date(sts);
        sts.setHours(sts.getHours() - 24);
        this.lastLoaded = ts;
        let valve = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString(), 'datapts': this.maxPoints },
            function (data) {
            // can't use this here as it is set at runtime
                valve.updateValve(data);
            });
    };


    this.draw = function () {
        this.gaugeReturn.draw();
        this.gaugeOut.draw();
        this.gaugeBoiler.draw();
        this.lineChart.update();
    };
}
