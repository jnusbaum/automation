
class Weather {

    constructor(name, temp_div, wind_div, sun_div, chart_div, hours, url, period) {
        this.name = name;
        this.url = url;
        this.period = period;
        this.hours = hours;

        this.gaugeTemp = null;
        if (temp_div) {
            this.gaugeTemp = new RadialGauge({
                renderTo: temp_div,
                title: 'TEMP',
                width: 200, height: 200,
                units: 'F', minValue: -20, maxValue: 100,
                majorTicks: ['-20', '-10', '0', '10', '20', '30', '40', '50', '60', '70', '80', '90', '100'],
                minorTicks: 5,
                highlights: [{from: -20, to: 0, color: 'skyblue'},
                    {from: 0, to: 40, color: 'aliceblue'},
                    {from: 40, to: 60, color: 'yellow'},
                    {from: 60, to: 80, color: 'orange'},
                    {from: 80, to: 100, color: 'red'}
                ],
                valueBox: true,
                value: 30
            });
        }
        this.gaugeWind = null;
        if (wind_div) {
            this.gaugeWind = new RadialGauge({
                renderTo: wind_div,
                title: 'WIND',
                width: 200, height: 200,
                units: 'MPH', minValue: 0, maxValue: 60,
                majorTicks: ['0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'],
                minorTicks: 5,
                highlights: [{from: 0, to: 5, color: 'skyblue'},
                    {from: 5, to: 15, color: 'aliceblue'},
                    {from: 15, to: 30, color: 'yellow'},
                    {from: 30, to: 45, color: 'orange'},
                    {from: 45, to: 60, color: 'red'}
                ],
                valueBox: true,
                value: 0
            });
        }
        this.gaugeSun = null;
        if (sun_div) {
            this.gaugeSun = new RadialGauge({
                renderTo: sun_div,
                title: 'SUN',
                width: 200, height: 200,
                units: 'L', minValue: 0, maxValue: 600,
                majorTicks: ['0', '200', '400', '600', '800', '1000', '1200', '1400', '1600'],
                minorTicks: 10,
                highlights: [{from: 0, to: 200, color: 'skyblue'},
                    {from: 200, to: 500, color: 'aliceblue'},
                    {from: 500, to: 800, color: 'yellow'},
                    {from: 800, to: 1200, color: 'orange'},
                    {from: 1200, to: 1600, color: 'red'}
                ],
                valueBox: true,
                value: 100
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
                    }, {
                        label: 'WIND',
                        borderColor: 'skyblue',
                        fill: false,
                        pointRadius: 0,
                        data: [],
                    }, {
                        label: 'SUN',
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
            var ctx = document.getElementById(chart_div).getContext('2d');
            this.lineChart = new Chart(ctx, this.chartConfig);
            this.tempMaxPoints = 0;
            this.windMaxPoints = 0;
            this.sunMaxPoints = 0;
        }

        // this.offset = new Date().getTimezoneOffset() * 60 * 1000;
        // dataset indices
        this.tempIndex = 0;
        this.windIndex = 1;
        this.sunIndex = 2;
        // last ts loaded
        this.lastLoaded = null;
    }


    updateData(adata) {
        let tempcount = adata['data']['sensor_temp']['count'];
        if (tempcount > this.tempMaxPoints) this.tempMaxPoints = tempcount;
        let tempdata = adata['data']['sensor_temp']['data']
        if (tempcount > 0) {
            // data comes in latest first
            if (this.gaugeTemp) {
                this.gaugeTemp.value = tempdata[0]['attributes']['value'];
            }
            let tempLen = 0;
            if (this.lineChart) {
                if (this.lineChart.data.datasets[this.tempIndex].data.length > 0) {
                    // already have data
                    for (let i = tempcount - 1; i >= 0; i--) {
                        tempLen = this.lineChart.data.datasets[this.tempIndex].data.push({
                            t: tempdata[i]['attributes']['timestamp'],
                            y: tempdata[i]['attributes']['value']
                        });
                        if (tempLen > this.tempMaxPoints) {
                            // remove extra
                            this.lineChart.data.datasets[this.tempIndex].data.shift();
                        }
                    }
                } else {
                    // no data
                    for (let i = 0; i < tempcount; i++) {
                        tempLen = this.lineChart.data.datasets[this.tempIndex].data.unshift({
                            t: tempdata[i]['attributes']['timestamp'],
                            y: tempdata[i]['attributes']['value']
                        });
                    }
                    // guaranteed not to have more than maxPoints in the incoming data\
                    // so no need to remove extras
                }
            }
        }

        let windcount = adata['data']['sensor_wind']['count']
        if (windcount > this.windMaxPoints) this.windMaxPoints = windcount;
        let winddata = adata['data']['sensor_wind']['data']
        if (windcount > 0) {
            // data comes in latest first
            if (this.gaugeWind) this.gaugeWind.value = winddata[0]['attributes']['value'];
            let windLen = 0;
            if (this.lineChart) {
                if (this.lineChart.data.datasets[this.windIndex].data.length > 0) {
                    // already have data
                    for (let i = windcount - 1; i >= 0; i--) {
                        windLen = this.lineChart.data.datasets[this.windIndex].data.push({
                            t: winddata[i]['attributes']['timestamp'],
                            y: winddata[i]['attributes']['value']
                        });
                        if (windLen > this.windMaxPoints) {
                            // remove extra
                            this.lineChart.data.datasets[this.windIndex].data.shift();
                        }
                    }
                } else {
                    // no data
                    for (let i = 0; i < windcount; i++) {
                        windLen = this.lineChart.data.datasets[this.windIndex].data.unshift({
                            t: winddata[i]['attributes']['timestamp'],
                            y: winddata[i]['attributes']['value']
                        });
                    }
                    // guaranteed not to have more than maxPoints in the incoming data\
                    // so no need to remove extras
                }
            }
        }

        let suncount = adata['data']['sensor_sun']['count']
        if (suncount > this.sunMaxPoints) this.sunMaxPoints = suncount;
        let sundata = adata['data']['sensor_sun']['data']
        if (suncount > 0) {
            // data comes in latest first
            if (this.gaugeBurn) this.gaugeBurn.value = sundata[0]['attributes']['value'];
            let sunLen = 0;
            if (this.lineChart) {
                if (this.lineChart.data.datasets[this.sunIndex].data.length > 0) {
                    // already have data
                    for (let i = suncount - 1; i >= 0; i--) {
                        sunLen = this.lineChart.data.datasets[this.sunIndex].data.push({
                            t: sundata[i]['attributes']['timestamp'],
                            y: sundata[i]['attributes']['value']
                        });
                        if (sunLen > this.sunMaxPoints) {
                            // remove extra
                            this.lineChart.data.datasets[this.sunIndex].data.shift();
                        }
                    }
                } else {
                    // no data
                    for (let i = 0; i < suncount; i++) {
                        sunLen = this.lineChart.data.datasets[this.sunIndex].data.unshift({
                            t: sundata[i]['attributes']['timestamp'],
                            y: sundata[i]['attributes']['value']
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
        let boiler = this;
        setTimeout(function () {
                        boiler.startUpdate();
                    }, this.period);
    }

    startUpdate() {
        let sts = new Date(this.lastLoaded);
        let ts = new Date();
        this.lastLoaded = ts;
        let boiler = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString()},
            function (data) {
                // can't use this here as it is set at runtime
                boiler.update(data);
            });
    }

    setup() {
        let sts = new Date();
        let ts = new Date(sts);
        sts.setHours(sts.getHours() - this.hours);
        this.lastLoaded = ts;
        let boiler = this;
        $.getJSON(this.url,
            {'starttime': sts.toISOString(), 'endtime': ts.toISOString()},
            function (data) {
            // can't use this here as it is set at runtime
                boiler.update(data);
            });
    }

    draw() {
        if (this.gaugeTemp) this.gaugeTemp.draw();
        if (this.gaugeWind) this.gaugeWind.draw();
        if (this.gaugeBurn) this.gaugeBurn.draw();
        if (this.lineChart) this.lineChart.update();
    }
}
