// Zone class
class Zone {

    constructor(name, in_div, out_div, chart_div, hours, url, period) {
        this.name = name;
        this.url = url;
        this.period = period;
        this.hours = hours;

        this.gaugeIn = null;
        if (in_div) {
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
        }

        this.gaugeOut = null;
        if (out_div) {
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
        }

        this.lineChart = null;
        if (chart_div) {
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
            var ctx = document.getElementById(chart_div).getContext('2d');
            this.lineChart = new Chart(ctx, this.chartConfig);

            this.inMaxPoints = 0;
            this.outMaxPoints = 0;
        }

        this.offset = new Date().getTimezoneOffset() * 60 * 1000;
        // dataset indices
        this.inIndex = 0;
        this.outIndex = 1;
        // last ts loaded
        this.lastLoaded = null;
    }

    updateData(adata) {
        let sincount = adata['data']['sensor_in']['count'];
        if (sincount > this.inMaxPoints) this.inMaxPoints = sincount;
        let sindata = adata['data']['sensor_in']['data']
        if (sincount > 0) {
            // data comes in latest first
            if (this.gaugeIn) this.gaugeIn.value = sindata[0]['attributes']['value'];
            let sinLen = 0;
            if (this.lineChart) {
                if (this.lineChart.data.datasets[this.inIndex].data.length > 0) {
                    // already have data
                    for (let i = sincount - 1; i >= 0; i--) {
                        sinLen = this.lineChart.data.datasets[this.inIndex].data.push({
                            t: sindata[i]['attributes']['timestamp'] - this.offset,
                            y: sindata[i]['attributes']['value']
                        });
                        if (sinLen > this.inMaxPoints) {
                            // remove extra
                            this.lineChart.data.datasets[this.inIndex].data.shift();
                        }
                    }
                } else {
                    // no data
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
        }

        let soutcount = adata['data']['sensor_out']['count']
        if (soutcount > this.outMaxPoints) this.outMaxPoints = soutcount;
        let soutdata = adata['data']['sensor_out']['data']
        if (soutcount > 0) {
            // data comes in latest first
            if (this.gaugeOut) this.gaugeOut.value = soutdata[0]['attributes']['value'];
            let soutLen = 0;
            if (this.lineChart) {
                if (this.lineChart.data.datasets[this.outIndex].data.length > 0) {
                    // already have data
                    for (let i = soutcount - 1; i >= 0; i--) {
                        soutLen = this.lineChart.data.datasets[this.outIndex].data.push({
                            t: soutdata[i]['attributes']['timestamp'] - this.offset,
                            y: soutdata[i]['attributes']['value']
                        });
                        if (soutLen > this.outMaxPoints) {
                            // remove extra
                            this.lineChart.data.datasets[this.outIndex].data.shift();
                        }
                    }
                } else {
                    // no data
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
        }
    }

    update(adata) {
        this.updateData(adata);
        this.draw();
        let zone = this;
        setTimeout(function () {
                        zone.startUpdate();
                    }, this.period);
    }


    startUpdate() {
        let sts = new Date(this.lastLoaded);
        let ts = new Date();
        this.lastLoaded = ts;
        let zone = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString() },
            function (data) {
                // can't use this here as it is set at runtime
                zone.update(data);
            });
    }


    setup() {
        let sts = new Date();
        let ts = new Date(sts);
        sts.setHours(sts.getHours() - this.hours);
        this.lastLoaded = ts;
        let zone = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString() },
            function (data) {
            // can't use this here as it is set at runtime
                zone.update(data);
            });
    }

    draw() {
        if (this.gaugeIn) {
            this.gaugeIn.draw();
        }
        if (this.gaugeOut) {
            this.gaugeOut.draw();
        }
        if (this.lineChart) {
            this.lineChart.update();
        }
    }
}
