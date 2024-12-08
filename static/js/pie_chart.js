document.addEventListener('DOMContentLoaded', function () {
    var chart1 = Highcharts.chart(chart_id_y, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: chart_type
        },
        title: {
            text: title1
        },
        accessibility: {
            point: {
                valueSuffix: '$'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                }
            }
        },
        series: [{
            name: 'Revenue Comparison',
            colorByPoint: true,
            data: [{
                name: 'Annually direct income',
                y: annually_direct,
                sliced: true,
                selected: true
            },{
                name: 'Annually indirect income',
                y: annually_indirect
            }]
        }]
    });
    var chart2 = Highcharts.chart(chart_id_m, {
        chart: {
            plotBackgroundColor: null,
            plotBorderWidth: null,
            plotShadow: false,
            type: chart_type
        },
        title: {
            text: title2
        },
        accessibility: {
            point: {
                valueSuffix: '$'
            }
        },
        plotOptions: {
            pie: {
                allowPointSelect: true,
                cursor: 'pointer',
                dataLabels: {
                    enabled: true,
                }
            }
        },
        series: [{
            name: 'Revenue Comparison',
            colorByPoint: true,
            data: [{
                name: 'Monthly direct income',
                y: monthly_direct,
                sliced: true,
                selected: true
            },{
                name: 'Monthly indirect income',
                y: monthly_indirect
            }]
        }]
    });
});
