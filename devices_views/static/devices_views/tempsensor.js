// TempSensor class
class TempSensor {
        constructor(name, gauge_div, chart_div, hours, url, period) {
        this.name = name;
        this.url = url;
        this.period = period;
        this.hours = hours;

        this.gauge = null;
        if (gauge_div) {
            this.gauge = new LinearGauge({
                renderTo: gauge_div,
                title: 'temp',
                width: 400, height: 150,
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
                        label: 'TEMP',
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
            var ctx = document.getElementById(chart_div).getContext('2d');
            this.lineChart = new Chart(ctx, this.chartConfig);

            // max data points to display in chart
            this.maxPoints = 0;
        }

        // this.offset = new Date().getTimezoneOffset() * 60 * 1000;
        // dataset indices
        this.index = 0;
        // last ts loaded
        this.lastLoaded = null;
    }

    updateData(adata) {
        let scount = adata['count'];
        if (scount > this.maxPoints) this.maxPoints = scount;
        let sdata = adata['data']
        if (scount > 0) {
            // data comes in latest first
            if (this.gauge) {
                this.gauge.value = sdata[0]['attributes']['value'];
            }
            if (this.lineChart) {
                let sLen = 0;
                if (this.lineChart.data.datasets[this.index].data.length > 0) {
                    // already have data
                    for (let i = scount - 1; i >= 0; i--) {
                        sLen = this.lineChart.data.datasets[this.index].data.push({
                            t: sdata[i]['attributes']['timestamp'],
                            y: sdata[i]['attributes']['value']
                        });
                        if (sLen > this.maxPoints) {
                            // remove extra
                            this.lineChart.data.datasets[this.index].data.shift();
                        }
                    }
                } else {
                    // no data
                    for (let i = 0; i < scount; i++) {
                        sLen = this.lineChart.data.datasets[this.index].data.unshift({
                            t: sdata[i]['attributes']['timestamp'],
                            y: sdata[i]['attributes']['value']
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
        let sensor = this;
        setTimeout(function () {
                        sensor.startUpdate();
                    }, this.period);
    }

    startUpdate() {
        let sts = new Date(this.lastLoaded);
        let ts = new Date();
        this.lastLoaded = ts;
        let sensor = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString() },
            function (data) {
                // can't use this here as it is set at runtime
                sensor.update(data);
            });
    };

    setup () {
        let sts = new Date();
        let ts = new Date(sts);
        sts.setHours(sts.getHours() - this.hours);
        this.lastLoaded = ts;
        let sensor = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString()},
            function (data) {
            // can't use this here as it is set at runtime
                sensor.update(data);
            });
    }

    draw() {
        if (this.gauge) {
            this.gauge.draw();
        }
        if (this.lineChart) {
            this.lineChart.update();
        }
    }
}
